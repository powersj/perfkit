#!/bin/bash
# Run KVM and QEMU unit tests
#
# Copyright 2017 Canonical Ltd.
# Joshua Powers <josh.powers@canonical.com>
set -ux

LOG_DIR="$HOME/logs/kvm"

if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
fi

sudo apt update
sudo apt install -y make build-essential python qemu-kvm qemu-system-x86

git clone https://git.kernel.org/pub/scm/virt/kvm/kvm-unit-tests.git
cd kvm-unit-tests/
./configure
make

filename="$LOG_DIR/qemu-$(date +%s).log"
cmd="sudo ./x86-run ./x86/msr.flat"
printf "%s\n%s\n" "$(date)" "$cmd" | tee "$filename"
$cmd | tee -a "$filename"

filename="$LOG_DIR/kvm-$(date +%s).log"
cmd="sudo ./run_tests.sh -j 4"
printf "%s\n%s\n" "$(date)" "$cmd" | tee "$filename"
$cmd | tee -a "$filename"
