#!/usr/bin/env bash

# Log the given message at the given level. All logs are written to stderr with a timestamp.
function log {
  local -r level="$1"
  local -r message="$2"
  local -r timestamp=$(date +"%Y-%m-%d %H:%M:%S")
  local -r script_name="$(basename "$0")"
  [[ $level == "ERROR" ]] &&  echo -e "\033[31m ${timestamp}[${level}][$script_name] ${message} \033[0m" && return $?
  [[ $level == "INFO" ]]  &&  echo -e "\033[32m ${timestamp}[${level}][$script_name] ${message} \033[0m"  && return $?
}

# Log the given message at INFO level. All logs are written to stderr with a timestamp.
function log_info {
  local -r message="$1"
  log "INFO" "$message"
}


# Log the given message at ERROR level. All logs are written to stderr with a timestamp.
function log_error {
  local -r message="$1"
  log "ERROR" "$message"
}
