# Number of states from input
#
# Create an LTS with N (input variable) states and a complete transition relation with the "a" label, and a "b" label only s_i -b-> s_{i+1}.
# Print as .aut file format.
# Usage: python gen_example_B.py N
#
# Create an LTS
# Argparse N
import sys

args = sys.argv[1:]
N = int(args[0])
lts = [[0, "i", 0]]

# Add states
for i in range(N):
    for j in range(N):
        if j < i:
            lts.append((j, "a", i))

# Set initial state
print("des (0, {}, {})".format(len(lts), N))
print("\n".join(["({},{},{})".format(s, l, t) for s, l, t in lts]))
# Print the LTS
