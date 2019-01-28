#!/bin/sh

#定义数组
arr=('|' '/' '--' '\')
index=0
icon=''
i=0

while [ $i -le 100 ]
do
  index=$(echo $i%4)
  # %-100s:-表示左对齐，占位置100字符 %d 对应%i数组，%c 对应数组中字符
  # \r 表示仍在本行，不用换行，营造出进度条
  # ${arr[下标]}获取数组中字符
  printf "[%-100s][%d%%][%c]\r" "$icon" "$i" "${arr[$index]}"
  icon="#"$icon
  let i++
  sleep 1
done
