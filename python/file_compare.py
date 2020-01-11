import hashlib
import os
import sys


def get_md5(file_name):
    md5 = hashlib.md5()
    with open(file_name, 'rb') as f:
        for chunk in iter(lambda: f.read(2048), b''):
            md5.update(chunk)
    return md5.hexdigest()


def get_files(root_dir):
    all_files = {}
    if not root_dir.endswith("/"):
        root_dir = "%s/" % root_dir
    for root, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_md5 = get_md5(file_path)
            all_files[file_path.replace(root_dir, "")] = file_md5 
    return all_files


def execute_shell(cmd):
    return os.popen(cmd).read()


def compare_files(dir1, dir2):
    dir1_files = get_files(dir1)
    dir2_files = get_files(dir2)
    diff = {
       "diff":{},
       "add":[],
    }
    for file, md5 in dir1_files.items():
        dir1_file = os.path.join(dir1, file)
        dir2_file = os.path.join(dir2, file)
        if file in dir2_files:
            if md5 != dir2_files.get(file):
                diff_value = execute_shell("diff -u %s %s"  %(dir1_file, dir2_file))
                diff["diff"][dir1_file] = "\n%s" % diff_value
        else:
            diff["add"].append(dir1_file)
    return diff 


def compare_report(diff):
    add_data = diff.get("add")
    for add_line in add_data:
        print(add_line)
    diff_data = diff.get("diff")
    for k, v in diff_data.items():
        print(k)
        print(v)


def print_help():
    print("Usage: python file_compare.py \n"
          "              dir1:the compare base directory\n"
          "              dir2:the target compare directory\n")

if __name__ == '__main__':
    argvs = sys.argv
    if any(["--help" in argvs, "-h" in argvs,
           len(argvs) != 3]):
        print_help()
        exit(0)
    dir1 = argvs[1]
    dir2 = argvs[2]
    data = compare_files(dir1, dir2)
    compare_report(data)
