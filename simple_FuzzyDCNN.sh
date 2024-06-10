#!/bin/bash
./xpilots -map .maps/simpleEdit.xp -switchBase 1 -maxRoundTime 30 -roundsToPlay 10 >/dev/null 2>&1 &
python3 ./dcnn/lifelessAgent.py &
python3 ./dcnn/lifelessAgent2.py
