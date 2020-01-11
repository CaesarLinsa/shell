#!/bin/sh
# get project_info.txt project infomation about
# project, branch ,url to download project and
# checkout to branch

get_path(){
 if [ -z "$clone_path" ]
   then
      path=$(pwd)
   else
      path=$clone_path
 fi
}

download_project(){
   cd $path
   if [ ! -d $branch ]
    then
       mkdir $branch
   fi
   cd $branch
   git clone $url
   cd $project
   cur_branch=$(git branch -a |grep ^* |cut -d ' ' -f 2)
   if [ $cur_branch != $branch ]
      then
         target=$(git branch -a|grep $branch)
         git checkout -b  $branch $target
   fi
}

clone_path="$1"
get_path $clone_path
while read line
do
  project=$(echo $line|awk '{print$1}')
  branch=$(echo $line |awk  '{print $2}')
  url=$(echo $line |awk  '{print $3}')
  download_project $project $branch $url
done <project_info.txt
