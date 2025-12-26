#!/usr/bin/env python3

import argparse
import subprocess
import os

def generate_example(script_name: str, output_file: str, size: int):
    """Generates the example LTSs"""

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Run the script and capture its output
    output_file = f"{output_file}_{size}.aut"
    with open(output_file, "w", encoding="utf-8") as f:
        print(f"Generating {output_file} using {script_name}")

        subprocess.run(
            ["python", script_name, str(size)],
            stdout=f,
            stderr=subprocess.STDOUT,
            check=True,
        )


def main():
    """Main function to generate all examples with varying sizes."""

    args = argparse.ArgumentParser(
        description="Generate example LTSs with varying sizes"
    )
    args.add_argument(
        dest="output_dir",
        type=str,
        default="lts",
        help="Directory to store generated LTS files",
    )
    args = args.parse_args()


    for size in [10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000]:
        generate_example("gen_example_A.py", f"{args.output_dir}/example_A", size)

    for size in [1000, 1500, 2000, 2500, 3000]:
        generate_example("gen_example_B.py", f"{args.output_dir}/example_B", size)
    for size in [16, 20, 24, 28, 32]:
        generate_example("gen_example_fib.py", f"{args.output_dir}/example_fib", size)


if __name__ == "__main__":
    main()
