# Define base image
FROM ubuntu:14.04

# Install required packages
RUN apt-get update && apt-get install -y \
	wget \
	tar \
	make \
	libncurses5-dev \
	zlib1g-dev \
	build-essential \
    -qq \
    bzip2 \
    gcc \
    g++
# Change workdir
WORKDIR /opt

# cwllib req
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:jonathonf/python-3.6 -y
RUN apt-get update
RUN apt-get install python3.6 -y
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.6 get-pip.py
RUN rm -rf get-pip.py
RUN python3.6 -m pip install --upgrade pip setuptools wheel
RUN pip3.6 install dill
# End of cwllib req

RUN apt-get install -y python

# Install Strelka
RUN wget https://github.com/Illumina/strelka/releases/download/v2.9.7/strelka-2.9.7.release_src.tar.bz2
RUN tar -xjf strelka-2.9.7.release_src.tar.bz2
RUN mkdir build
WORKDIR /opt/build
RUN ../strelka-2.9.7.release_src/configure --jobs=4 --prefix=/opt
RUN make -j4 install

WORKDIR /opt

COPY Dockerfile /opt/
MAINTAINER Gavrilo Andric, Seven Bridges, <gavrilo.andric@sbgenomics.com>

