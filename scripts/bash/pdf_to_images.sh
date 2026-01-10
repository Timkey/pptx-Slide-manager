#!/usr/bin/env bash
set -euo pipefail

# Usage: pdf_to_images.sh input.pdf outdir
# Requires poppler's pdftoppm on PATH (brew install poppler)

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 input.pdf outdir" >&2
  exit 2
fi

PDF="$1"
OUTDIR="$2"

if [ ! -f "$PDF" ]; then
  echo "Input PDF not found: $PDF" >&2
  exit 1
fi

if ! command -v pdftoppm >/dev/null 2>&1; then
  echo "pdftoppm not found. Install poppler (e.g. brew install poppler)." >&2
  exit 3
fi

mkdir -p "$OUTDIR"
echo "Converting PDF pages to PNG images in $OUTDIR..."
pdftoppm -png "$PDF" "$OUTDIR/page" >/dev/null
echo "Images written to $OUTDIR" 
