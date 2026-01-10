#!/usr/bin/env bash
# Docker wrapper for pdf_to_images.sh
# This script executes PDF to images conversion inside a Docker container
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 input.pdf outdir" >&2
  exit 2
fi

PDF_PATH="$1"
OUT_DIR="$2"

# Convert paths to container paths
CONTAINER_PDF="/app/assets/$(basename "$PDF_PATH")"
CONTAINER_OUT="/app/assets/$(basename "$OUT_DIR")"

docker-compose run --rm immerculate /app/scripts/bash/pdf_to_images.sh "$CONTAINER_PDF" "$CONTAINER_OUT"
