#!/usr/bin/env python3
"""Collect boot and reboot test time.

This will run the follow test steps a defined number of times:

  1. launch the instance
  2. collect systemd-analyze output
  3. reboot
  4. collect systemd-analyze output
  5. tear down

The end result will be the results and averages.
"""

import argparse
import datetime
import os
import statistics
import sys

import pycloudlib


class BootResult():
    """Capture results from test."""

    def __init__(self):
        """Initialize class."""
        self.kernel = 0.0
        self.loader = 0.0
        self.userspace = 0.0

    @property
    def total(self):
        """Return total time."""
        return round(self.kernel + self.loader + self.userspace, 3)

    def __str__(self):
        """Print CSV of results."""
        return "%.3f,%.3f,%.3f" % (self.kernel, self.userspace, self.total)


def _setup_args():
    """Set up and configure argparse."""
    parser = argparse.ArgumentParser(prog='Instance Boot Time Test')
    parser.add_argument(
        'instance_type', help='AWS instance type to test'
    )
    parser.add_argument(
        '--release',  default='bionic', help='Ubuntu release under test'
    )
    parser.add_argument(
        '--iterations',  default=10, type=int,
        help='Number of iterations to complete'
    )

    args = parser.parse_args()
    return args.release, args.instance_type, args.iterations


def collect_systemd_analyze(instance):
    """Run systemd-analyze on instance."""
    out, _, rc = instance.execute('systemd-analyze')

    if rc != 0:
        print('oops: something went wrong collecting systemd-analyze')

    return parse_systemd_analyze(out)


def parse_systemd_analyze(systemd_output):
    """Parse out the various times from analyze output."""
    prefix = 'Startup finished in '
    lines = systemd_output.replace(prefix, '').split('=')[0].split('+')
    times = [x.replace('(', '').replace(')', '').strip() for x in lines]

    result = BootResult()
    for entry in times:
        # "59.968s kernel" versus "1m 3s kernel"
        values = entry.split(' ')

        if len(values) == 3:
            mins = float(values[0].replace('min', ''))
            seconds = float(values[1].replace('s', ''))
            setattr(result, values[2], (mins * 60.0) + seconds)
        else:
            setattr(result, values[1], float(values[0].replace('s', '')))

    return result


def format_results(results):
    """Format results with average, median, and std. deviation."""
    kernel = []
    userspace = []
    total = []

    output = 'iteration,kernel,userspace,total\n'
    for count, result in enumerate(results):
        kernel.append(result.kernel)
        userspace.append(result.userspace)
        total.append(result.total)

        output += '%s,%s\n' % (count, result)

    output += '\nAverage,%.3f,%.3f,%.3f\n' % (
        sum(kernel)/len(kernel),
        sum(userspace)/len(userspace),
        sum(total)/len(total)
    )
    output += 'Median,%.3f,%.3f,%.3f\n' % (
        statistics.median(kernel),
        statistics.median(userspace),
        statistics.median(total),
    )
    output += 'Std. Deviation,%.3f,%.3f,%.3f\n' % (
        statistics.stdev(kernel),
        statistics.stdev(userspace),
        statistics.stdev(total),
    )
    output += '\n'

    return output


def run_tests(iterations, instance_type, ec2, daily_image_ami):
    """Run the launching and collection of data."""
    launch = []
    reboot = []

    for index in range(iterations):
        print('running iteration %s' % str(index+1))
        instance = ec2.launch(daily_image_ami, instance_type=instance_type)
        launch.append(collect_systemd_analyze(instance))

        instance.restart()
        reboot.append(collect_systemd_analyze(instance))

        instance.delete()

    return launch, reboot


def parse_data(launch_data, reboot_data):
    """Parse out the actual data and return data."""
    result = 'Description,Initial boot and reboot times\n'
    result += 'Command,systemd-analyze time\n'

    result += '\nInitial Boot\n'
    result += format_results(launch_data)
    result += '\nReboot\n'
    result += format_results(reboot_data)

    return result


def results_to_file(results, instance_type, release):
    """TODO."""
    logs_dir = 'logs/%s/%s' % (instance_type, release)
    os.makedirs(logs_dir, exist_ok=True)

    date = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = 'boot-%s.log' % (date)

    with open(os.path.join(logs_dir, filename), 'w') as out:
        out.write(results)


def test_boot_time():
    """Launch and collect boot times for an instance."""
    release, instance_type, iterations = _setup_args()

    print('logging into EC2')
    ec2 = pycloudlib.EC2()
    daily_image_ami = ec2.daily_image(release)
    print('using daily image for %s: %s' % (release, daily_image_ami))

    launch_data, reboot_data = run_tests(
        iterations, instance_type, ec2, daily_image_ami
    )

    results = parse_data(launch_data, reboot_data)
    results_to_file(results, instance_type, release)
    print('\n%s' % results)


if __name__ == '__main__':
    sys.exit(test_boot_time())
