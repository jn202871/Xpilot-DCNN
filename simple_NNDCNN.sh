#!/bin/bash
./xpilots -map .maps/simpleEdit.xp -switchBase 1 -maxRoundTime 30 >/dev/null 2>&1 &
python3 ./dcnn/simpleAgentNN.py &
cd ./bots/neuralNetBot
java -Djava.library.path="/lib/xpilot-ai/binaries/" NeuralHelp >/dev/null 2>&1
