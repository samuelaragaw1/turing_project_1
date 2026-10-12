#!/bin/bash
# Oracle solution wrapper for hill-instability-tongues
set -e
cp /solution/solver.py /root/solver/solver.py
python3 /root/solver/solver.py /root/data/input.json /root/result/tongues.json
