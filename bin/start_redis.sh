#!/bin/bash
# Start a Redis server using Singularity

PORT=${1:-6379}
DATADIR=$(pwd)/.redis_data
mkdir -p "$DATADIR"

echo "Starting Redis on port $PORT..."
echo "Data directory: $DATADIR"

# Run redis-server in the background using the official docker image
singularity run --bind "$DATADIR:/data" docker://redis:alpine redis-server --port $PORT --dir /data --save 60 1 &
REDIS_PID=$!
echo $REDIS_PID > .redis.pid

echo "Redis server started with PID $REDIS_PID."
