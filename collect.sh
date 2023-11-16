#!/bin/bash
./xpilots -map .maps/lifeless.xp -switchBase 1 -maxRoundTime 30 &
python3 ./bots/baseline.py &
python3 ./img_processing/fuzzyCollector.py 
