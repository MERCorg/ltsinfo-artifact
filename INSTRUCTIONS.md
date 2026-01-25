# Preparing the artifact

Initialize the git submodules:

```bash
git submodule update --init --recursive
```

Apply the mCRL2 patch to the mCRL2 toolset:

```bash
cd mCRL2
git apply ../mcrl2.patch
cd ..
```

Then follow the instructions in the [README](README.md) to build the Docker
image, after which the self-contained docker can be built using:

```bash
docker save ltsinfo_artifact -o ltsinfo_artifact.tar
```

The artifact should contain `README.md`, `Dockerfile` and `.dockerignore` files,
the `ltsinfo`, `ltsmin`, and `mCRL2` source code, the `scripts/` directory, and
the `lts/` directory with the mCRL2 case LTSs (in .aut format). An empty
`results/` directory should also be present to store the output of the
experiments.