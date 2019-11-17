import paramiko
import time


class Ssh(object):
    """
    if use root to login, make sure root permit function: connet_root-->permit_root_login
    else use function connect
    """
    def __init__(self,  **kwargs):
        opt_args = {
            "host": None,
            'host_port': 22,
            'username': 'root',
            'password': None,
            'sftp_support': True,
            'root_password': None
            }
        opt_args.update(kwargs)
        self.ssh_timeout = 4
        self.host = opt_args['host']
        self.host_port = opt_args['host_port']
        self.username = opt_args['username']
        self.password = opt_args['password']
        self.sftp_support = opt_args['sftp_support']
        self.root_ssh = None
        self.root_password = opt_args['root_password']
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.sftp_client = None
        self.transport = None

    def connect(self):
        if self.username and self.password and self.host:
            self.ssh_client.connect(hostname=self.host,
                                    port=self.host_port,
                                    username=self.username,
                                    password=self.password,
                                    timeout=self.ssh_timeout)
            self.transport = self.ssh_client.get_transport()
            if self.sftp_support:
                ftp_transport = paramiko.Transport(self.host, self.host_port)
                ftp_transport.connect(username=self.username, password=self.password)
                self.sftp_client = paramiko.SFTPClient.from_transport(ftp_transport)
        else:
            raise Exception('password or username is None, exit')

    def connect_root(self):
        if self.username and self.password and self.host:
            self.ssh_client.connect(hostname=self.host,
                                    port=self.host_port,
                                    username=self.username,
                                    password=self.password,
                                    timeout=self.ssh_timeout)
            self.root_ssh = self.ssh_client.invoke_shell()
            resp = self.root_execute("su - root")
            if resp.endswith(u"Password: "):
                self.root_execute(self.root_password)
                if not self.is_root_user:
                    raise Exception("transfer to root failed")

    def execute_cmd(self, cmd, timeout=20):
        buffersize = -1
        ret = True
        try:
            session = self.transport.open_session()
            session.settimeout(timeout)
            session.exec_command(cmd)
            stdout = session.makefile('rb', buffersize)
            stderr = session.makefile_stderr('rb', buffersize)
            error = ''.join(str(lines) for lines in stderr.readlines())
            output = ''.join(str(lines) for lines in stdout.readlines())
            if len(error) > 0:
                ret = False
                return False , output, error
        except Exception as e:
            return False, "Socket TimeOut", "Socket Timeout"
        return ret, output, error

    def root_execute(self, cmd, timesleep=0.1):
        self.root_ssh.send("%s\n" %cmd)
        time.sleep(timesleep)
        resp = self.root_ssh.recv(9999).decode("utf8")
        return resp

    def permit_root_login(self,timesleep=0.1):
        self.root_execute("sed -i 's/#PermitRootLogin yes/PermitRootLogin yes/g'"
                          "  /etc/ssh/sshd_config")
        ret = self.root_execute("echo $?")
        if not "0" in ret:
            raise Exception("modify permit root "
                            "login failed")
        time.sleep(timesleep)
        self.root_execute("service sshd restart")

    def is_root_user(self):
        user_info = self.root_execute("whoami")
        if "root" in user_info:
            return True
        return False


    def upload_file(self, local_file_path, remote_file_path):
        return self.sftp_client.put(local_file_path, remote_file_path)

    def download_file(self, local_file_path, remote_file_path):
        self.sftp_client.get(remote_file_path, local_file_path)

    def close_connection(self):
        self.ssh_client.close()
        self.sftp_client.close()

