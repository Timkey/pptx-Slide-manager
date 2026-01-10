#!/usr/bin/env bash
# Docker wrapper for Python scripts
# Usage: ./docker-run-python.sh script_name.py [args...]
set -eo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 script_name.py [args...]" >&2
  echo "Example: $0 merge_pptx.py output.pptx input1.pptx input2.pptx" >&2
  exit 2
fi

SCRIPT="$1"
shift
ARGS=("$@")

# Convert file paths in arguments to container paths
CONTAINER_ARGS=()
for arg in "${ARGS[@]}"; do
    if [[ -f "$arg" ]] || [[ "$arg" == *.pptx ]] || [[ "$arg" == *.pdf ]] || [[ "$arg" == *.png ]]; then
        CONTAINER_ARGS+=("/app/assets/$(basename "$arg")")
    else
        CONTAINER_ARGS+=("$arg")
    fi
done

docker-compose run --rm immerculate python "/app/scripts/python/$SCRIPT" "${CONTAINER_ARGS[@]}"
