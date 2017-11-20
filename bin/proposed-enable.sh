#!/bin/bash
# Enable proposed for apt
#
# Copyright 2017 Canonical Ltd.
# Joshua Powers <josh.powers@canonical.com>
set -eux

RELEASE=$(lsb_release -c -s)

grep -E "deb .* $RELEASE main" /etc/apt/sources.list |
    sed "s/$RELEASE/$RELEASE-proposed/" > /tmp/proposed.list
sudo mv /tmp/proposed.list /etc/apt/sources.list.d/
sudo apt-get update

# vi: ts=4 noexpandtab
