#!/bin/bash
./xpilots -map .maps/lifeless.xp -switchBase 1 -maxRoundTime 30 &
python3 ./img_processing/ekkoCollect.py &
python3 ./img_processing/ekkoCollect2.py
