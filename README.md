# Overview

This is the artifact for the TACAS 2026 paper.

> Jan J.M. Martens and Maurice Laveaux. Faster Signature Refinement for Branching Bisimilarity Minimization. TACAS 2026.

We compare the efficiency of branching bisimulation minimization for three different implementations:
- [ltsinfo](https://github.com/MERCorg/ltsinfo): Our new implementation described in the paper.
- [mCRL2](https://github.com/mCRL2org/mCRL2): The existing implementation in the mCRL2 toolset.
- [ltsmin](https://github.com/utwente-fmt/ltsmin): The existing implementation in the LTSmin toolset.

The artifact uses [Docker](https://www.docker.com/) to run the experiments in a reproducible environment. The artifact consists of the following parts:

- A `Dockerfile` that builds the required tools from source.
- A set of Python `scripts` to run the experiments and collect the results.
- The documentation for the tool, in the `docs/ltsinfo/ltsinfo/index.html` directory.
- A copy of the VLTS webpage in `docs/The VLTS Benchmark Suite.html` for reference.

## Acquiring the benchmark suite

For the paper, we used the labelled transition systems of the
[VLTS](https://cadp.inria.fr/resources/vlts/) benchmark suite. They can be
downloaded from the website by clicking the names of the LTSs. A copy of the
website is provided in `docs`. The LTSs are provided in compressed `.bcg.bz2`
format and should be stored in the `lts/` directory.

You also need a valid installation of the CADP toolset to convert the LTSs to the `.aut` format. A license and download can be requested from the CADP website [here](https://cadp.inria.fr/registration/).

The `.bcg.bz2` files can be converted to `.aut` format using the provided
`convert.py` script in the `scripts/` directory. Set the `CADP` environment
variable to point to your CADP installation before running the conversion
script:

> CADP=<installation_path> python scripts/convert.py ./lts

Alternatively, preconverted `.aut` files can be found in another
[artifact](https://doi.org/10.6084/m9.figshare.11876688). They are in the
`artifact/experiments/benchmarks` directory and can be copied into the `lts/`
directory. From this we only use the `01_` to `32_` LTSs, since they correspond
to the LTSs in the VLTS benchmark suite.

## Preparing the experiments

The experiments can be run using Docker. First build the Docker image using the
following command (from within the artifact directory):

```bash
docker build -t ltsinfo_artifact .
```

This should take about 20 minutes. Alternatively, we provide a prebuilt image
`ltsinfo_artifact.tar`, which can be loaded using the following command:

```bash
docker image load -i ltsinfo_artifact.tar
```

Afterward, mount the `lts/` directory containing the `.aut` files and the
`results/` directory to store the output. This can be done using the following
command:

```bash
docker run -it --mount type=bind,src=./lts/,dst=/root/lts/ --mount type=bind,src=./results/,dst=/root/results/ ltsinfo_artifact
```

First, generate the example LTSs used in the paper using the provided script; they should appear in the `lts` directory on the host:

```bash
python3 /root/scripts/generate_examples.py /root/lts/
```

## Running the experiments

While still in the Docker container (from the run command above), run the
experiments using the provided scripts. The following commands will run each
of the three tools on all LTSs in the `lts` directory, using 5 repetitions for
each LTS, and store the results in the `results` directory:

```bash
python3 /root/scripts/run_ltsinfo.py /root/lts/ /root/ltsinfo/target/release/ 5 /root/results/
python3 /root/scripts/run_ltsmin.py /root/lts/ /root/ltsmin/src/ltsmin-reduce/ 5 /root/results/
python3 /root/scripts/run_mcrl2.py /root/lts/ /root/mCRL2/build/stage/bin/ 5 /root/results/
```

Each script will produce a separate JSON file in the results directory, containing
the results for that tool. Furthermore, the `.aut` files after reduction are
also output into the results directory. The full run takes about 2 hours.

Afterward, a LaTeX table can be created using the corresponding script:

```bash
python3 scripts/create_table.py /root/results/
```

We have also included a `verify_results.py` script to verify that all tools
produce the same minimized LTS. It can be run as follows:

```bash
python3 scripts/verify_results.py /root/mCRL2/build/stage/bin/ /root/results/ltsinfo_branching-bisim /root/results/mcrl2_branching-bisim
```

And similarly for `ltsmin_branching-bisim`.

## Reusable

The artifact contains the source code of the `ltsinfo`, `ltsmin`, and `mCRL2` tools, and the API documentation produced by rustdoc for `ltsinfo`. Our reduction algorithm is implemented in `ltsinfo/crates/reduction/src`. The `ltsinfo` tool also contains an earlier implementation of branching bisimulation minimization as option `branching-bisim-naive`, which implements inductive signatures without the optimizations described in the paper. However, in practice, it turned out that this implementation is also fairly efficient compared to the existing tools.

Continued development of the tool takes place in the
[MERC](https://github.com/MERCorg/merc) repository, where it is named
`merc-lts`. A generic `LTS` trait is used to decouple the reduction algorithms
from the underlying LTS storage format.