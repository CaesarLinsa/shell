#!/bin/sh
#
# 每隔1min统计，文档中关键字次数的变化
#
file="/var/log/mongodb/mongodb.log"
count=0
while true
do
 if [ $count -lt 1 ];then
 # 首次统计文档中关键字次数
 num=`grep -c "ceilometer" $file`
 else
    # 每隔1min统计关键字次数，并将两者最差输出
    this_num=`grep -c "ceilometer" $file`
    number=`expr $this_num - $num`
    #以增加后的次数作为基数
    num=$this_num
    echo $number
 fi
 let count++
 sleep 60
done
