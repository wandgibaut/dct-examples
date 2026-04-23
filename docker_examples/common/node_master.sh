#!/bin/bash

set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"
ROOT_NODE_DIR="${ROOT_NODE_DIR:-$(pwd)}"

require_dct_package()
{
  if "$PYTHON_BIN" -c "import dct" >/dev/null 2>&1; then
    return 0
  fi
  echo "Unable to import the dct package. Install dct-python in this Python environment." >&2
  exit 1
}

load_param()
{
  unset internal_codelets
  unset active_codelets
  unset signals
  unset memory
  eval "$("$PYTHON_BIN" -m dct.parser < "$ROOT_NODE_DIR"/param.ini)"
}

check_integrity()
{
  for PID in "${PIDARRAY[@]}"; do
    if [[ -d "/proc/${PID}" ]]; then
      echo "process ${PID} exists"
    else
      echo "need regenerate ${PID}"
      regenerate_process "$PID"
    fi
  done
}

regenerate_process()
{
  for (( i = 0; i < "${#PIDARRAY[@]}"; i++ )); do
    if [[ "${PIDARRAY[$i]}" == "$1" ]]; then
      if [[ "${NAMEARRAY[$i]}" == "server" ]]; then
        "$PYTHON_BIN" -m dct.server "${SERVER_IPS[0]}" &
        PIDARRAY["$i"]=$!
        echo "server regenerated!"
      else
        if containsElement "${NAMEARRAY[$i]}" "${active_codelets[@]}"; then
          "$PYTHON_BIN" "$ROOT_NODE_DIR"/codelets/"${NAMEARRAY[$i]}"/codelet.py &
          PIDARRAY["$i"]=$!
          echo "regenerated!"
        else
          eliminate_codelet "$i"
          echo "eliminated!"
        fi
      fi
    fi
  done
}

eliminate_codelet()
{
  local eliminated_name="${NAMEARRAY[$1]}"
  local new_name_array=()
  local new_pid_array=()

  kill "${PIDARRAY[$1]}" 2>/dev/null || true
  unset PIDARRAY["$1"]
  unset NAMEARRAY["$1"]

  for i in "${!NAMEARRAY[@]}"; do
    new_name_array+=( "${NAMEARRAY[$i]}" )
    new_pid_array+=( "${PIDARRAY[$i]}" )
    echo "${NAMEARRAY[$i]}"
  done

  declare -g NAMEARRAY=("${new_name_array[@]}")
  declare -g PIDARRAY=("${new_pid_array[@]}")

  echo "$eliminated_name eliminated!"
}

run_new_codelet()
{
  for codelet in "${internal_codelets[@]}"; do
    if [[ "$codelet" == "$1" ]]; then
      NAMEARRAY+=("$1")
      "$PYTHON_BIN" "$ROOT_NODE_DIR"/codelets/"$1"/codelet.py &
      PIDARRAY+=($!)
      echo "ran $1!"
    fi
  done
}

check_codelets()
{
  for (( i = 0; i < "${#NAMEARRAY[@]}"; i++ )); do
    if [[ "${NAMEARRAY[i]}" != "server" ]] && ! containsElement "${NAMEARRAY[i]}" "${active_codelets[@]}"; then
      eliminate_codelet "$i"
    fi
  done

  for codelet in "${active_codelets[@]}"; do
    if ! containsElement "$codelet" "${NAMEARRAY[@]}"; then
      run_new_codelet "$codelet"
    fi
  done
}

containsElement()
{
  local element
  local match="$1"
  shift
  for element in "$@"; do
    [[ "$element" == "$match" ]] && return 0
  done
  return 1
}

require_dct_package

PIDARRAY=()
NAMEARRAY=()
SERVER_IPS=()

if [[ $# -ne 0 ]]; then
  echo "initiating servers!"
  for var in "$@"; do
    NAMEARRAY+=("server")
    SERVER_IPS+=("$var")
    echo "$var"
    "$PYTHON_BIN" -m dct.server "$var" &
    PIDARRAY+=($!)
  done
fi

load_param

for var in "${active_codelets[@]}"; do
  NAMEARRAY+=("$var")
  "$PYTHON_BIN" "$ROOT_NODE_DIR"/codelets/"$var"/codelet.py &
  PIDARRAY+=($!)
done

if [[ "${memory[redis]:-false}" == true && "${#SERVER_IPS[@]}" -gt 0 ]]; then
  port="$(echo "${SERVER_IPS[0]}" | cut -f 2 -d ":")"
  redis-server \
    --port "$((port + 1))" \
    --save "${memory[seconds]:-3600}" "${memory[changes]:-1}" \
    --dir "${memory[dir]:-./storage}" \
    --dbfilename "${memory[dbfilename]:-memory.rdb}" &
fi

while [[ "${signals[suicide_note]:-false}" == false ]]; do
  load_param
  check_integrity
  check_codelets
  sleep 5
done
