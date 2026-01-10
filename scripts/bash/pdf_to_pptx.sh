#!/usr/bin/env bash
set -euo pipefail

# Usage: pdf_to_pptx.sh input.pdf output.pptx
# Requires: pdftoppm (poppler) and python (with python-pptx installed in venv)

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 input.pdf output.pptx" >&2
  exit 2
fi

PDF="$1"
OUT_PPTX="$2"

if [ ! -f "$PDF" ]; then
  echo "Input PDF not found: $PDF" >&2
  exit 1
fi

if ! command -v pdftoppm >/dev/null 2>&1; then
  echo "pdftoppm not found. Install poppler (e.g. brew install poppler)." >&2
  exit 3
fi

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

echo "Rendering PDF to images in $TMPDIR..."
pdftoppm -png "$PDF" "$TMPDIR/page" >/dev/null

# Collect images in sorted order
IMAGES=("$TMPDIR"/page-*.png)
if [ ${#IMAGES[@]} -eq 0 ]; then
  echo "No images produced from PDF." >&2
  exit 4
fi

echo "Building PPTX from images..."
python3 src/pdf_images_to_pptx.py "$OUT_PPTX" "$TMPDIR"

echo "Wrote $OUT_PPTX"
