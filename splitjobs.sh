#!/bin/bash

if [ -z $2 ]; then
	echo "[-] Usage: splitjobs.sh [number of tasks] [tasklist]"
	exit
fi

totaljobs=$1
tasklist=$2
totaltasks=$(cat "$tasklist" | wc -l)
totaltasksperjob=$(( totaltasks / totaljobs ))
nxtfilecounter=$(( totaltasksperjob + 1 ))
currentfilenumber=1
counter=1
while read line; do 
	#echo $currentfilenumber:$nxtfilecounter:$counter:$line
	echo $line >> "$tasklist"-"$currentfilenumber"
	counter=$(( counter + 1 ))
	if (( $counter > $nxtfilecounter )); then
		counter=1
		currentfilenumber=$(( currentfilenumber + 1 ))
	fi
done < "$tasklist"
