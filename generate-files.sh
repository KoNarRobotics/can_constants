#!/bin/bash

SCRIPT_PATH=$(dirname "$(readlink -f "$0")")
cd $SCRIPT_PATH
# python3 -m venv .venv
# source .venv/bin/activate
python3 -m pip install -r requirements.txt
cd can_messages
python3 generator.py