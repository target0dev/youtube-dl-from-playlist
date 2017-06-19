#!/bin/bash
if [ -z $2 ]; then
	echo "[-] Error. USAGE: ./runThis.sh [YOUTUBE PLAYLIST ID] [SOURCE 1 or 2]"
	exit
fi

opt1="downloadFrom-onlinevideoconverter.com.py"
opt2="downloadFrom-youtubeinmp4.com.py"

if (( $2 == 1 )); then 
	sourcedownloader=$opt1
elif (( $2 == 2 )); then
	sourcedownloader=$opt2
else
	echo "[-] Error. USAGE: ./runThis.sh [YOUTUBE PLAYLIST ID] [SOURCE 1 or 2]"
	exit
fi 

#generate random seed
#echo "Seed generation, please wait."
#rand1 = $RANDOM
#sleep 1
#rand2 = $RANDOM
#sleep 1
#randseed = $(( $(( rand1 * rand2 )) % RANDOM ))
#echo "[i] Randomseed: " randseed;

#start state, we have a playlist id
YTPLID=$1
echo "[i] Start state, we have a playlist id $YTPLID" 
pwd
echo

#we translate the playlist id into xls or table format and output into a download list
echo "[i] We translate the playlist id into xls or table format and output into a download list"
YTPLID_urllist="./working/$YTPLID-urllist"
python p2xls-williamsportwebdeveloper.com.py "$YTPLID"
if [ ! -f $YTPLID_urllist ]; then
	echo "[-] Problem, cannot find $YTPLID_urllist"
	exit
fi
echo "[+] $YTPLID_urllist created"
pwd
echo


#we then split the file into number of jobs that we want to run parallelly
echo "[i] We then split the file into number of jobs that we want to run parallelly"
./splitjobs.sh 3 "$YTPLID_urllist" 
if (( $(ls "$YTPLID_urllist"-* | wc -l) < 1 )); then
	echo "[-] Problem, cannot find job files"
	exit
fi
echo "[+] Job files created"
ls "$YTPLID_urllist"-*
pwd
echo

#exit #safety tag, remove before use


#we then run the jobs parallel
echo "[i] We then run the jobs parallel" 
#WARNING: ASYNC
./runparalleljob.sh "$YTPLID_urllist" "python ./$sourcedownloader" 
if (( $(ls ./result/*.mp4 | wc -l) < 1 )); then
	echo $(ls ./result/*.mp4 | wc -l)
	echo "[-] Problem, cannot find any mp4 files"
	exit
fi
pwd
echo

#cleans the file to avoid protocol errors
./cleansename.sh
pwd
echo

