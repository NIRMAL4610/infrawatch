#!/bin/bash

python -m src.infrawatch.monitor &
MONITOR_PID=$!

gunicorn --bind 0.0.0.0:5000 src.infrawatch.api:app &
API_PID=$!

wait $MONITOR_PID $API_PID
