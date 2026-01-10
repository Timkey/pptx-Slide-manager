#!/usr/bin/env python3
"""Merge using a template/master as base. This script wraps the existing
`merge_pptx.py` merge_presentations function and provides a simpler CLI
for the template-based workflow.

Usage:
  python3 src/merge_template.py output.pptx -t template.pptx input1.pptx input2.pptx ...
If `-t` is not provided but inputs are given, the first input will be used
as the base (as before).
"""
import argparse
import os
import sys
from merge_pptx import merge_presentations


def main():
    p = argparse.ArgumentParser(description="Template-based PPTX merge")
    p.add_argument("output", help="Output filename (written to assets/slides/merged)")
    p.add_argument("inputs", nargs="*", help="Input PPTX files to merge")
    p.add_argument("-t", "--template", help="Template/master PPTX to use as base")
    args = p.parse_args()

    # Build input_files list consistent with merge_pptx expectations
    input_files = args.inputs or []
    if args.template:
        # Prepend template so merged is initialized from it and the script
        # will skip copying its slides (no duplication)
        input_files = [args.template] + input_files

    # Resolve output path to assets/slides/merged
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    merged_dir = os.path.join(root, "assets", "slides", "merged")
    os.makedirs(merged_dir, exist_ok=True)
    output_path = os.path.join(merged_dir, args.output)

    if not input_files:
        print("No input files provided. Provide inputs or use templates directory.")
        sys.exit(1)

    merge_presentations(output_path, input_files)


if __name__ == "__main__":
    main()
