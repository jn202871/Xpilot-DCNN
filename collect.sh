#!/bin/bash
./xpilots -map .maps/simpleEdit.xp -switchBase 1 -maxRoundTime 30 &
python3 ./img_processing/fuzzyCollector2.py &
python3 ./img_processing/fuzzyCollector.py
