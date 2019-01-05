#! /bin/sh
# this is check user whether
# exist in /etc/passwd file

while getopts u: option
do
   if [ -z $option -o -z $OPTARG ]
    then
       echo "[USAGE]: -u username"
    fi
    usercount=$(cat /etc/passwd |awk -F: '{print $1}'|grep -c $OPTARG)
   if [ $usercount -ne 0 ]
    then
      echo "user $OPTARG is found"
    else
      echo "user $OPTARG is not found"
    fi
done
