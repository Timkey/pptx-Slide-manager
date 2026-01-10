#!/usr/bin/env bash
set -euo pipefail

# Usage: merge_pdfs.sh output.pdf in1.pdf in2.pdf [...]
# Tries qpdf, pdfunite, then ghostscript to merge PDFs.

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 output.pdf in1.pdf [in2.pdf ...]" >&2
  exit 2
fi

OUT="$1"
shift
INPUTS=("$@")

if command -v qpdf >/dev/null 2>&1; then
  echo "Merging with qpdf..."
  qpdf --empty --pages "${INPUTS[@]}" -- "$OUT"
  exit 0
fi

if command -v pdfunite >/dev/null 2>&1; then
  echo "Merging with pdfunite..."
  pdfunite "${INPUTS[@]}" "$OUT"
  exit 0
fi

if command -v gs >/dev/null 2>&1; then
  echo "Merging with ghostscript (gs)..."
  gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile="$OUT" "${INPUTS[@]}"
  exit 0
fi

echo "No PDF merge tool found. Install qpdf (recommended) or poppler/pdfunite or ghostscript." >&2
echo "On macOS: brew install qpdf" >&2
exit 3
