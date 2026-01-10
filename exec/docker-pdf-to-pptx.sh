#!/usr/bin/env bash
# Docker wrapper for pdf_to_pptx.sh
# This script executes PDF to PPTX conversion inside a Docker container
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 input.pdf output.pptx" >&2
  exit 2
fi

PDF_PATH="$1"
PPTX_PATH="$2"

# Convert paths to container paths
CONTAINER_PDF="/app/assets/$(basename "$PDF_PATH")"
CONTAINER_PPTX="/app/assets/$(basename "$PPTX_PATH")"

docker-compose run --rm immerculate /app/scripts/bash/pdf_to_pptx.sh "$CONTAINER_PDF" "$CONTAINER_PPTX"
