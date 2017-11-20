#!/bin/bash
# Install dependencies for testing.
#
# Copyright 2017 Canonical Ltd.
# Joshua Powers <josh.powers@canonical.com>
set -eux

PACKAGES=(
    fio
    mdadm
    netperf
    stress-ng
)

sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y "${PACKAGES[@]}"

# vi: ts=4 noexpandtab
