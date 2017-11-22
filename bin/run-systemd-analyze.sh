#!/bin/sh
# Collect sosreport when boot is complete.
#
# Copyright 2017 Canonical Ltd.
# Joshua Powers <josh.powers@canonical.com>
set -eux

while [ ! -e /var/lib/cloud/instance/boot-finished ]; do
    echo "Boot NOT finished, sleeping 3"
    sleep 3
done

LOG_DIR="$HOME/logs/systemd-analyze"

if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
fi

systemd-analyze time | tee "$LOG_DIR/time-$(date +%s).log"

# vi: ts=4 noexpandtab
