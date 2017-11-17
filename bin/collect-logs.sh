#!/bin/sh
# Collect sosreport when boot is complete.
#
# Copyright 2017 Canonical Ltd.
# Joshua Powers <josh.powers@canonical.com>
set -eux

LOG_DIR="$HOME/logs/"

while [ ! -e /var/lib/cloud/instance/boot-finished ]; do
    echo "Boot NOT finished, sleeping 3"
    sleep 3
done

if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
fi

# sosreport-HOSTNAME-YYYYMMDDHHMMSS.tar.xz
sudo sosreport --batch --quiet --tmp-dir="$LOG_DIR"

# Logs specific to this boot
LOG_DIR="$HOME/logs/$(date +%s)"

cp /var/log/cloud-init.log "$LOG_DIR/cloud-init.log"
cp /var/log/cloud-init-output.log "$LOG_DIR/cloud-init-output.log"
systemd-analyze time | tee "$LOG_DIR/systemd_time.log"
systemd-analyze blame --no-pager | tee "$LOG_DIR/systemd_blame.log"
systemd-analyze critical-chain --no-pager | tee "$LOG_DIR/systemd_chain.log"
