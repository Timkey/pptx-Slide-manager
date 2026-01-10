#!/usr/bin/env python3
"""Interactive entry point to select a merge strategy.

Options:
  1) Template-based merge (use an existing PPTX as base/master)
  2) Image-based merge (render slides to images, then compose)
  3) Clone-based merge (best-effort cloning)

The script will prompt for required arguments and then run the chosen
executable script.
"""
import os
import shlex
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS = {
    "1": os.path.join(ROOT, "src", "merge_template.py"),
    "2": os.path.join(ROOT, "src", "merge_images.py"),
    "3": os.path.join(ROOT, "src", "merge_clone.py"),
}


def prompt(msg):
    try:
        return input(msg)
    except EOFError:
        return ""


def run_script(script, args):
    cmd = [sys.executable, script] + args
    print("Running:", shlex.join(cmd))
    subprocess.run(cmd)


def main():
    print("Choose merge strategy:\n 1) Template-based (use a PPTX as base)\n 2) Image-based (render slides to images)\n 3) Clone-based (best-effort clone)")
    choice = prompt("Enter 1, 2 or 3: ").strip()
    if choice not in SCRIPTS:
        print("Invalid choice")
        sys.exit(1)

    script = SCRIPTS[choice]
    if choice == "1":
        output = prompt("Output filename (e.g. final.pptx): ").strip()
        tmpl = prompt("Template/master PPTX (or leave empty to use first input): ").strip()
        inputs = prompt("Space-separated input PPTX files: ").strip()
        args = [output]
        if tmpl:
            args += ["-t", tmpl]
        args += inputs.split()
    else:
        output = prompt("Output filename (e.g. final.pptx): ").strip()
        inputs = prompt("Space-separated input PPTX files: ").strip()
        args = [output] + inputs.split()

    run_script(script, args)


if __name__ == "__main__":
    main()
