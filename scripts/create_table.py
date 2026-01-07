import argparse
import math
import os
import json
from pathlib import Path
import re


def print_gb(value):
    return float(value) / 1024 / 1024


def average(timings: list[float]) -> float:
    """ Compute the average solving time in milliseconds from a list of timing results. """
    total = 0.0

    for result in timings:
        total += result

    return total / len(timings)


def print_escaped(value: str) -> str:
    return value.replace("_", "\\_")


def print_result(value: float) -> str:
    if math.isnan(value):
        return "\\timeout"

    return f"{value:.1f}"


def print_memory(value: float) -> str:
    if math.isnan(value):
        return "\\timeout"

    return f"{print_gb(value)}"


def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split("([0-9]+)", key)]
    return sorted(l, key=alphanum_key)

def read_results(filename: str) -> dict:

    results = {}
    
    with open(filename, "r", encoding="utf-8") as json_file:
        # Read line by line and parse each line as JSON
        for line in json_file:
            json_data = json.loads(line)

            name = json_data["experiment"]
            if name not in results:
                results[name] = {
                    "total_time": [json_data["total_time"]],
                    "reduction": [json_data["reduction"]]
                }
            else:
                # Append to the existing data.
                results[name]["total_time"].append(json_data["total_time"])
                results[name]["reduction"].append(json_data["reduction"])
                    
    return results

def main():
    parser = argparse.ArgumentParser(
        prog="create_table.py",
        description="Print JSON output as a LaTeX table",
        epilog="",
    )

    parser.add_argument(
        "input", action="store", type=str
    )

    args = parser.parse_args()

    mcrl2_results = read_results(os.path.join(args.input, "mcrl2_branching-bisim.json"))
    ltsmin_results = read_results(os.path.join(args.input, "ltsmin_branching-bisim.json"))
    ltsinfo_results = read_results(os.path.join(args.input, "ltsinfo_branching-bisim.json"))

    # Read all the benchmark names.
    benchmarks = []
    for benchmark, _ in ltsinfo_results.items():
        benchmarks.append(benchmark)

    benchmarks = natural_sort(benchmarks)

    print("\\begin{tabular}{r || r | r || r | r | r || r | r | r}")
    print(
        "\\multicolumn{1}{c||}{} & \\multicolumn{3}{c||}{Total time (\\textbf{s})} & \\multicolumn{3}{c||}{Reduction time (\\textbf{s})}\\\\"
    )
    print("\\hline")

    outer_first = True
    for benchmark in benchmarks:
        # Get the values for comparison
        total_times = [
            average(mcrl2_results.get(benchmark, {}).get("total_time", float("NaN"))),
            average(ltsmin_results.get(benchmark, {}).get("total_time", float("NaN"))),
            average(ltsinfo_results.get(benchmark, {}).get("total_time", float("NaN"))),
        ]
        if not outer_first:
            print(" \\\\")
        outer_first = False

        minimum_index = min(
            range(len(total_times)),
            key=lambda i: total_times[i]
            if not math.isnan(total_times[i])
            else float("inf"),
        )
        first = True
        for i, result in enumerate(total_times):
            if not first:
                print(" & ", end="")
            first = False

            if i == minimum_index:
                print(f"\\textbf{{{print_result(result)}}}", end="")
            else:
                print(f"{print_result(result)}", end="")

        print(" & ", end="")
        reduction_times = [
            average(mcrl2_results.get(benchmark, {}).get("reduction", float("NaN"))),
            average(ltsmin_results.get(benchmark, {}).get("reduction", float("NaN"))),
            average(ltsinfo_results.get(benchmark, {}).get("reduction", float("NaN"))),
        ]

        minimum_index = min(
            range(len(reduction_times)),
            key=lambda i: reduction_times[i]
            if not math.isnan(reduction_times[i])
            else float("inf"),
        )
        first = True
        for i, result in enumerate(reduction_times):
            if not first:
                print(" & ", end="")
            first = False

            if i == minimum_index:
                print(f"\\textbf{{{print_result(result)}}}", end="")
            else:
                print(f"{print_result(result)}", end="")

    print("")
    print("\\end{tabular}")


if __name__ == "__main__":
    main()
