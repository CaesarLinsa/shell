### linux 命令

#### expect

```bash
#!/bin/bash
expect -c "expect {
                \"no\" {send \"helloword\";}
                \"yes\" {send \"you yes\";exp_continue;}
                }
             "
```

exp_continue 继续，当交互命令匹配yes 后，send "you yes"，可继续匹配交互
当匹配no，后send "hello world"后结束

#### sort

[root@bogon linux]# cat date.txt
2017-12-02 caesar
2017-01-09 river
2017-10-23 ciro
2017-04-24 alibb
[root@bogon linux]# sort -t '-' -k 2 date.txt
2017-01-09 river
2017-04-24 alibb
2017-10-23 ciro
2017-12-02 caesar
[root@bogon linux]#

cat  文本输入 CTR+D结束输入

[root@bogon linux]# cat > helloworld.txt
 听说你来自海
    那是遥远的地方
没有人，只有浪与浪
    和曾经
   不羁的你

#### vimdiff 比对文件

CTRL+w+w 切换窗口

]c 跳跃到下一个差异点
[c 跳跃到上一个差异点

dp do point 光标所在点，进行同步
do do other 不在光标的，进行同步

### 使用grep 匹配搜索

当匹配到相应语句时，返回0
当没有匹配到语句时，返回1

