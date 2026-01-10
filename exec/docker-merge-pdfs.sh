#!/usr/bin/env bash
# Docker wrapper for merge_pdfs.sh
# This script executes the PDF merge inside a Docker container
set -euo pipefail

# Convert local paths to container paths
ARGS=()
for arg in "$@"; do
    if [[ -f "$arg" ]] || [[ "$arg" == *.pdf ]]; then
        # Convert to relative path from project root for container
        ARGS+=("/app/assets/$(basename "$arg")")
    else
        ARGS+=("$arg")
    fi
done

docker-compose run --rm immerculate /app/scripts/bash/merge_pdfs.sh "${ARGS[@]}"
