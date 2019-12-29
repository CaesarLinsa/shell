#!/bin/sh
# analysis the number of keyword occurrences in the file
# every 60 seconds
keyword=$1
file=$2
count=0
while true
do
 if [ $count -lt 1 ];then
 # At first,analysis the number 
 # of keyword occurrences in the file
 num=`grep -c "$keyword" $file`
 else
    # After 60 seconds,analysis the number
    # of keyword occurrences
    this_num=`grep -c "$keyword" $file`
    number=`expr $this_num - $num`
    # The increased number of times as the next
    # numbers
    num=$this_num
    time=$(date  +"%Y-%m-%dT%H:%M:%S")
    printf "%s \t %s\n" $time $number
 fi
 let count++
 sleep 60
done
