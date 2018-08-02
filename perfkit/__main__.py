# This file is part of perfkit. See LICENSE file for license information.
"""Program entry point and arg parser."""

import argparse
import datetime
import logging
import os
import sys

import distro_info

from . import boot, info


def _setup_logging(debug=False):
    """Set up the root logger with format and level."""
    log = logging.getLogger()

    level = logging.DEBUG if debug else logging.INFO
    log.setLevel(level)

    console = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console.setFormatter(formatter)
    log.addHandler(console)


def _setup_args():
    """TODO."""
    parser = argparse.ArgumentParser(prog='perfkit')
    parser.add_argument('--log-dir', default='logs', help='dir to write logs')

    subparsers = parser.add_subparsers(title='Subcommands', dest='subcommand')
    subparsers.add_parser(
        'info', help='collect system info'
    )

    boot_time = subparsers.add_parser('boot-time', help='run boot time')
    boot_time.add_argument('instance_type', help='Instance type to test')
    boot_time.add_argument(
        '--release', default=distro_info.UbuntuDistroInfo().lts(),
        help='Ubuntu release under test'
    )
    boot_time.add_argument(
        '--iterations', type=int, default=10,
        help='Number of iterations to run'
    )

    return parser.parse_args()


def _results_to_file(result, log_dir):
    """TODO."""
    os.makedirs(log_dir, exist_ok=True)

    date = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = 'boot-%s.log' % date

    with open(os.path.join(log_dir, filename), 'w') as out:
        out.write(result)


def launch_test():
    """Run selected test and record results to file."""
    args = _setup_args()
    _setup_logging()

    result = ""
    if args.subcommand == 'boot-time':
        test = boot.Test()
        launch_data, reboot_data = test.execute(
            args.instance_type, args.release, args.iterations
        )
        result = test.parse_results(launch_data, reboot_data)
    elif args.subcommand == 'info':
        test = info.Test()
        result = test.execute(args.instance_type, args.release)

    if result:
        log_dir = os.path.join(args.log_dir, args.instance_type, args.release)
        _results_to_file(result, log_dir)
        print(result)


if __name__ == '__main__':
    sys.exit(launch_test())
