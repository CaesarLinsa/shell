#!/usr/bin/env bash

caesar="hello"

# 在定义变量，默认全局变量。如果在其他地方定义过名称，再次定义会修改原值（不安全），
# 在方法中定义变量，使用局部变量，循环中使用变量也需定义为局部，防止修改某全局变量。
global_var(){
   caesar="one two three"
   for x in $caesar
   do
      echo $x
   done
}

local_var(){
   local -r caesar="one two three"
   local x
   for x in $caesar
   do
      echo $x
   done
}
local_var
echo $caesar
