# Number of states from input
#
# Create an LTS with N (input variable that is hard for ltsmin, but easy for the
# new signature refinement algorithms.
#  Usage: python gen.py N
#
# Create an LTS
# Argparse N
import sys

args = sys.argv[1:]
N = int(args[0])
lts = [[0, "i", 0]]

# Add states
for j in range(N):
    lts.append((0, "a", j))

for j in range(N):
    lts.append((1, "a", j))

for i in range(N - 1):
    lts.append((i, "b", i + 1))

# Set initial state
print("des (0, {}, {})".format(len(lts), N))
print("\n".join(["({},{},{})".format(s, l, t) for s, l, t in lts]))
# Print the LTS
