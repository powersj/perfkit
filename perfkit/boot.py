#!/usr/bin/env python3
"""Collect boot and reboot test time.

This will run the follow test steps a defined number of times:

  1. launch the instance
  2. run systemd-analyze
  3. reboot
  4. run systemd-analyze
  5. tear down

The end result will be the results and averages.
"""

import argparse
import statistics
import sys

import distro_info

from . import BaseTest


class BootResult:
    """Store boot time test results."""

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


class BootTest(BaseTest):
    """Boot Time Test Object."""

    test_name = 'boot'

    def __init__(self, cloud, instance_type, release, iterations, log_dir):
        """Initialize Boot Time Test."""
        super().__init__(cloud, instance_type, release, iterations, log_dir)

        self.systemd_launch_times = []
        self.systemd_reboot_times = []

    def run(self):
        """Combine provision, execute, and cleanup and run iterations."""
        for index in range(self.iterations):
            self._log.info(
                'running iteration %s of %s', str(index+1), self.iterations
            )
            self.provision()
            self.execute()
            self.cleanup()

        self.analyze()

    def provision(self):
        """Create and setup instances for testing."""
        self.instance = self.create_instance()

    def execute(self):
        """Run the test."""
        self._systemd_output()
        self._log.info('restarting instance')
        self.instance.restart()
        self._systemd_output(reboot=True)

    def cleanup(self):
        """Tear down instances."""
        self.instance.delete()

    def analyze(self):
        """Analyze collected results and produce final output."""
        self.csv_result = '\n'.join([
            'Description,Initial boot and reboot systemd-analyze times',
            'Command,systemd-analyze time',
            '\nInitial Boot',
            self._print_results(self.systemd_launch_times),
            '\nReboot',
            self._print_results(self.systemd_reboot_times),
        ])

        self.save_to_file(self.csv_result, prefix='results')

    def _systemd_output(self, reboot=False):
        """Run systemd-analyze on instance."""
        result = self.instance.execute('systemd-analyze')
        self.save_to_file(result, suffix='reboot' if reboot else '')

        times = self._parse_systemd_analyze(result)
        if reboot:
            self.systemd_reboot_times.append(times)
        else:
            self.systemd_launch_times.append(times)

    @staticmethod
    def _parse_systemd_analyze(result):
        """Parse the output of systemd analyze and returns Boot Result."""
        prefix = 'Startup finished in '
        lines = str(result).replace(prefix, '').split('=')[0].split('+')
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

    def _print_results(self, boot_time_result):
        """Format results with average, median, and std. deviation."""
        result = ['iteration,kernel,userspace,total']
        for count, boot_time in enumerate(boot_time_result):
            result.append('%s,%s' % (count, boot_time))

        result.append(self._calc_average(boot_time_result))
        result.append(self._calc_median(boot_time_result))
        if self.iterations > 1:
            result.append(self._calc_stdev(boot_time_result))

        return '\n'.join(result)

    @staticmethod
    def _calc_average(results):
        """Return averages of results."""
        total = len(results)

        kernel = sum([result.kernel for result in results]) / total
        userspace = sum([result.userspace for result in results]) / total
        total = sum([result.total for result in results]) / total

        return '\naverage,%.3f,%.3f,%.3f' % (kernel, userspace, total)

    @staticmethod
    def _calc_median(results):
        """Return averages of results."""
        kernel = statistics.median([result.kernel for result in results])
        userspace = statistics.median([result.userspace for result in results])
        total = statistics.median([result.total for result in results])

        return 'median,%.3f,%.3f,%.3f' % (kernel, userspace, total)

    @staticmethod
    def _calc_stdev(results):
        """Return averages of results."""
        kernel = statistics.stdev([result.kernel for result in results])
        userspace = statistics.stdev([result.userspace for result in results])
        total = statistics.stdev([result.total for result in results])

        return 'std dev,%.3f,%.3f,%.3f' % (kernel, userspace, total)


def _setup_args():
    """TODO."""
    parser = argparse.ArgumentParser(
        prog='boot', description='Collect boot and reboot timings'
    )

    parser.add_argument(
        '--log-dir', default='logs', help='dir to write logs'
    )
    parser.add_argument(
        'instance_type', help='Instance type to test'
    )
    parser.add_argument(
        '--release', default=distro_info.UbuntuDistroInfo().lts(),
        help='Ubuntu release to test; default is latest LTS'
    )
    parser.add_argument(
        '--iterations', type=int, default=10,
        help='number of test iterations to run'
    )

    return parser.parse_args()


def run_boot_testing():
    """TODO."""
    args = _setup_args()

    test = BootTest(
        'ec2', args.instance_type, args.release,
        args.iterations, args.log_dir
    )

    test.run()
    print(test.csv_result)


if __name__ == '__main__':
    sys.exit(run_boot_testing())
