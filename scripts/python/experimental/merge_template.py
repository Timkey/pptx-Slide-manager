#!/usr/bin/env python3
"""Merge using a template/master as base. This script wraps the existing
`merge_pptx.py` merge_presentations function and provides a simpler CLI
for the template-based workflow.

Usage:
  python3 scripts/python/merge_template.py [output.pptx] -t template.pptx input1.pptx input2.pptx ...
If `-t` is not provided but inputs are given, the first input will be used
as the base (as before). Output filename is optional - auto-generates if omitted.
"""
import argparse
import os
import random
import sys
from merge_pptx import merge_presentations

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUTPUT_DIR = os.path.join(ROOT, "assets", "output", "merge_template")


def generate_output_filename(prefix="merged-template", extension=".pptx"):
    """Generate incremental filename in assets/output."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    counter = 1
    while True:
        filename = f"{prefix}-{counter:03d}{extension}"
        filepath = os.path.join(OUTPUT_DIR, filename)
        if not os.path.exists(filepath):
            return filepath
        counter += 1
        if counter > 999:
            filename = f"{prefix}-{random.randint(1000, 9999)}{extension}"
            return os.path.join(OUTPUT_DIR, filename)


def main():
    p = argparse.ArgumentParser(description="Template-based PPTX merge")
    p.add_argument("-o", "--output", help="Output filename (saved to assets/output). If omitted, auto-generates name.")
    p.add_argument("-t", "--template", help="Template/master PPTX to use as base")
    p.add_argument("inputs", nargs="*", help="Input PPTX files to merge")
    args = p.parse_args()

    # Build input_files list consistent with merge_pptx expectations
    input_files = args.inputs or []
    if args.template:
        # Prepend template so merged is initialized from it and the script
        # will skip copying its slides (no duplication)
        input_files = [args.template] + input_files

    # Generate output filename if not provided
    if args.output:
        output_path = os.path.join(OUTPUT_DIR, args.output)
    else:
        output_path = generate_output_filename("merged-template", ".pptx")

    if not input_files:
        print("No input files provided. Provide inputs or use templates directory.")
        sys.exit(1)

    merge_presentations(output_path, input_files)


if __name__ == "__main__":
    main()
