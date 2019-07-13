source log.sh
domain="https://100.100.199.100:500/caesar/cast"
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

