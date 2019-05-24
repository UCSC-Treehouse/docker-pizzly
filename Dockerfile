FROM ubuntu:18.04

MAINTAINER Jacob Pfeil, jpfeil@ucsc.edu

# Update and install required software
RUN apt-get update --fix-missing

RUN apt-get install -y build-essential \
                       wget \
                       software-properties-common \
                       seqan-dev \
                       zlib1g-dev \
                       apt-utils \
                       libpthread-stubs0-dev \
                       cmake

RUN wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O ~/miniconda.sh
RUN bash ~/miniconda.sh -b -p $HOME/miniconda

ENV PATH=/root/miniconda/bin:$PATH

RUN conda update -y conda

RUN conda install -y -c bioconda pizzly

WORKDIR /opt

RUN wget -qO- https://github.com/pmelsted/pizzly/archive/v0.37.3.tar.gz | tar xz

# Add wrapper scripts
COPY pipeline /opt/pipeline

# Data processing occurs at /data
WORKDIR /data

ENTRYPOINT ["python", "/opt/pipeline/run.py"]
