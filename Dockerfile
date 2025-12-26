FROM ubuntu:24.04

# Install dependencies
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
# Dependencies for mCRL2
 build-essential \
 cmake \
 git \
 libboost-dev \
 python3 \
 python3-pip \
 python3-psutil \ 
 z3 \
# Dependencies for ltsmin.
 ant \
 autoconf \
 automake \
 bison \
 diffutils \
 flex \
 file \
 libtool \
 pkgconf \
 libpopt-dev \
 zlib1g-dev \
# Requires to install Rust
 curl \
# Requires to fix the bash shebangs
 dos2unix
 
# Build mCRL2 from source
COPY ./mCRL2 /root/mCRL2/

# Configure build
RUN mkdir /root/mCRL2/build && cd /root/mCRL2/build && cmake . \
 -DCMAKE_BUILD_TYPE=RELEASE \
 -DMCRL2_ENABLE_GUI_TOOLS=OFF \
 -DMCRL2_PACKAGE_RELEASE=ON \
 /root/mCRL2

# Build the toolset and install it such that the tools are available on the PATH
ARG THREADS=8
RUN cd /root/mCRL2/build && make -j${THREADS} ltsconvert

# Build ltsmin from source
COPY ./ltsmin /root/ltsmin/

# Build the ltsmin toolset, we create an empty .git directory for the build system to be happy
RUN cd /root/ltsmin/ \
    && mkdir .git \
    && find . -type f -print0 | xargs -0 dos2unix \
    && ./ltsminreconf \
    && ./configure --disable-dependency-tracking

ARG THREADS=8
RUN cd /root/ltsmin \
    && make -j${THREADS}

# Install Rust for building ltsinfo
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Build ltsinfo from source
COPY ./ltsinfo /root/ltsinfo/

ARG THREADS=8
ENV PATH="/root/.cargo/bin:${PATH}"
RUN cd /root/ltsinfo/ \
    && cargo build --release -j${THREADS}

# Copy the LTSs into the container
COPY ./lts/ /root/lts/

# Copy the scripts
COPY ./scripts/ /root/scripts/

# Run the preparation scripts
RUN python3 /root/scripts/unpack.py /root/lts/
RUN python3 /root/scripts/generate_examples.py /root/lts/