import math
import os
import json
import re
import subprocess

def print_gb(value):
    return float(value) / 1024 / 1024

def combine(left: dict, right: dict) -> None:    
    for key, value in left.items():
        for k, v in value.items():
            value[k] = v + right[key][k]

def average(results: dict, number_of_inputs: int) -> None:
    for _, value in results.items():
        for k, v in value.items():
            if isinstance(v, (int, float)):
                value[k] = v / number_of_inputs

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
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

    def extract_states(line: str) -> int:
        return 0

def ltsinfo(filename: str) -> tuple[int, int]:
    # Run ltsinfo on the given filename
    result = subprocess.run(['ltsinfo', filename], 
                            capture_output=True, text=True, check=True)
    
    # Parse the output to extract number of states and transitions
    states = 0
    transitions = 0
    
    for line in result.stderr.splitlines():
        match = re.search(r'Number of states:\s*(\d+)', line)
        if match:
            states = int(match.group(1))
        
        match = re.search(r'Number of transitions:\s*(\d+)', line)
        if match:
            transitions = int(match.group(1))
    
    return (states, transitions)
        
def read_results(filename: str) -> dict:

    # Read all the JSON results starting with the given filename
    results = None
    num_of_results = 0
    for file in os.listdir("results"):
        if file.startswith(filename) and file.endswith(".json"):
            print(f"Reading {file}")
            with open(os.path.join("results", file), "r", encoding="utf-8") as json_file:
                result = json.load(json_file)
                num_of_results += 1
                if results is None:
                    results = result
                else:
                    combine(results, result)

    assert results is not None
    average(results, num_of_results)
    return results

def main():
    ltsconvert_results = read_results("ltsconvert_branching-bisim_")
    ltsmin_results = read_results("ltsmin_branching-bisim_")
    mcrl2rust_results = read_results("mcrl2rust_branching-bisim_")

    # Read all the benchmark names.
    benchmarks = []
    for benchmark, _ in mcrl2rust_results.items():
        # If the total time is less than 1 second for all results, ignore it.
        if ltsconvert_results[benchmark]['total_time'] < 1.0 and ltsmin_results[benchmark]['total_time'] < 1.0 and mcrl2rust_results[benchmark]['total_time'] < 1.0:
            continue
        
        benchmarks.append(benchmark)

    benchmarks = natural_sort(benchmarks)

    print("\\begin{tabular}{r || r | r || r | r | r || r | r | r}")
    print("\\multicolumn{1}{c||}{} & \\multicolumn{3}{c||}{Total time (\\textbf{s})} & \\multicolumn{3}{c||}{Reduction time (\\textbf{s})}\\\\")
    print("\\hline")
    
    outer_first = True
    for benchmark in benchmarks:
        # Get the values for comparison
        total_times = [
            ltsconvert_results.get(benchmark, {}).get('total_time', float('NaN')),
            ltsmin_results.get(benchmark, {}).get('total_time', float('NaN')),
            mcrl2rust_results.get(benchmark, {}).get('total_time', float('NaN'))
        ]
        if not outer_first:
            print(' \\\\')
        outer_first = False

        # Find the minimum valid (non-NaN) values     
        (states, transitions) = ltsinfo("lts/" + benchmark)
        print(f"{print_escaped(benchmark)} & {states} & {transitions} & ", end="")   

        minimum_index = min(range(len(total_times)), key=lambda i: total_times[i] if not math.isnan(total_times[i]) else float('inf'))
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
            ltsconvert_results.get(benchmark, {}).get('reduction', float('NaN')),
            ltsmin_results.get(benchmark, {}).get('reduction', float('NaN')),
            mcrl2rust_results.get(benchmark, {}).get('reduction', float('NaN'))
        ]

        minimum_index = min(range(len(reduction_times)), key=lambda i: reduction_times[i] if not math.isnan(reduction_times[i]) else float('inf'))
        first = True
        for i, result in enumerate(reduction_times):
            if not first:
                print(" & ", end="")
            first = False

            if i == minimum_index:
                print(f"\\textbf{{{print_result(result)}}}", end="")
            else:
                print(f"{print_result(result)}", end="")


    print('')
    print("\\end{tabular}")

if __name__ == "__main__":
    main()
