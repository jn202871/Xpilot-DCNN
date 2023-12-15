#!/bin/bash
./xpilots -map .maps/lifeless.xp -switchBase 1 -maxRoundTime 30 -roundsToPlay 250 &
python3 ./bots/baseline.py &
python3 ./dcnn/lifelessAgent.py
