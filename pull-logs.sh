#!/bin/bash
# Collect logs directory from system under test.
#
# Copyright 2017 Canonical Ltd.
# Joshua Powers <josh.powers@canonical.com>
set -eu

PROJECT=${1:-''}
TARGET=${2:-''}

usage() {
    echo "usage:"
    echo "$0 project target-ip"
    echo "example:"
    echo "$0 cloud 127.0.0.1"
    exit 1
}

fail() {
    local msg=$1
    shift

    echo "$msg"
    exit 1
}

ssh_target(){
    local cmd=$1
    shift


    ssh ubuntu@"$TARGET" -- "$cmd"  # shellcheck disable=SC2059
}

[ $# -eq 2 ] || { echo "must provide 2 arguments"; usage; }

RELEASE=$(ssh_target "lsb_release -s -c")
KERNEL=$(ssh_target "uname -r | rev | cut -d'-' -f1 | rev")
LOCAL_LOG_DIR="logs/raw/$PROJECT/$RELEASE-$KERNEL"

if [ ! -d "$LOCAL_LOG_DIR" ]; then
    mkdir -p "$LOCAL_LOG_DIR"
fi

rsync --verbose --recursive -e "ssh -o StrictHostKeyChecking=no" \
    ubuntu@"$TARGET":logs/ "$LOCAL_LOG_DIR"

# vi: ts=4 noexpandtab
