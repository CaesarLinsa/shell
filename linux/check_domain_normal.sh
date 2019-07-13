source log.sh

check_domain_normal(){
    # domain=https://www.baidu.com:8090/caesar/rest
    local domain="$1"
    domain_ip=$(echo $domain |sed "{s/[^/]*\/\///;s/:.*//}")
    ping_info=$(ping $domain_ip -c 4)
    sa=$(echo "$ping_info"|grep -v "100% packet loss"|grep "0% packet loss")
    if [ -z "$sa" ]
      then
       log_error "ping  $domain_ip is unreachable"
      else
       ip=$(echo "$ping_info" |grep "time=" |sed '{s/[^(]*(//;s/).*//;q}')
       log_info "ping $domain_ip is  $ip  normal"
    fi
}

check_file_modify_time(){
 local file=$1 
 file_time=$(stat -c %Y $file)
 ctime=$(date +%s)
 if [ $(($ctime - $file_time)) -ge 3600 ]
 then
   log_info "test.sh is modify more than 3600 seconds"
 fi 
}

check_file_exist_key_words(){
  local file="$1"
  local key_word="$2"
  chour=$(date +"%Y-%m-%dT%H")
  error_infos=$(cat $file |grep "$chour"|grep $key_word)
  if [ ! -z "$error_infos" ]
  then
    log_error "$error_infos"
  fi
}

