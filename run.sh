#!/bin/bash
cd /home/roman/.gemini/antigravity/scratch/tomv2
export PYTHONPATH="/home/roman/.local/lib/python3.12/site-packages:$PYTHONPATH"

# Load .env file if exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

python3 ai_computer_assistant.py "$@"