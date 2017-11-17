#!/bin/sh
# Intalls the AWS Kernel via linux-image-aws and reboot.
#
# Copyright 2017 Canonical Ltd.
# Joshua Powers <josh.powers@canonical.com>
set -eux

sudo apt-get update
sudo apt-get install linux-image-aws -y
sudo shutdown -r now
