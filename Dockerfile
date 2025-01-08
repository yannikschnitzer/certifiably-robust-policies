FROM --platform=linux/amd64 ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

# Update and install base dependencies
RUN apt-get update && \
    apt-get install -y \
        git \
        build-essential \
        sudo \
        software-properties-common \
        wget \
        zip \
        curl && \
    apt-get autoremove -y

# Install GNU make (gmake), GCC/G++ (C/C++ compilers)
RUN apt-get install -y make gcc g++

# Install Java Development Kit (JDK)
RUN apt-get install -y openjdk-21-jdk

# Add Python dependencies
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3-pip && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10 && \
    pip3 install --upgrade pip

# Clean up to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Create working directory
RUN mkdir TACAS25
WORKDIR /TACAS25

# Clone repository (replace <repo-url> with the actual repository URL)
RUN git clone https://github.com/yannikschnitzer/PRISM-updmps.git
WORKDIR /TACAS25/PRISM-updmps
RUN git checkout artifact_eval
WORKDIR /TACAS25/PRISM-updmps/PRISM


