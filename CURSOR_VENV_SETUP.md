# Cursor Virtual Environment Setup

This document explains how to ensure Cursor chat terminals have access to the Python virtual environment.

## The Problem

Cursor chat terminals may not automatically activate the virtual environment, which means:
- `python` and `pip` commands use the system Python instead of the venv
- Installed packages aren't accessible
- Import errors occur when running scripts

## Solutions

### Solution 1: Manual Activation (Recommended for Chat Terminals)

When using Cursor chat terminals, manually activate the venv before running commands:

```bash
source backend/venv/bin/activate
```

Or use the helper script:
```bash
source backend/activate.sh
```

### Solution 2: Use the Run Script

For running Python commands, use the `run.sh` script which automatically activates the venv:

```bash
# Run a Python script
./backend/run.sh python scripts/analyze_students.py

# Run uvicorn
./backend/run.sh uvicorn app.main:app --reload

# Run pip install
./backend/run.sh pip install -r requirements.txt
```

### Solution 3: Explicit Python Path

Use the full path to the venv Python:

```bash
# Instead of: python script.py
backend/venv/bin/python script.py

# Instead of: pip install package
backend/venv/bin/pip install package
```

### Solution 4: VS Code/Cursor Settings

The workspace is configured in `.vscode/settings.json` to:
- Use the venv Python interpreter for the editor
- Auto-activate venv in integrated terminals

**Note:** Cursor chat terminals may not respect these settings. Use Solution 1 or 2 for chat terminals.

## Verifying the Virtual Environment

Check if the venv is active:
```bash
which python
# Should show: /path/to/guten-vocab/backend/venv/bin/python

echo $VIRTUAL_ENV
# Should show: /path/to/guten-vocab/backend/venv
```

## Quick Reference

```bash
# Activate venv
source backend/venv/bin/activate

# Deactivate venv
deactivate

# Check if active
which python

# Install dependencies
pip install -r backend/requirements.txt

# Run FastAPI app
cd backend && uvicorn app.main:app --reload
```

