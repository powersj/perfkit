#!/bin/bash
# Run hour long netperf stream and rr tests.
#
# Copyright 2017 Canonical Ltd.
# Joshua Powers <josh.powers@canonical.com>
set -eux

TARGET=${1:-''}
if [ -z "$TARGET" ]; then
    echo "target IP not set!"
    echo "$0 target_ip"
    exit 1
fi

CPUS=$(grep -c 'processor' /proc/cpuinfo)
LOG_DIR="$HOME/logs/netperf"

if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
fi

run_test() {
    local test="$1"
    shift 1

    # -l: run for 600 seconds
    # -D: print interim results every 60 seconds
    # -c: print local CPU usage
    # -C: print remote CPU usage
    # -n: set the nubmer of CPUs
    cmd="sudo netperf -t $test -H $TARGET -l 600 -D 60 -c -C -n $CPUS"

    filename="$LOG_DIR/$test-$(date +%s).log"
    printf "%s\n%s\n" "$(date)" "$cmd" | tee "$filename"
    $cmd | tee -a "$filename"

    printf "\n\n"
    sleep 60
}


STREAM_TESTS=("TCP_STREAM" "TCP_MAERTS" "UDP_STREAM")
for test in "${STREAM_TESTS[@]}"; do
    # -f: print in gigabits (only necessary for STREAM tests; not RR)
    run_test "$test"
done

RR_TESTS=("TCP_RR" "UDP_RR")
for test in "${RR_TESTS[@]}"; do
    run_test "$test"
done

# vi: ts=4 noexpandtab
