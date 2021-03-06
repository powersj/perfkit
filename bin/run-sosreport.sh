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

LOG_DIR="$HOME/logs/sosreport/$(date +%s)"

if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
fi

TEMP_D=$(mktemp -d) ||
    fail "failed to make tempdir"
sudo sosreport --build --batch --quiet --tmp-dir "$TEMP_D"

# Custom modifications to sosreport output that will delete any socket and
# charachter files to avoid errors on tar as well as make sure all files
# are readable as well owned by the user and not root.
sudo chown -R "$USER":"$USER" "$TEMP_D"
chmod -R u+r "$TEMP_D"
find "$TEMP_D" -type s -delete
find "$TEMP_D" -type c -delete
report=$(basename "$(find "$TEMP_D" -mindepth 1 -maxdepth 1 -type d)")
tar --create --file - --directory="$TEMP_D" . |
    xz -c - > "$LOG_DIR"/"$report".tar.xz
rm -rf "$TEMP_D"
