#!/usr/bin/env bash
# Stop Colima
set -euo pipefail

echo "Stopping Colima..."
colima stop

echo "✓ Colima stopped"
