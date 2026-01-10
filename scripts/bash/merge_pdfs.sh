#!/usr/bin/env bash
# Enhanced merge_pdfs.sh with auto-generated output names
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
OUTPUT_DIR="$ROOT_DIR/assets/output/merge_pdfs"
PDF_TEMPLATES_DIR="$ROOT_DIR/assets/pdfs/templates"

# Function to generate incremental filename
generate_filename() {
    local prefix="$1"
    local extension="$2"
    local counter=1
    
    mkdir -p "$OUTPUT_DIR"
    
    while true; do
        local filename=$(printf "%s-%03d%s" "$prefix" "$counter" "$extension")
        local filepath="$OUTPUT_DIR/$filename"
        
        if [ ! -f "$filepath" ]; then
            echo "$filepath"
            return 0
        fi
        
        counter=$((counter + 1))
        
        if [ $counter -gt 999 ]; then
            # Fallback to random
            filename="${prefix}-${RANDOM}${extension}"
            echo "$OUTPUT_DIR/$filename"
            return 0
        fi
    done
}

# Parse arguments
if [ "$#" -eq 0 ]; then
  # No arguments - merge all templates with auto-generated filename
  OUT=$(generate_filename "merged-pdf" ".pdf")
  INPUTS=("$PDF_TEMPLATES_DIR"/*.pdf)
  if [ ! -f "${INPUTS[0]}" ]; then
    echo "No PDF templates found in $PDF_TEMPLATES_DIR" >&2
    exit 1
  fi
elif [ "$#" -eq 1 ]; then
  # Single arg that could be template directory - use templates
  OUT=$(generate_filename "merged-pdf" ".pdf")
  INPUTS=("$PDF_TEMPLATES_DIR"/*.pdf)
  if [ ! -f "${INPUTS[0]}" ]; then
    echo "No PDF templates found in $PDF_TEMPLATES_DIR" >&2
    exit 1
  fi
elif [[ "$FIRST_ARG" == *.pdf ]] && [ -f "$FIRST_ARG" ]; then
  # First arg is existing file (input), auto-generate output
  OUT=$(generate_filename "merged-pdf" ".pdf")
  INPUTS=("$@")
else
  # First arg is output name
  if [[ "$FIRST_ARG" == */* ]]; then
    # Full path provided
    OUT="$FIRST_ARG"
  else
    # Just filename, put in output directory
    OUT="$OUTPUT_DIR/$FIRST_ARG"
  fi
  shift
  INPUTS=("$@")
  
  # If no inputs, use templates
  if [ "${#INPUTS[@]}" -eq 0 ]; then
    INPUTS=("$PDF_TEMPLATES_DIR"/*.pdf)
    if [ ! -f "${INPUTS[0]}" ]; then
      echo "No PDF templates found in $PDF_TEMPLATES_DIR" >&2
      exit 1
    fi
  fi
fi

# Ensure output directory exists
mkdir -p "$(dirname "$OUT")"

# Merge using available tool
if command -v qpdf >/dev/null 2>&1; then
  echo "Merging ${#INPUTS[@]} PDFs with qpdf..."
  qpdf --empty --pages "${INPUTS[@]}" -- "$OUT"
  echo "✓ Saved merged PDF to: $OUT"
  exit 0
fi

if command -v pdfunite >/dev/null 2>&1; then
  echo "Merging ${#INPUTS[@]} PDFs with pdfunite..."
  pdfunite "${INPUTS[@]}" "$OUT"
  echo "✓ Saved merged PDF to: $OUT"
  exit 0
fi

if command -v gs >/dev/null 2>&1; then
  echo "Merging ${#INPUTS[@]} PDFs with ghostscript (gs)..."
  gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile="$OUT" "${INPUTS[@]}"
  echo "✓ Saved merged PDF to: $OUT"
  exit 0
fi

echo "No PDF merge tool found. Install qpdf (recommended) or poppler/pdfunite or ghostscript." >&2
echo "On macOS: brew install qpdf" >&2
exit 3
