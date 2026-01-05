#!/usr/bin/env python

import argparse
import json
import os
from pathlib import Path
import re
import shutil
from library import run_experiment

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

TIMING_REGEX = re.compile(r".*reduction: (\d*\.\d*)s.*")
SCC_REGEX = re.compile(r".*scc_reduce: (\d*\.\d*)s.*")
QUOTIENT_REGEX = re.compile(r".*quotient: (\d*\.\d*)s.*")
PREPROCESS_REGEX = re.compile(r".*preprocess: (\d*\.\d*)s.*")


def main():
    # Parse some configuration options
    parser = argparse.ArgumentParser(
        prog="run_mcrl2.py",
        epilog="",
    )
    parser.add_argument(
        dest="lts_dir",
        type=Path,
        default="lts",
        help="Directory that contains the LTS files to benchmark",
    )
    parser.add_argument(
        dest="ltsconvert_binpath", action="store", type=str, required=True
    )
    parser.add_argument(
        dest="runs",
        action="store",
        type=int,
        help="Number of runs to perform for each algorithm",
    )
    parser.add_argument(dest="output_dir", action="store", type=Path)

    args = parser.parse_args()
    ltsconvert_bin = shutil.which("ltsconvert", args.ltsconvert_binpath)

    for alg in ["branching-bisim"]:
        os.makedirs(os.path.join(args.output_dir, f"mcrl2_{alg}"), exist_ok=True)

        for run in range(1, args.runs):
            for file in args.lts_dir.glob("*.aut"):
                print(f"Run {run}: Benchmarking {file} with mcrl2 {alg}")
                (output, time, memory) = run_experiment(
                    [
                        ltsconvert_bin,
                        "-e",
                        alg,
                        "--tau=i",
                        "--timings",
                        os.path.join(SCRIPT_PATH, "lts", file),
                        os.path.join(args.output_dir, f"mcrl2_{alg}", file),
                    ]
                )
                run_result = {"file": str(file), "total_time": time, "memory": memory, "output": output}

                for line in output:
                    result = TIMING_REGEX.match(line)
                    if result is not None:
                        time = float(result.group(1))
                        run_result["reduction"] = time

                    result = SCC_REGEX.match(line)
                    if result is not None:
                        time = float(result.group(1))
                        run_result["scc_time"] = time

                    result = PREPROCESS_REGEX.match(line)
                    if result is not None:
                        time = float(result.group(1))
                        run_result["preprocess_time"] = time

                print(run_result)

                # writing the dictionary data into the corresponding JSON file
                with open(
                    os.path.join(args.output_dir, f"mcrl2_{alg}.json"),
                    "a",
                    encoding="utf-8",
                ) as json_file:
                    json.dump(run_result, json_file)


if __name__ == "__main__":
    main()
