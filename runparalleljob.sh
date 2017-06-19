#!/bin/bash

if [ -z $2 ]; then
	echo "[-] USAGE: ./runparalleljob.sh [JOB COLLECTION PREFIX] [COMMAND]"
	exit
fi

jobCollection=$1
_cmd=$2
echo "[i] Querying job collection: $jobCollection"
echo "[i] Querying command: $_cmd"
for file in $(ls "$jobCollection"-*); do
	while read line; do
		eval "$_cmd $line"
	done < $file & 
done 
wait
#async escape
while true; do
	if (( $(ps -x | grep "$_cmd" | grep -v grep | grep -v 'runparalleljob.sh' | wc -l) < 1 )); then
		break
	fi
	sleep 1
done

echo "Parallel Done"
