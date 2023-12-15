#!/bin/bash
./xpilots -map .maps/simpleEdit.xp -switchBase 1 -maxRoundTime 30 &
python3 ./bots/baseline.py &
python3 ./dcnn/simpleAgent.py
