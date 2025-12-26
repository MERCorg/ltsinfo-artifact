#!/usr/bin/env python3

import argparse
import bz2
import sys
from pathlib import Path

def main():
    """Simple script to unpack all .lts.bz2 files in /root/lts."""

    args = argparse.ArgumentParser(description="Unpack .lts.bz2 files in given directory")
    args.add_argument(
        dest="directory",
        type=Path,
        default=Path("/root/lts"),
        help="Directory containing .lts.bz2 files to unpack",
    )
    args = args.parse_args()

    for p in args.directory.glob("*.aut.bz2"):
        print(f"Unpacking {p}")
        try:
            out = p.with_name(p.name[:-4])  # strip trailing ".bz2"
            with bz2.open(p, "rb") as fin, out.open("wb") as fout:
                fout.write(fin.read())
        except Exception as e:
            print(f"Error unpacking {p}: {e}", file=sys.stderr)

        # Cleaning up
        print(f"Removing {p}")
        p.unlink()

if __name__ == "__main__":
    main()
