#!/bin/bash
./xpilots -map .maps/simpleEdit.xp -switchBase 1 -maxRoundTime 30 >/dev/null 2>&1 &
python3 ./bots/baseline.py >/dev/null 2>&1 &
python3 ./dcnn/simpleAgent.py
