#!/usr/bin/env zsh
set -euo pipefail

# Creates a virtual environment in `src/.venv` and installs requirements
VENV_DIR=".venv"
PY=python3

if ! command -v $PY >/dev/null 2>&1; then
  echo "Error: $PY not found. Install Python 3 (https://www.python.org/) and try again." >&2
  exit 1
fi

echo "Creating virtual environment at $PWD/$VENV_DIR..."
$PY -m venv "$VENV_DIR"

echo "Activating virtual environment and upgrading packaging tools..."
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip setuptools wheel

if [ -f requirements.txt ] && [ -s requirements.txt ]; then
  echo "Installing dependencies from requirements.txt..."
  pip install -r requirements.txt
else
  echo "No dependencies to install (requirements.txt missing or empty)."
fi

echo "Done. To activate the venv, run:"
echo "  source $VENV_DIR/bin/activate"
