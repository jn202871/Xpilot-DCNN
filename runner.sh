#!/bin/bash
x=1
while true
do
	x=$(( $x + 1 ))
	echo "Starting Run $x"
	timeout -s SIGKILL 10m python3 ./img_processing/expert.py >/dev/null 2>&1 &
	timeout -s SIGKILL 10m python3 ./img_processing/expert2.py >/dev/null 2>&1 &
	wait
done
