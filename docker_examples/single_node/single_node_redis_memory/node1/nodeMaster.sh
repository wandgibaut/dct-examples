#!/bin/bash

#*****************************************************************************#
# Copyright (c) 2020  Wandemberg Gibaut                                       #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the MIT License                       #
# which accompanies this distribution, and is available at                    #
# https://opensource.org/licenses/MIT                                         #
#                                                                             #
# Contributors:                                                               #
#      W. Gibaut                                                              #
#                                                                             #
#*****************************************************************************#

check_integrity()
{
  for PID in "${PIDARRAY[@]}"
  do
    if [[ -d "/proc/${PID}" ]]
    then
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
      if [[ "${NAMEARRAY[$i]}"  == "server" ]]; then
        python3 "$ROOT_NODE_DIR"/server.py "${SERVER_IPS[0]}"  &
        PIDARRAY["$i"]=$!
        echo "server regenerated!"
      else
        if containsElement "${NAMEARRAY["$i"]}" "${active_codelets[@]}"; then
          python3 "$ROOT_NODE_DIR"/codelets/"${NAMEARRAY["$i"]}"/codelet.py  &
          PIDARRAY["$i"]=$!
          echo "regenerated!!!!"
        else
          eliminate_codelet "$i"
          echo "eliminated!"
        fi
      fi
    fi
  done
}

# working ok!
eliminate_codelet()
{
  kill "${PIDARRAY["$1"]}"
  unset PIDARRAY["$1"]
  unset NAMEARRAY["$1"]
  # rebuild arrays
  for i in "${!NAMEARRAY[@]}"; do
    new_name_array+=( "${NAMEARRAY[i]}" )
    new_pid_array+=( "${PIDARRAY[i]}" )
    echo "${NAMEARRAY[i]}"
  done
  declare -g NAMEARRAY=("${new_name_array[@]}")
  declare -g PIDARRAY=("${new_pid_array[@]}")

 echo "$codelet eliminated!"
}

# working ok!
run_new_codelet()
{
   for codelet in "${internal_codelets[@]}"; do
     if [[ "$codelet" = "$1" ]]; then
       NAMEARRAY+=("$1")
       python3 "$ROOT_NODE_DIR"/codelets/"$1"/codelet.py  &
       PIDARRAY+=($!)
       echo "ran $1!"
     fi
   done
}

check_codelets()
{
  # check if there is a codelet running that shouldn't be
  for (( i = 0; i < "${#NAMEARRAY[@]}"; i++ ))
  do
    if [[ "${NAMEARRAY[i]}" != "server" ]]; then
      if ! containsElement "${NAMEARRAY[i]}" "${active_codelets[@]}"; then
        eliminate_codelet $i
      fi
    fi
  done
  # check if there is a codelet that should be running but isn't
  for codelet in "${active_codelets[@]}"
  do
    if ! containsElement "$codelet" "${NAMEARRAY[@]}"; then
      run_new_codelet "$codelet"
    fi
  done

}

containsElement() {
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}



# array to index all pids
PIDARRAY=()
NAMEARRAY=()
SERVER_IPS=()
# initialize any number of servers, usually just one
if [ $# -ne 0 ]
    then
        echo "initiating servers!"
        for var in "$@"
        do
            NAMEARRAY+=("server")
            SERVER_IPS+=("$var")
            echo "$var"
            #python3 -m dct.server "$var"  &
            #python3 "$ROOT_NODE_DIR"/server.py "$var"  &
            python3 /usr/src/app/dct/server.py "$var"  &
            PIDARRAY+=($!)
        done
fi

# run all codelet that should run
#mapfile -t <"$ROOT_NODE_DIR"/init_codelets.txt

#eval "$(cat param.ini  |  python3 parser.py)"
eval "$(< "$ROOT_NODE_DIR"/param.ini python3 /usr/src/app/dct/parser.py)"
#eval "$(< "$ROOT_NODE_DIR"/param.ini python3 "$ROOT_NODE_DIR"/parser.py)"
# eval "$(< ./param.ini python3 ./parser.py)"


for var in "${active_codelets[@]}"
do
  NAMEARRAY+=("$var")
  python3 "$ROOT_NODE_DIR"/codelets/"$var"/codelet.py  &
  PIDARRAY+=($!)
done

#run redis if pertinent on a port equal to the node server +1
if [ -z ${memory+x} ]
  then
    #echo "redis is true"
    #echo "${memory[redis]}"
    echo "${active_codelets[@]}"
    if [ "${memory[redis]}" = true ]
      then
        echo "redis is true"
        echo "${SERVER_IPS[0]}"
        #$ IFS=: read -r ip port <<< "${SERVER_IPS[0]}"
        port=$(echo "${SERVER_IPS[0]}" | cut -f 2 -d ":")
        redis-server --port "$(($port + 1))"
    fi
fi


# create memories if pertinent
#./create_memories.sh "${active_codelets[@]}"


# periodically check the health
while [[ "${signals["suicide_note"]}" == "false" ]]
do
  unset active_codelets
  unset signals
  eval "$(< "$ROOT_NODE_DIR"/param.ini python3 /usr/src/app/dct/parser.py)"
  #eval "$(< "$ROOT_NODE_DIR"/param.ini python3 "$ROOT_NODE_DIR"/parser.py)"
  check_integrity
  check_codelets
  sleep 10 #check every 10 secs
done

