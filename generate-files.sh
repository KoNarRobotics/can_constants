#!/bin/bash

SCRIPT_PATH=$(dirname "$(readlink -f "$0")")
cd $SCRIPT_PATH

if [[ "$1" == "-v" ]]; then
  echo "Creating virtual environment"
  python3 -m venv .venv
  source .venv/bin/activate
fi


python3 -m pip install -r requirements.txt
cd can_messages
python3 generator.py