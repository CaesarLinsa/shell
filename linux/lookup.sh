#!/bin/sh
# this program is to save the user info
# in caesar.txt with the user input

file=/home/caesar/caesar.txt

is_file_exits(){
   if [ -f $1 ]
    then
        :
   else
     echo "file  is not exits and make for it"
     dir_name=$($1 %/*)
     if [ -d $dir_name ]
        then mkdir -p $dir_name
     fi
     touch $1
     exit 0
   fi
}

show_menu(){
    echo "[1] Add Entry"
    echo "[2] Delete Entry"
    echo "[3] View Entry"
    echo "[4] Exit"
}

add_entry(){
echo "do you want to add a user info in useinfo.txt?yes/no"
read answer
if [ $answer == "yes" -o $answer == "y" ]
then
   is_file_exits $file
   echo "please input username:"
   read username
   echo "please input password:"
   read password
   echo "please input your age:"
   read age
   echo "$username;$password;$age" >>$file
   echo "add $username successful"
   echo "$(grep -nr $username $file)"
fi
}

is_user_exist(){
  grep "$1" $file >/dev/null
  ret=$?
  if [ $ret -ne 0 ]
    then
       echo "username $1 is not in the file,please check"
       return 1
    else
       return 0
   fi
}

delete_entry(){
   echo "enter you want delete username:"
   read username
   is_user_exist $username
   if [ $? -eq 0 ]
      then
         sed /$username/d $file >$file
         echo "delete $username successful"
    fi

}
view_entry(){
  echo "enter the username or number you want to view"
  read username
  sed -n /$username/p $file
}

show_menu
read option
case $option in
    1) add_entry;;
    2) delete_entry;;
    3) view_entry;;
    4) exit_view;;
esac
