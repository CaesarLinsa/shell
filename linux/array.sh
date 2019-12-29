# When calling this function, use the following construction: ary=( $(array_split "a,b,c" ",") )
# Sources:
# - https://stackoverflow.com/a/15988793/2308858
function array_split {
  local -r separator="$2"
  local -r str="$1"
  local -a ary=()

  IFS="$separator" read -a ary <<<"$str"

  echo ${ary[*]}
}
# $@ 传入的所有参数。shift num，默认参数向左移动一位，num向左移动num位
# ${#..[@]} 数组或者键值对长度
# local -r 定义变量，变量只读readonly 不可修改，array定义时，local -ar 
# Joins the elements of the given array into a string with the given separator between each element.
# Examples:
# abc=("A" "B" "C")
# array_join "," ${abc[*]}
function array_join {
  local -r separator="$1"
  shift
  local -ar values=("$@")
  local out=""
  for (( i=0; i<"${#values[@]}"; i++ )); do
    if [[ "$i" -gt 0 ]]; then
      out="${out}${separator}"
    fi
    out="${out}${values[i]}"
  done
  echo -n "$out"
}
