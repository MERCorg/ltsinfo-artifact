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
 ant-lib \
 autoconf \
 automake \
 bison \
 diffutils \
 flex \
 file \
 libtool \
 libtool-ltdl-devel \
 pkgconf \
 popt-devel \
 zlib-devel \
# Requires to install Rust
 curl
 
# Build mCRL2 from source
COPY ./mCRL2 /root/mCRL2/

# Configure build
RUN mkdir ~/mCRL2/build && cd ~/mCRL2/build && cmake . \
 -DCMAKE_BUILD_TYPE=RELEASE \
 -DMCRL2_ENABLE_GUI_TOOLS=OFF \
 ~/mCRL2

# Build the toolset and install it such that the tools are available on the PATH
ARG THREADS=8
RUN cd ~/mCRL2/build && make -j${THREADS} && make install

# Build ltsmin from source
COPY ./ltsmin /root/ltsmin/

# Build the ltsmin toolset.
RUN cd ~/ltsmin \
    && ./ltsminreconf \
    && ./configure --disable-dependency-tracking \
    && cd ~/ltsmin \
    && make -j${THREADS} install

# Install Rust for building ltsinfo
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Build ltsinfo from source
COPY ./ltsinfo /root/ltsinfo/

RUN cd ~/ltsinfo/ \
    && cargo build --release

# Copy the LTSs into the container
COPY ./lts/ /root/lts/