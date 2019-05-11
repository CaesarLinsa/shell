# get project_info.txt project infomation about
# project, branch ,url to download project and
# checkout to branch
declare -A map=()
path=$(pwd)
while read line
do
  project=$(echo $line|awk '{print$1}')
  branch_url=$(echo $line |awk  '{print $2,$3}')
  map[$project]=$branch_url
done <project_info.txt

for project in ${!map[@]}
do
   branch=$(echo ${map[$project]}|cut -d ' ' -f 1)
   url=$(echo ${map[$project]}|cut -d ' ' -f 2)
   cd $path
   if [ ! -d $branch ]
    then
       mkdir $branch
   fi
   cd $branch
   git clone $url
   cd $project
   cur_branch=$(git branch -a |grep ^* |cut -d ' ' -f 2)
   if [ $cur_branch == $branch ]
      then
         continue
   fi
   target=$(git branch -a|grep $branch)
   git checkout -b  $branch $target
done
