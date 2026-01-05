# Overview

This is the artifact for TACAS 2026 paper.

  > Jan J. Martens and Maurice Laveaux. Faster Signature Refinement for Branching Bisimilarity Minimization. TACAS 2026.

We compare the efficiency of branching bisimulation for three different implementations:
    - [ltsinfo](https://github.com/MERCorg/ltsinfo): Our new implementation described in the paper.
    - [mCRL2](https://github.com/mCRL2org/mCRL2): The existing implementation in the mCRL2 toolset.
    - [ltsmin](https://github.com/utwente-fmt/ltsmin): The existing implementation in the LTSmin toolset.

The artifact uses [Docker](https://www.docker.com/) to run the experiments in a
reproducible environment.

## Preparation

For the paper we have used the labelled transition systems of the
[VLTS](https://cadp.inria.fr/resources/vlts/) benchmark suite. They can be
downloaded from the website by clicking the names of the LTSs.

Afterwards, we require a valid installation for the CADP toolset to convert the
LTSs to the `.aut` format. Set the `CADP` environment variable to point to
your CADP installation before running the conversion script:

 > CADP=<installation_path> python scripts/convert.py ./lts

Alternatively, preconverted `.aut` files can be found in another [artifact](https://doi.org/10.6084/m9.figshare.11876688)

`artifact\experiments\benchmarks`

## Running the experiments

docker run -it --mount type=bind,src=./lts/,dst=/root/lts/ 


RUN python3 /root/scripts/run_ltsinfo.py /root/lts/ /root/ltsinfo/target/release/ 5 /root/results/
RUN python3 /root/scripts/run_ltsmin.py /root/lts/ /root/ltsmin/src/ltsmin-reduce/ 5 /root/results/
RUN python3 /root/scripts/run_mcrl2.py /root/lts/ /root/mCRL2/build/stage/bin/ 5 /root/results/


