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

import statistics

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


class Test(BaseTest):
    """Boot Time Test Object."""

    def execute(self, instance_type, release, iterations):
        """Boot and reboot instance and collect results."""
        launch = []
        reboot = []

        image_id = self.cloud.daily_image(release)
        for index in range(iterations):
            self._log.info('running iteration %s', str(index+1))

            instance = self.cloud.launch(image_id, instance_type=instance_type)
            launch.append(self._collect_systemd_analyze(instance))

            instance.restart()
            reboot.append(self._collect_systemd_analyze(instance))

            instance.delete()

        return launch, reboot

    def parse_results(self, launch, reboot):
        """Parse the systemd-analyze results."""
        result = ['Description,Initial boot and reboot times']
        result.append('Command,systemd-analyze time')

        result.append('\nInitial Boot')
        result.extend(self._format_results(launch))
        result.append('\nReboot')
        result.extend(self._format_results(reboot))

        return '\n'.join(result)

    @staticmethod
    def _collect_systemd_analyze(instance):
        """Run systemd-analyze on instance."""
        stdout, _, _ = instance.execute('systemd-analyze')

        prefix = 'Startup finished in '
        lines = stdout.replace(prefix, '').split('=')[0].split('+')
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

    @staticmethod
    def _format_results(results):
        """Format results with average, median, and std. deviation."""
        kernel, userspace, total = [], [], []

        result = ['iteration,kernel,userspace,total\n']
        for count, result in enumerate(results):
            result.append('%s,%s' % (count, result))

            kernel.append(result.kernel)
            userspace.append(result.userspace)
            total.append(result.total)

        result.append('\nAverage,%.3f,%.3f,%.3f' % (
            sum(kernel)/len(kernel),
            sum(userspace)/len(userspace),
            sum(total)/len(total)
        ))
        result.append('Median,%.3f,%.3f,%.3f' % (
            statistics.median(kernel),
            statistics.median(userspace),
            statistics.median(total),
        ))
        result.append('Std. Deviation,%.3f,%.3f,%.3f' % (
            statistics.stdev(kernel),
            statistics.stdev(userspace),
            statistics.stdev(total),
        ))
        result.append('')

        return result
