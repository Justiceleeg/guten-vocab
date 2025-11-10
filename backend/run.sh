#!/bin/bash
# Helper script to run Python commands with the virtual environment
# Usage: ./backend/run.sh python script.py
#        ./backend/run.sh uvicorn app.main:app --reload

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SCRIPT_DIR/venv/bin/activate"
exec "$@"

