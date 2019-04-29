#!/usr/bin/env bash

set -o errexit    # abort script at first error
set -o pipefail   # return the exit status of the last command in the pipe
set -o nounset    # treat unset variables and parameters as an error

apt-get update && apt-get dist-upgrade --assume-yes && apt-get install --assume-yes --no-install-recommends\
    bash \
    git \
    python3-minimal \
    python3-venv \
    python3-pip \
    python3-setuptools \
    locales \
    binutils \
    libproj-dev \
    gdal-bin \
    python3-dev \
    libpq-dev \
    gcc \
    liblz4-dev \
    build-essential
