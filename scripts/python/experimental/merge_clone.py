#!/usr/bin/env python3
"""Best-effort cloning merge: try to preserve formatting by deep-copying
slide XML and copying picture blobs when needed. This is an incremental
approach toward full package-level cloning.

Usage:
  python3 src/merge_clone.py output.pptx input1.pptx input2.pptx ...
"""
import argparse
import os
import sys
from merge_pptx import merge_presentations


def main():
    p = argparse.ArgumentParser(description="Best-effort clone merge (preserve formatting)")
    p.add_argument("output", help="Output filename (written to assets/slides/merged)")
    p.add_argument("inputs", nargs="+", help="Input PPTX files to merge")
    args = p.parse_args()

    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    merged_dir = os.path.join(root, "assets", "slides", "merged")
    os.makedirs(merged_dir, exist_ok=True)
    output_path = os.path.join(merged_dir, args.output)

    merge_presentations(output_path, args.inputs)


if __name__ == "__main__":
    main()
