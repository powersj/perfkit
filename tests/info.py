#!/usr/bin/env python3
"""Collect info about test system.
"""

import argparse
import os
import sys

import pycloudlib


def run_command(instance, command):
    """TODO."""
    out, _, rc = instance.execute(command)

    if rc != 0:
        print('oops: something went wrong collecting %s' % command)

    print('$ %s\n%s\n' % (command, out))


def _setup_args():
    """Set up and configure argparse."""
    parser = argparse.ArgumentParser(prog='Instance Boot Time Test')
    parser.add_argument(
        'instance_type', help='AWS instance type to test'
    )
    parser.add_argument(
        '--release',  default='bionic', help='Ubuntu release under test'
    )

    args = parser.parse_args()
    return args.release, args.instance_type


def collect_info():
    """TODO."""
    release, instance_type = _setup_args()

    print('logging into EC2')
    ec2 = pycloudlib.EC2()
    daily_image_ami = ec2.daily_image(release)
    print('using daily image for %s: %s' % (release, daily_image_ami))

    instance = ec2.launch(daily_image_ami, instance_type=instance_type)
    instance.execute('sudo apt-get update')

    commands = [
        'uname --kernel-release',
        'apt-cache show systemd',
        'apt-cache show cloud-init',
        'apt-cache show fio',
        'apt-cache show netperf',
        'apt-cache show landscape-client',
    ]

    for cmd in commands:
        run_command(instance, cmd)

    instance.delete()


if __name__ == '__main__':
    sys.exit(collect_info())
