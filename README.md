# python and linux shell learn
一个在工作和学习中遇到的一些问题并进行编写的shell脚本的工程。工欲善其事必先利其器，脚本还在增长的过程中，凡是对工作可以优化的shell都会存放在此工程下，避免出现过河拆桥，用罢则扔，需要又写的尴尬处境。
## ConfigParse.py
一个ini文件读写的脚本，通过该脚本可以读取ini文件内容转为dict格式，或者将dict内容写入ini文件。写入的dict会进行格式校验，形如{str:{str:str|int|float}}格式。
```highlight
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
## code_analysis.py
一个python代码分析脚本，通过装饰器profile装饰的方法，方法一旦调用会将该方法中的所有变量值进行打印，对于分析脚本中逻辑错误非常有用。通过from code_analysis import profile 装饰需要分析的方法。
```highlight
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
