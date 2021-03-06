# python and linux shell learn

一个在工作和学习中遇到的一些问题并进行编写的shell脚本的工程。工欲善其事必先利其器，脚本还在增长的过程中，凡是对工作可以优化的shell都会存放在此工程下，避免出现过河拆桥，用罢则扔，需要又写的尴尬处境。

## log_util.py
对原生logging模块封装，可以方便地使用在项目中

显示在控制台
``` python
log_util.setup(level=logging.DEBUG,
                 outs=[log_util.StreamOut(level=logging.DEBUG)],
                 program_name=None,
                 capture_warnings=True)
LOG = logging.getLogger(__name__)
LOG.info("caesar come here")
```
记录到日志
``` python
import logging
import log_util
log_util.setup(level=logging.DEBUG,
                 outs=[log_util.File(filename="caesar.log",
                                       level=logging.DEBUG)],
                 program_name=None,
                 capture_warnings=True)

LOG = logging.getLogger(__name__)
LOG.info("caesar come here")
```
或者以固定大小归档日志
``` python
log_util.setup(level=logging.DEBUG,
               outs=[log_util.RotatingFile(filename="caesar.log",
                                            level=logging.DEBUG,
                                            max_size_bytes=1000,
                                            backup_count=3)],
                 program_name=None,
                 capture_warnings=True)

LOG = logging.getLogger(__name__)
LOG.info("caesar come here")
```
## ConfigParse.py

一个ini文件读写的脚本，通过该脚本可以读取ini文件内容转为dict格式，或者将dict内容写入ini文件。写入的dict会进行格式校验，形如{str:{str:str|int|float}}格式。

```python
>>> from ConfigParse import ConfigParse
>>> ini = ConfigParse('setup.ini')
>>> di = {'ciro':{'name':'ciro',"age":18}}
>>> ini.write_file(di)
>>>
>>>
>>> ini.read_file()
{'ciro': {'age': '18', 'name': 'ciro'}}
>>>
```
## timeout.py
启动一个进程，执行某代码段，若超时(时间可以设置，默认10秒)，则退出脚本
```python
from timeout import TimeOut

def test():
    import time
    time.sleep(12)

with TimeOut():
    print("start")
    test()
    print("end")
```
执行后，结果见下:
start
Traceback (most recent call last):
  File "test.py", line 9, in <module>
    test()
  File "test.py", line 5, in test
    time.sleep(12)
  File "/home/caesar/shell/python/timeout.py", line 14, in handle_alarm_signal
    raise TimeOutException("timeout")

## query_json.py
json文件搜索，每行一个json对象。根据json对象中属性进行搜索，将符合条件的json对象打印出来。
```python
cat json.db
{"name":"caesar","age":18}
{"name":"caesar","age":19}

python query_json.py  json.db "{\"gt\":{\"age\":17}}"
{"name":"caesar","age":18}
{"name":"caesar","age":19}

python query_json.py  json.db "{\"gt\":{\"age\":19}}"

python query_json.py  json.db "{\"ge\":{\"age\":19}}"
{"name":"caesar","age":19}
```
## evar.py
对方法参数及其返回值进行类型判断，如果不满足类型，则报错
```python
from evar import expose

@expose(int, int, int, return_type=int)
def spam(x, y, z=42):
    return x * y * z

print(spam(1, 2))
```

## exec_remote_shell

登录远程服务器执行命令，尤其对多台服务器进行管理。在host_ips中加入服务器ip，执行./exec_remote_shell.sh user host user_password root_password "exec_command"。

## file_compare.py
对相似两个目录文件进行对比，基于第一个目录dir1，计算比第二个目录dir2多出的文件和不同文件的不同内容。执行python file_compare.py dir1 dir2。

## code_analysis.py

一个python代码分析脚本，通过装饰器profile装饰的方法，方法一旦调用会将该方法中的所有变量值进行打印，对于分析脚本中逻辑错误非常有用。通过from code_analysis import profile 装饰需要分析的方法。

```python
@profile
def print_ok(a,b):
    print("ok")
>>>b=2 a=1
    c = a+b
>>>c=3
    print c
>>>c=3 b=2 a=1
    d = a +b +c
>>>c=3 b=2 a=1 d=6
```

## FileLock.py

一个文件锁类，通过该类可以实现在对文件访问时加锁，避免其他进程访问，待进程释放锁后，其他进程才可进行文件修改

## file_keyword_count.sh

一个日志分析脚本，通过脚本可以每隔1min获取日志中关键字出现的次数。使用 bash
file_keyword_count.sh $keyworld  $filepath

```
[root@localhost linux]# bash file_keyword_count.sh 123 caesar.txt
2019-05-04T19:33:57 	 0
2019-05-04T19:34:57 	 12
2019-05-04T19:35:57 	 41
```

## git_script

配置git后(ssh rsa),在project_info.txt中添加工程信息，工程名(projectname)，分支(branch)和url后，使用此脚本，自动化完成工程的下载和分支的切换，尤其对众多工程下载和进行比对时。将此脚本和project_info.txt放在目录下，使用bash git_download.sh $path，在$path下，根据分支创建目录并将在此分支的工程下载，当使用bash git_download.sh，下载在脚本所在位置。

## Ssh.py
依赖paramiko库，实现登录服务器，执行linux命令，获取返回结果。示例如下:
```python
host_info = {
              "host":"196.168.1.234",
              "username":"caesar",
              "password":"123"
}
ssh = Ssh(**host_info)
ssh.connect()
ret, out, err = ssh.execute_cmd("cd /home/caesar")
print ret
ret, out, err = ssh.execute_cmd("ls -al")
print out
```

## diff_changes_to_excel.sh
对不同branch 的代码使用linux 自带diff -u dir1/  dir2/比较，如下log日志：

```linux
 +++ test.py	2019-06-28 23:17:39.507637999 +1000
@@ -1,5 +1,5 @@
 import select
-ddddd
+
 signal_pipe_r, signal_pipe_w = os.pipe()
```
通过脚本 bash diff_changes_to_excel.sh log文件，将差异文件和差异点，输出在excel的第一列和第二列，如下所示：
![image](https://github.com/CaesarLinsa/shell/blob/master/images/diff_change_to_excel.png)

