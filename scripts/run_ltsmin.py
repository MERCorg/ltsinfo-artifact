#!/usr/bin/env python

import argparse
import json
import os
from pathlib import Path
import re
import shutil
from library import run_experiment

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

BEGIN_PREPROCESS_REGEX = re.compile(r"ltsmin-reduce, (\d*\.\d*): input has .*")
BEGIN_TIMING_REGEX = re.compile(
    r"ltsmin-reduce, (\d*\.\d*): size after tau cycle elimination is .*"
)
END_TIMING_REGEX = re.compile(r"ltsmin-reduce, (\d*\.\d*): reduced LTS has .*")


def main():
    # Parse some configuration options
    parser = argparse.ArgumentParser(
        prog="run_ltsmin.py",
        epilog="",
    )

    parser.add_argument(
        dest="lts_dir",
        type=str,
        default="lts",
        help="Directory that contains the LTS files to benchmark",
    )

    parser.add_argument(
        dest="ltsmin_binpath", action="store", type=str
    )
    parser.add_argument(
        dest="num-runs", action="store", type=int,
        help="Number of runs to execute",
    )

    args = parser.parse_args()
    os.environ["PATH"] = args.ltsmin_binpath.strip() + os.pathsep + os.environ["PATH"]
    ltsmin_exe = shutil.which("ltsmin-reduce")

    for run in range(1, args.runs + 1):
        for alg in ["branching-bisim"]:
            os.makedirs(os.path.join(SCRIPT_PATH, f"ltsmin_{alg}"), exist_ok=True)

            for file in args.lts_dir.glob("*.aut"):
                print(f"Run {run}: Benchmarking {file} with ltsmin_reduce {alg}")
                (output, time, memory) = run_experiment(
                    [
                        ltsmin_exe,
                        "-b",
                        "-v",
                        "--stats",
                        "--when",
                        os.path.join(SCRIPT_PATH, "lts", file),
                        os.path.join(SCRIPT_PATH, f"ltsmin_{alg}", file),
                    ]
                )
                run_result = {
                    "total_time": time,
                    "memory": memory,
                    "output": output,
                }

                begin_preprocess = None
                begin_time = None
                end_time = None
                for line in output:
                    result = BEGIN_TIMING_REGEX.match(line)
                    if result is not None:
                        begin_time = float(result.group(1))

                    result = BEGIN_PREPROCESS_REGEX.match(line)
                    if result is not None:
                        begin_preprocess = float(result.group(1))

                    result = END_TIMING_REGEX.match(line)
                    if result is not None:
                        end_time = float(result.group(1))

                if end_time is None or begin_preprocess is None:
                    run_result["preprocess"] = float("nan")
                    run_result["reduction"] = float("nan")
                else:
                    if begin_time is None:
                        run_result["preprocess"] = 0.0
                        run_result["reduction"] = end_time - begin_preprocess
                    else:
                        run_result["preprocess"] = begin_time - begin_preprocess
                        run_result["reduction"] = end_time - begin_time

                print(run_result)
                result = {}
                result[file] = run_result

                # Add run number suffix to the result file name
                with open(
                    os.path.join("results", f"ltsmin_{alg}.json"),
                    "a",
                    encoding="utf-8",
                ) as json_file:
                    json.dump(result, json_file)


if __name__ == "__main__":
    main()
