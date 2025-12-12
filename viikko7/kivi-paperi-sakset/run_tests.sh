#!/bin/bash
# Simple script to run tests

cd "$(dirname "$0")/src" || exit 1
python -m pytest test_app.py -v
