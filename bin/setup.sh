#!/bin/bash
# Do the basic stuff I always do when first testing
#
# Copyright 2017 Canonical Ltd.
# Joshua Powers <josh.powers@canonical.com>
set -ux

./install-depends.sh
./collect-logs.sh
./run-systemd-analyze.sh
