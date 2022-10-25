#!/bin/bash

ROOT_DIR="$1"

if [ -z "$ROOT_DIR" ]
  then
    echo "Please supply a root directory."
    exit 1
  else
    echo "Starting API with root directory $ROOT_DIR"
    python3 src/api.py "$ROOT_DIR"
fi

