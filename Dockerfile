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
# Required to unpack the LTSs
 bzip2 
 
# Build mCRL2 from source
COPY ./mCRL2 /root/mCRL2/

# Configure build
RUN mkdir ~/mCRL2/build && cd ~/mCRL2/build && cmake . \
 -DCMAKE_BUILD_TYPE=RELEASE \
 -DMCRL2_ENABLE_GUI_TOOLS=OFF \
 -DMCRL2_PACKAGE_RELEASE=ON \
 ~/mCRL2

# Build the toolset and install it such that the tools are available on the PATH
ARG THREADS=8
RUN cd ~/mCRL2/build && make -j${THREADS} ltsconvert

# Build ltsmin from source
COPY ./ltsmin /root/ltsmin/

# Build the ltsmin toolset.
RUN cd ~/ltsmin \
    && ./ltsminreconf \
    && ./configure --disable-dependency-tracking \
    && cd ~/ltsmin \
    && make -j${THREADS}

# Install Rust for building ltsinfo
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Build ltsinfo from source
COPY ./ltsinfo /root/ltsinfo/

ARG THREADS=8
ENV PATH="/root/.cargo/bin:${PATH}"
RUN cd ~/ltsinfo/ \
    && cargo build --release -j${THREADS}

# Copy the LTSs into the container
COPY ./lts/ /root/lts/

# Copy the scripts
COPY ./scripts/ /root/scripts/
RUN scripts/unpack.sh