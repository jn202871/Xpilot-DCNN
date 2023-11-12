#!/bin/bash
xpilots -map .maps/lifeless.xp -switchBase 1 -roundsToPlay 10 -maxRoundTime 30 &
python3 ./bots/$1 >/dev/null 2>&1 &
python3 ./bots/$2 >/dev/null 2>&1 &
