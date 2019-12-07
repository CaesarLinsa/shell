#!/usr/bin/bash

user="$1"
user_passwd="$2"
root_passwd="$3"
exec_command="$4"

while read host
do
   ./ssh_exec.exp $user $host $user_passwd $root_passwd "$exec_command"
done < host_ips

