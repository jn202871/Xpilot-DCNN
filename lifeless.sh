#!/bin/bash
./xpilots -map .maps/lifeless.xp -switchBase 1 -maxRoundTime 30 -roundsToPlay 250 >/dev/null 2>&1 &
python3 ./bots/baseline.py >/dev/null 2>&1 &
python3 ./dcnn/lifelessAgent.py
