#!/bin/bash
set -e
pytest --json-report --json-report-file=/root/result/test-report.json test_tongues.py -v
