# ltsinfo-artifact
The TACAS 2026 artifact for the paper "Faster Signature Refinement for Branching Bisimilarity Minimization"


We compare the efficiency of branching bisimulation for three different implementations:
    - [ltsinfo](https://github.com/MERCorg/ltsinfo): Our new implementation described in the paper.
    - [mCRL2](https://github.com/mCRL2org/mCRL2): The existing implementation in the mCRL2 toolset.
    - [ltsmin](https://github.com/utwente-fmt/ltsmin): The existing implementation in the LTSmin toolset.

The labelled transition systems are derived from the Very Large Transition Systems ([VLTS](https://cadp.inria.fr/resources/vlts/)) benchmark suite, which contains modelsfrom various sources. THese have been converted from the `.bcg` format to the `.aut` format using the [bcg2lts](