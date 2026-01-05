# Overview

This is the artifact for TACAS 2026 paper.

  > Jan J. Martens and Maurice Laveaux. Faster Signature Refinement for Branching Bisimilarity Minimization. TACAS 2026.

The artifact is provided on Zenodo, and can be downloaded from the following link:

  > 10.5281/zenodo.17858373

In the artifact.zip we provide a Dockerfile, requiring the
[Docker](https://www.docker.com/) tool, for the artifact that builds `mCRL2`,
`ltsmin`, and `ltsinfo` from source, and contains the benchmark scripts.

## Preparation

Every labelled transition system (LTS) in the `lts/` directory, which must be in
the `.aut` format, will be used as input for the experiments. For the paper we
used the VLTS benchmark suite, which cannot be shared directly due to licensing, 
but we provide instructions on how to acquire it. Note, that this does require a valid
license for the CADP toolset.

## Smoke test

For the smoke test it should be sufficient to build the docker image using the
following command (from within the artifact directory):

```bash
    docker build .
```

We also provide a prebuilt docker file as `ltsinfo_artifact.tar` that can simply
be loaded using the following command, and requires no further internet access
except for acquiring the VLTS benchmark suite:

```bash
    docker image load -i ltsinfo_artifact.tar
```

The minimal run should take about 20 minutes, and running the experiments should
take about 1 hour. After the run the `/root/results/` directory should only
contain json files for each of the experiments.

## Tested on
We have tested the artifact on Windows, restricting Docker to 8GB of memory with
(`-m8GB`) on x86_64, and on macOS arm64.

## Badges
We apply for the available, functional and reusable badges.