#!/usr/bin/env bash
set -euo pipefail

# Usage: pptx_to_pdf.sh input.pptx output.pdf
# Converts a PPTX to PDF using LibreOffice (`soffice`) if available.

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 input.pptx output.pdf" >&2
  exit 2
fi

INPUT="$1"
OUTPUT="$2"

if [ ! -f "$INPUT" ]; then
  echo "Input file not found: $INPUT" >&2
  exit 1
fi

SOFFICE=""
if command -v soffice >/dev/null 2>&1; then
  SOFFICE=soffice
elif command -v libreoffice >/dev/null 2>&1; then
  SOFFICE=libreoffice
elif [ -x "/Applications/LibreOffice.app/Contents/MacOS/soffice" ]; then
  SOFFICE="/Applications/LibreOffice.app/Contents/MacOS/soffice"
fi

if [ -z "$SOFFICE" ]; then
  # Try to use Microsoft PowerPoint on macOS via AppleScript (osascript)
  if [ "$(uname)" = "Darwin" ]; then
    if /usr/bin/osascript -e 'id of application "Microsoft PowerPoint"' >/dev/null 2>&1; then
      echo "LibreOffice not found; will try Microsoft PowerPoint via AppleScript" >&2
      # Use AppleScript to open and save as PDF
      /usr/bin/osascript <<APPLESCRIPT
tell application "Microsoft PowerPoint"
  activate
  try
    set thePres to open POSIX file "$INPUT"
    save thePres in POSIX file "$OUTPUT" as save as PDF file format
    close thePres saving no
  on error errMsg
    -- propagate the error
    error errMsg
  end try
end tell
APPLESCRIPT
      exit $?
    else
      echo "Microsoft PowerPoint not found as an Apple application." >&2
    fi
  fi

  echo "LibreOffice (soffice) not found. Install LibreOffice or use another conversion method." >&2
  echo "On macOS you can: brew install --cask libreoffice" >&2
  exit 3
fi

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

echo "Converting $INPUT -> PDF using $SOFFICE" >&2
"$SOFFICE" --headless --convert-to pdf --outdir "$TMPDIR" "$INPUT" >/dev/null 2>&1

BASE=$(basename "$INPUT" .pptx)
GENPDF="$TMPDIR/${BASE}.pdf"
if [ ! -f "$GENPDF" ]; then
  # Sometimes extension case differs
  GENPDF=$(ls "$TMPDIR"/*.pdf 2>/dev/null | head -n1 || true)
fi

if [ -z "$GENPDF" ] || [ ! -f "$GENPDF" ]; then
  echo "Conversion failed; PDF not produced." >&2
  exit 4
fi

mv "$GENPDF" "$OUTPUT"
echo "Wrote $OUTPUT"
