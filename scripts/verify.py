import argparse
import os
import subprocess
import shutil

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))


def main():
    """Checks whether the reduced LTSs of the left and right directories are strongly bisimilar."""

    # Parse some configuration options
    parser = argparse.ArgumentParser(
        prog="check_results.py",
        epilog="",
    )

    parser.add_argument(dest="mcrl2_binpath", action="store", type=str)
    parser.add_argument("left", type=str)
    parser.add_argument("right", type=str)

    args = parser.parse_args()

    ltscompare_exe = shutil.which("ltscompare", path=args.mcrl2_binpath)

    for file in os.listdir(os.path.join(SCRIPT_PATH, args.left)):
        if ".aut" in file:
            print(f"Comparing {file}")
            result = subprocess.run(
                [
                    ltscompare_exe,
                    "-ebisim",
                    "--tau=i",
                    os.path.join(SCRIPT_PATH, args.left, file),
                    os.path.join(SCRIPT_PATH, args.right, file),
                ],
                stdout=subprocess.PIPE,
                check=True,
            )

            if "false" in result.stdout.decode("utf-8"):
                raise RuntimeError(f"File {file} is not bisimilar")


if __name__ == "__main__":
    main()
