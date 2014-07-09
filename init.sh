#!/bin/bash

if [ "$PYTHON" == "" ]; then
    PYTHON="python"
fi

# Use embedded virtualenv
REAL=`python -c 'import os,sys;print os.path.realpath(sys.argv[1])' "$0"`
VIRTUALENV="$PYTHON $(dirname $REAL)/support/virtualenv.py"

if [ ! -e venv ]; then 
    echo "Initializing virtualenv folder (venv)"
    $VIRTUALENV --no-site-packages venv
fi

echo "Installing required libraries"
venv/bin/pip install -r requirements.txt
