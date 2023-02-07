#!/bin/bash
kill -9 `cat logs/save_pid.txt`
rm -r logs
mkdir logs
nohup python3 -u teleyoutube.py > logs/my.log 2>&1 &
echo $! > logs/save_pid.txt