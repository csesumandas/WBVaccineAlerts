#!/bin/bash
for pid in $(ps aux | grep cowinv2.py | awk '{print $2}')
do
    kill -9 $pid
    echo "Killed process $pid"
done