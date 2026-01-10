# Python environment for this folder

This directory contains a small helper to create an isolated Python environment inside `src/.venv` and keep dependencies local to the folder.

Quick start

1. From the repo root run:

```bash
cd src
./setup_env.sh
```

2. Activate the virtual environment:

```bash
source .venv/bin/activate
```

3. Add any pip dependencies to `requirements.txt` (one per line) and run the setup script again to install them.

Notes
- The virtual environment is created at `src/.venv` so dependencies are kept inside the folder.
- The root `.gitignore` includes `src/.venv` so the venv is not committed.
