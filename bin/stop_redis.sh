#!/bin/bash
if [ -f .redis.pid ]; then
    PID=$(cat .redis.pid)
    echo "Stopping Redis (PID $PID)..."
    kill $PID
    rm .redis.pid
    echo "Redis stopped."
else
    echo "No .redis.pid file found."
fi
