#!/bin/sh
# Collect sosreport and other interesting logs when boot is complete.
#
# Copyright 2017 Canonical Ltd.
# Joshua Powers <josh.powers@canonical.com>
set -ux

while [ ! -e /var/lib/cloud/instance/boot-finished ]; do
    echo "Boot NOT finished, sleeping 3"
    sleep 3
done

LOG_DIR="$HOME/logs/boot/$(date +%s)"

if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
fi

cp /var/log/cloud-init.log "$LOG_DIR/cloud-init.log"
cp /var/log/cloud-init-output.log "$LOG_DIR/cloud-init-output.log"
cp /run/cloud-init/result.json "$LOG_DIR/cloud-init-result.json"
cp /run/cloud-init/status.json "$LOG_DIR/cloud-init-status.json"
cp /run/cloud-init/cloud.cfg "$LOG_DIR/cloud-init-cloud.cfg"
cp /run/cloud-init/ds-identify.log "$LOG_DIR/cloud-init-ds-identify.log"

systemd-analyze time | tee "$LOG_DIR/systemd_$(date +%s).log"
systemd-analyze blame --no-pager | tee "$LOG_DIR/systemd_blame.log"
systemd-analyze critical-chain --no-pager | tee "$LOG_DIR/systemd_chain.log"

# vi: ts=4 noexpandtab
