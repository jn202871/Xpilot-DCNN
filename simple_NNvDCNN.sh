#!/bin/bash
./xpilots -map .maps/simpleEdit.xp -switchBase 1 -maxRoundTime 30 &
python3 ./dcnn/simpleAgent.py &
cd ./bots/neuralNetBot
java -Djava.library.path="/lib/xpilot-ai/binaries/" NeuralHelp
