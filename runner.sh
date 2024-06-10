#!/bin/bash
cp ./dcnn/models/modelstate_MAIN_0.1231.pt ./dcnn/models/retrain/retrained.pt
rm data.txt
python3 ./dcnn/clear.py >/dev/null 2>&1
for i in {1..10}; do
	echo "Starting Run"
	timeout 25m python3 ./img_processing/expert.py $i >/dev/null 2>&1 &
	timeout 25m python3 ./dcnn/lifelessretrain.py $i >/dev/null 2>&1 &
	wait
	echo "Parsing Run Data"
	python3 parse.py
	rm data.txt
	echo "Cleared Raw Data"
	echo "Retraining"
	python3 ./dcnn/dcnnretrain.py
	python3 ./dcnn/clear.py
	echo "Cleared SQL Data"
done
for i in {11..20}; do
	echo "Starting Run"
	timeout 25m python3 ./img_processing/fuzzyCollector.py $i >/dev/null 2>&1 &
	timeout 25m python3 ./dcnn/lifelessretrain.py $i >/dev/null 2>&1 &
	wait
	echo "Parsing Run Data"
	python3 parse.py
	rm data.txt
	echo "Cleared Raw Data"
	echo "Retraining"
	python3 ./dcnn/dcnnretrain.py
	python3 ./dcnn/clear.py
	echo "Cleared SQL Data"
done
for i in {21..30}; do
	echo "Starting Run"
	timeout 25m python3 ./img_processing/expert.py $i >/dev/null 2>&1 &
	timeout 25m python3 ./dcnn/lifelessretrain.py $i >/dev/null 2>&1 &
	wait
	echo "Parsing Run Data"
	python3 parse.py
	rm data.txt
	echo "Cleared Raw Data"
	echo "Retraining"
	python3 ./dcnn/dcnnretrain.py
	python3 ./dcnn/clear.py
	echo "Cleared SQL Data"
done
for i in {31..40}; do
	echo "Starting Run"
	timeout 25m python3 ./img_processing/fuzzyCollector.py $i >/dev/null 2>&1 &
	timeout 25m python3 ./dcnn/lifelessretrain.py $i >/dev/null 2>&1 &
	wait
	echo "Parsing Run Data"
	python3 parse.py
	rm data.txt
	echo "Cleared Raw Data"
	echo "Retraining"
	python3 ./dcnn/dcnnretrain.py
	python3 ./dcnn/clear.py
	echo "Cleared SQL Data"
done
