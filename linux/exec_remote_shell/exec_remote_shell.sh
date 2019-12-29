#!/usr/bin/bash

[[ $# -lt 4 ]] && printf "Usage:\n $0 user user_password root_password exec_command\n" && exit 1

user="$1"
user_passwd="$2"
root_passwd="$3"
shift 3
exec_command="$@"

while read host
do
   ./ssh_exec.exp $user $host $user_passwd $root_passwd "$exec_command"
done < host_ips

