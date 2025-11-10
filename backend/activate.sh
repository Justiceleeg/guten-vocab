#!/bin/bash
# Helper script to activate the virtual environment
# Usage: source backend/activate.sh

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SCRIPT_DIR/venv/bin/activate"
echo "✓ Virtual environment activated: $VIRTUAL_ENV"
echo "✓ Python: $(which python)"
echo "✓ Pip: $(which pip)"

