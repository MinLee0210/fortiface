#!/bin/bash

# Load environment variables from .env file
if [ -f ".env" ]; then
    export $(cat .env | xargs)
else
    echo ".env file not found!"
    exit 1
fi

# Check if MILVUS_HOST and MILVUS_PORT are set
if [ -z "$MILVUS_HOST" ] || [ -z "$MILVUS_PORT" ]; then
    echo "MILVUS_HOST or MILVUS_PORT is not set in the .env file."
    exit 1
fi

# Concatenate MILVUS_URI
MILVUS_URI="$MILVUS_HOST:$MILVUS_PORT"

echo "Starting ATTU with Milvus URI: $MILVUS_URI"

# Run ATTU Docker container
docker run --rm -it\
    -p $MILVUS_ATTU:$MILVUS_ATTU \
    -e MILVUS_URL=$MILVUS_URI \
    -e ATTU_LOG_LEVEL=info  \
    zilliz/attu:latest

if [ $? -eq 0 ]; then
    echo "ATTU is running at: $MILVUS_HOST:$MILVUS_ATTU"
else
    echo "Failed to start ATTU."
    exit 1
fi