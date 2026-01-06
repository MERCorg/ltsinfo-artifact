# Overview

This is the artifact for TACAS 2026 paper.

  > Jan J. Martens and Maurice Laveaux. Faster Signature Refinement for Branching Bisimilarity Minimization. TACAS 2026.

We compare the efficiency of branching bisimulation for three different implementations:
    - [ltsinfo](https://github.com/MERCorg/ltsinfo): Our new implementation described in the paper.
    - [mCRL2](https://github.com/mCRL2org/mCRL2): The existing implementation in the mCRL2 toolset.
    - [ltsmin](https://github.com/utwente-fmt/ltsmin): The existing implementation in the LTSmin toolset.

The artifact uses [Docker](https://www.docker.com/) to run the experiments in a
reproducible environment. The artifact consists of the following parts:

- A `Dockerfile` that builds the required tools from source, and generates the examples from the paper.
- A set of Python `scripts` to run the experiments and collect the results.
- The documentation for the tool, in the `docs/ltsinfo/ltsinfo/index.html` directory.
- A copy of the VLTS webpage in `docs/The VLTS Benchmark Suite.html/` for reference.

## Preparation

For the paper we have used the labelled transition systems of the
[VLTS](https://cadp.inria.fr/resources/vlts/) benchmark suite. They can be
downloaded from the website by clicking the names of the LTSs. A copy of the
website is provided in `docs`. The LTSs are provided in compressed `.bcg.bz2`
format, and should be stored in the `lts/` directory.

Afterwards, we require a valid installation for the CADP toolset to convert the
LTSs to the `.aut` format, a license and download can be requested from the CADP
website [here](https://cadp.inria.fr/registration/).

The `.bcg.bz2` files can be converted to `.aut` format using the provided
`convert.py` script in the `scripts/` directory. Set the `CADP` environment
variable to point to your CADP installation before running the conversion
script:

 > CADP=<installation_path> python scripts/convert.py ./lts

Alternatively, preconverted `.aut` files can be found in another
[artifact](https://doi.org/10.6084/m9.figshare.11876688). They are in the
`artifact/experiments/benchmarks` directory, and can be copied into the `lts/`
directory.

## Running the experiments

The experiments can be run using Docker. First build the docker image using the
following command (from within the artifact directory):

```bash
    docker build -t ltsinfo_artifact .
```

This should take about 20 minutes. Afterwards, we mount the `lts/` directory
containing the `.aut` files, and the results directory to store the output. This
can be done using the following command:

```bash
  docker run -it --mount type=bind,src=./lts/,dst=/root/lts/ --mount type=bind,src=./results/,dst=/root/results/ ltsinfo_artifact
``` 

Within the docker container, the experiments can be run using the provided
scripts. The following commands will run each of the three tools on all LTSs in
the `/root/lts/` directory, using 5 repetitions for each LTS, and store the
results in the `/root/results/` directory:

```bash
  python3 /root/scripts/run_ltsinfo.py /root/lts/ /root/ltsinfo/target/release/ 5 /root/results/
  python3 /root/scripts/run_ltsmin.py /root/lts/ /root/ltsmin/src/ltsmin-reduce/ 5 /root/results/
  python3 /root/scripts/run_mcrl2.py /root/lts/ /root/mCRL2/build/stage/bin/ 5 /root/results/
```

Each script will produce a separate JSON file in the results directory, containing
the results for that tool. Furthermore, the `.aut` files after reduction are output into
the results directory as well.

## Reusable

The artifact contains the source code of `ltsinfo`, `ltsmin`, and `mCRL2`, a