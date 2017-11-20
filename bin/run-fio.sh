#!/bin/bash
# Run basic fio tests.
#
# I would love to make this more dynamic and remove
# the need to have test files, do everything via the
# CLI to make it more explicit.
#
# Copyright 2017 Canonical Ltd.
# Joshua Powers <josh.powers@canonical.com>
set -eu

VERBOSITY=0
TEMP_D=""
LOG_DIR="$HOME/logs/fio"

error() { echo "$@" 1>&2; }
fail() { [ $# -eq 0 ] || error "$@"; exit 1; }
bad_usage() { usage 1>&2; return 1; }

cleanup() {
    [ -z "${TEMP_D}" ] || [ ! -d "${TEMP_D}" ] || rm -Rf "${TEMP_D}"
}

debug() {
    local level=${1}; shift;
    [ "${level}" -gt "${VERBOSITY}" ] && return
    error "${@}"
}

usage() {
    cat <<EOF
Usage: ${0##*/} [ options ]

   Run predefined fio tests.

   options:
      -r | --read       Run read tests
      -w | --write      Run write tests
      -o | --random     Run random I/O instead of sequential I/O
      -m | --md         Use /dev/md0 as target device
EOF
}

fio_test(){
    local test=$1
    shift

    filename="$LOG_DIR/$test-$(date +%s)"
    cmd="fio fio/$test.ini -output=$filename.json -output-format=json"
    printf "%s\n%s\n" "$(date)" "$cmd" | tee "$filename.log"
    $cmd | tee -a "$filename.log"

    printf "\n\n"
    sleep 60
}

main() {
    local short_opts="hvrwom"
    local long_opts="help,verbose,read,write,random,md"
    local getopt_out=""
    getopt_out=$(getopt --name "${0##*/}" \
        --options "${short_opts}" --long "${long_opts}" -- "$@") ||
        { bad_usage; return; }
    eval set -- "${getopt_out}" ||
        { bad_usage; return; }

    local read="" write="" random="" md=""
    local cur=""
    while [ $# -ne 0 ]; do
        cur="$1";
        case "$cur" in
            -h|--help) usage ; exit 0;;
            -v|--verbose) VERBOSITY=$((VERBOSITY+1));;
            -r|--read) read=1;;
            -w|--write) write=1;;
            -o|--random) random=1;;
            -m|--md) md=1;;
            --) shift; break;;
        esac
        shift;
    done

    if [ -z "$read" ] && [ -z "$write" ]; then
        echo "must specify either read or write"
        bad_usage
    fi

    if [ ! -d "$LOG_DIR" ]; then
        mkdir -p "$LOG_DIR"
    fi

    prefix=""
    if [ -n "$md" ]; then
        echo "running tests on /dev/md0"
        prefix="${prefix}md0-"
    fi

    if [ -n "$random" ]; then
        echo "running random tests"
        prefix="${prefix}random-"
    fi

    if [ -n "$read" ]; then
        echo "running read tests"
        fio_test "${prefix}read"
    fi

    if [ -n "$write" ]; then
        echo "running write tests"
        fio_test "${prefix}write"
    fi

    return 0
}

main "$@"
# vi: ts=4 noexpandtab
