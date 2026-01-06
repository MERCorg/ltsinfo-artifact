#!/usr/bin/env python3

import argparse
import bz2
import os
import shutil
import subprocess
import sys

from pathlib import Path

def main():
    """Simple script to unpack and convert all .bcg.bz2 files in the given directory."""

    args = argparse.ArgumentParser(description="Unpack .bcg.bz2 files in given directory")
    args.add_argument(
        dest="directory",
        type=Path,
        help="Directory containing .bcg.bz2 files to unpack and convert",
    )
    args = args.parse_args()

    if "CADP" not in os.environ:
        print("CADP environment variable not set; cannot find CADP tools", file=sys.stderr)
        sys.exit(1)
    
    bcg_io_bin = shutil.which("bcg_io", path=os.path.join(os.environ["CADP"], "bin.x64"))
    if bcg_io_bin is None:
        print("bcg_io tool not found in CADP bin directory", file=sys.stderr)
        sys.exit(1)

    for p in args.directory.glob("*.bz2"):
        print(f"Converting {p}")

        # Unpack the bz2 file
        out = p.with_name(p.name[:-4])  # strip trailing ".bz2"
        with bz2.open(p, "rb") as fin, out.open("wb") as fout:
            fout.write(fin.read())

    for p in args.directory.glob("*.bcg"):
        print(f"Converting {p} to .aut format")

        # Use CADP tools to convert to .aut format
        subprocess.run([bcg_io_bin, str(p), str(p.with_suffix(".aut"))], check=True)

        # Cleaning up
        print(f"Removing {p}")
        p.unlink()

if __name__ == "__main__":
    main()
