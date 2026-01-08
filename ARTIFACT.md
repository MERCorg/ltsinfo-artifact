# Overview

This is the artifact for the TACAS 2026 paper.

  > Jan J.M. Martens and Maurice Laveaux. Faster Signature Refinement for Branching Bisimilarity Minimization. TACAS 2026.

The artifact is provided on Zenodo and can be downloaded from the following link:

  > 10.5281/zenodo.17858373

The `artifact.zip` includes a Dockerfile, which requires
[Docker](https://www.docker.com/) to be installed. The image builds `mCRL2`,
`ltsmin`, and `ltsinfo` from source, and contains the benchmark scripts.

## Preparation

Every labelled transition system (LTS) in the `lts/` directory, which must be in
the `.aut` format, will be used as input for the experiments. For the paper, we
used the VLTS benchmark suite, which cannot be shared directly due to licensing,
but we provide instructions on how to acquire it. Note that using this
benchmark set requires a valid license for the CADP toolset, which must also be
acquired separately.

## Smoke test

For the smoke test, it should be sufficient to run the preparation steps in `README.md`
and then run the experiments without acquiring the full VLTS benchmark set.

## Tested on

We tested the artifact on x86_64 Windows and Linux (Docker limited to 8GB with
`-m8GB`). Note that `ltsmin` does not compile on macOS arm64, but the Docker
image can still be built with the `--platform linux/amd64` option.

## Badges

We are applying for the available, functional, and reusable badges.
