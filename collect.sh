#!/bin/bash
./xpilots -map .maps/simpleEdit.xp -switchBase 1 -maxRoundTime 30 &
python3 ./img_processing/expertBot.py &
python3 ./img_processing/expertBot2.py
