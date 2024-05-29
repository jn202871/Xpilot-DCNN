#!/bin/bash
./xpilots -map .maps/lifeless.xp -switchBase 1 -maxRoundTime 30 &
#cd ./bots/neuralNetBot
#java -Djava.library.path="/lib/xpilot-ai/binaries/" NeuralHelp >/dev/null 2>&1
#java -Djava.library.path="/lib/xpilot-ai/binaries/" NeuralHelp2 >/dev/null 2>&1
python3 ./img_processing/expert.py >/dev/null 2>&1 &
python3 ./img_processing/expert2.py >/dev/null 2>&1 &
