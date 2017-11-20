#!/bin/bash
# Disable proposed for apt
#
# Copyright 2017 Canonical Ltd.
# Joshua Powers <josh.powers@canonical.com>
set -eux

sudo rm /etc/apt/sources.list.d/proposed.list
sudo apt-get update

# vi: ts=4 noexpandtab
