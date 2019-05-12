#!/bin/sh
# get project_info.txt project infomation about
# project, branch ,url to download project and
# checkout to branch

get_path(){
 if [ -z "$1" ]
   then
      path=$(pwd)
   else
      path="$1"
 fi
}

# $1 is projectname
# $2 is branch,$3 is url
download_project(){
   cd $path
   if [ ! -d $branch ]
    then
       mkdir $2
   fi
   cd $2
   git clone $3
   cd $1
   cur_branch=$(git branch -a |grep ^* |cut -d ' ' -f 2)
   if [ $cur_branch != $2 ]
      then
         target=$(git branch -a|grep $2)
         git checkout -b  $2 $target
   fi
}

get_path $1
while read line
do
  project=$(echo $line|awk '{print$1}')
  branch=$(echo $line |awk  '{print $2}')
  url=$(echo $line |awk  '{print $3}')
  download_project $project $branch $url
done <project_info.txt
