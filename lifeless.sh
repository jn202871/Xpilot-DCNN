#!/bin/bash
./xpilots -map .maps/lifeless.xp -switchBase 1 -maxRoundTime 30 -roundsToPlay 1 >/dev/null 2>&1 &
python3 ./bots/expert.py >/dev/null 2>&1 &
#python3 ./dcnn/lifelessretrain.py &
python3 ./dcnn/lifelessAgent.py &
#python3 ./img_processing/fuzzyCollector.py
#python3 ./img_processing/expert.py
#python3 ./bots/expert2.py
