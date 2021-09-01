#!/bin/bash

distparams=(COB ALP JAL KOL NPR SPR HGL HOW MUR WMI BNK BIS NAD EBW WBW KLP DRJ UDJ DDJ EMI MLD BIR PUR RAM JHA)
logs=(cobout.txt alpout.txt jalout.txt kolout.txt nprout.txt sprout.txt hglout.txt howout.txt murout.txt wmiout.txt bnkout.txt bisout.txt nadout.txt ebwout.txt wbwout.txt klpout.txt drjout.txt udjout.txt ddjout.txt emiout.txt mldout.txt birout.txt purout.txt ramout.txt jhaout.txt)

#distparams=(KOL NPR SPR)
#logs=(kolout.txt nprout.txt sprout.txt)

i=0
for dist in "${distparams[@]}"
do
	logfileurl="/home/ubuntu/out/${logs[$i]}"
	nohup python3 cowinv3.py $dist &>> $logfileurl &
	echo "$dist script started. Log file location $logfileurl"
	i=$((i + 1))
	sleep 7
done
