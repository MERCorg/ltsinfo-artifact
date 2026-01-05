#!/usr/bin/env python

import argparse
import json
import os
from pathlib import Path
import re
import shutil
from library import run_experiment

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

TIMING_REGEX = re.compile(r"Time reduction: (\d*\.\d*)s.*")
SCC_REGEX = re.compile(r"Time scc_reduce: (\d*\.\d*)s.*")
QUOTIENT_REGEX = re.compile(r"Time quotient: (\d*\.\d*)s.*")
PREPROCESS_REGEX = re.compile(r"Time preprocess: (\d*\.\d*)s.*")


def main():
    # Parse some configuration options
    parser = argparse.ArgumentParser(
        prog="run_mcrl2rust.py",
        epilog="",
    )

    parser.add_argument(
        dest="lts_dir",
        type=Path,
        default="lts",
        help="Directory that contains the LTS files to benchmark",
    )
    parser.add_argument(dest="ltsinfo_binpath", action="store", type=str)
    parser.add_argument(
        dest="num_runs",
        action="store",
        type=int,
        default=1,
        help="Number of runs to perform for each benchmark",
    )
    parser.add_argument(dest="output_dir", action="store", type=Path)

    args = parser.parse_args()
    os.environ["PATH"] = args.ltsinfo_binpath.strip() + os.pathsep + os.environ["PATH"]
    ltsinfo_exe = shutil.which("ltsinfo")

    for alg in ["branching-bisim"]:
        # Time the Rust implementation.
        os.makedirs(os.path.join(args.output_dir, f"ltsinfo_{alg}"), exist_ok=True)

        for run in range(0, args.num_runs):
            for file in args.lts_dir.glob("*.aut"):
                print(f"Run {run}: Benchmarking {file} with ltsinfo {alg}")
                (output, time, memory) = run_experiment(
                    [
                        ltsinfo_exe,
                        alg,
                        "--tau=i",
                        "--time",
                        os.path.join(SCRIPT_PATH, "lts", file),
                        os.path.join(args.output_dir, f"ltsinfo_{alg}", file),
                    ]
                )
                run_result = {"total_time": time, "memory": memory, "output": output}

                for line in output:
                    result = TIMING_REGEX.match(line)
                    if result is not None:
                        time = float(result.group(1))
                        run_result["reduction"] = time

                    result = SCC_REGEX.match(line)
                    if result is not None:
                        time = float(result.group(1))
                        run_result["scc_time"] = time

                    result = QUOTIENT_REGEX.match(line)
                    if result is not None:
                        time = float(result.group(1))
                        run_result["quotient_time"] = time

                    result = PREPROCESS_REGEX.match(line)
                    if result is not None:
                        time = float(result.group(1))
                        run_result["preprocess_time"] = time

                print(run_result)

                # Add run number suffix to the result file name
                with open(
                    os.path.join(args.output_dir, f"ltsinfo_{alg}.json"),
                    "a",
                    encoding="utf-8",
                ) as json_file:
                    json.dump(run_result, json_file)


if __name__ == "__main__":
    main()
