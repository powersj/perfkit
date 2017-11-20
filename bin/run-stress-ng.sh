#!/bin/bash
# Run basic stress-ng test.
#
# Copyright 2017 Canonical Ltd.
# Joshua Powers <josh.powers@canonical.com>
set -eux

CMD="stress-ng --matrix 0 --timeout 10m --metrics-brief --times"
LOG_DIR="$HOME/logs/stress-ng"

if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
fi

filename="$LOG_DIR/$(date +%s).log"
printf "%s\n%s\n" "$(date)" "$CMD" | tee "$filename"
$CMD | tee -a "$filename"

# vi: ts=4 noexpandtab
