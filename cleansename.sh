#!/bin/bash

ls ./result/*.mp4 > tmpfilename
while read filename; do 
	mv "$filename" "$(echo $filename | tr -d ':' | tr -d '?' | tr -d '\"' | tr -d '\|')"
done < tmpfilename
rm tmpfilename
