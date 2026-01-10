#!/usr/bin/env bash
# Start Colima with appropriate settings for this project
set -euo pipefail

echo "Starting Colima..."

# Check if Colima is already running
if colima status >/dev/null 2>&1; then
    echo "✓ Colima is already running"
    colima status
    exit 0
fi

# Start Colima with reasonable defaults
# Adjust CPU, memory, and disk as needed for your system
colima start \
    --cpu 2 \
    --memory 4 \
    --disk 20 \
    --arch x86_64 \
    --vm-type=vz

echo ""
echo "✓ Colima started successfully"
echo ""
echo "Next steps:"
echo "  1. Build the Docker image: make build"
echo "  2. Run tests: make test"
echo "  3. Use scripts in exec/ folder"
