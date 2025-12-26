# Number of states from input
#
# Create an LTS corresponding to the N'th fibonacci word.
# Print as .aut file format.
# Usage: python gen.py N
#
# Create an LTS
# Argparse N
import sys

args = sys.argv[1:]
N = int(args[0])

# We start with one silent transition so algorithms correctly use brnaching bisim
lts = [[0, "i", 0]]

fib = ["0", "01"]
# Add states
for i in range(N):
    fib.append(fib[-1] + fib[-2])

word = fib[-1]
for i in range(len(word)):
    lts.append([i, "a", (i + 1) % len(word)])
    if word[i] == "1":
        lts.append([i, "b", i])
    # For tau-hard example.

# for i in range(1,len(word)):
#   state = i + len(word)
#   lts.append([state, "i",state-1])

# Set initial state
print("des (0, {}, {})".format(len(lts), len(word) + 1))
print("\n".join(["({},{},{})".format(s, l, t) for s, l, t in lts]))
# Print the LTS
