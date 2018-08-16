#!/usr/bin/env python3
"""FIO Testing."""

import argparse
import json
import statistics
import sys
import time

import distro_info

from . import BaseTest


class FioResult:
    """Store fio results."""

    def __init__(self):
        """Initialize class."""
        self.iops = 0.0
        self.bw = 0.0
        self.io = 0.0
        self.util = 0.0

    def __str__(self):
        """Print CSV of results."""
        return "%.f,%.f,%.f,%.2f" % (
            self.iops, self.bw, self.io, self.util
        )


class FioTest(BaseTest):
    """FIO Test Object."""

    test_name = 'fio'

    def __init__(self, cloud, instance_type, release, iterations, log_dir):
        """Initialize FIO Test."""
        super().__init__(cloud, instance_type, release, iterations, log_dir)

        self.read_results = []
        self.write_results = []
        self.raid_disk = None

        self.fio_boot_disk = (
            "fio --name={name} --readwrite={type} --size=1G --numjobs=4"
            " --direct=1 --ioengine=libaio --iodepth=32"
            " --time_based --ramp_time=60 --runtime=600"
            " --group_reporting=1 --output-format=json --output=fio.json"
        )
        self.fio_raid_disk = (
            "sudo fio --name={name} --readwrite={type} --filename={disk}"
            " --numjobs=32 --direct=1 --ioengine=libaio --iodepth=32"
            " --time_based --ramp_time=60 --runtime=600"
            " --group_reporting=1 --output-format=json --output=fio.json"
        )

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
        self.instance.execute('sudo apt-get update')
        self.instance.execute('sudo apt-get install --yes fio')

    def execute(self):
        """Run the test."""
        self.read_results.append(self._run_fio('read'))
        self._log.info('sleeping between tests')
        time.sleep(120)
        self.write_results.append(self._run_fio('write'))

    def cleanup(self):
        """Tear down instances."""
        self.instance.delete()

    def analyze(self):
        """Analyze collected results and produce final output."""
        self.csv_result = '\n'.join([
            'Peak 4K IOPS performance of sequential read and write',
            'Command,fio',
            '\nRead',
            self._print_results(self.read_results),
            '\nWrite',
            self._print_results(self.write_results),
        ])

        self.save_to_file(self.csv_result, prefix='results')

    @staticmethod
    def _calc_disk_mean(disks):
        """Determine mean disk utilization."""
        total = 0.0
        for disk in disks:
            total = total + disk['util']

        return total / len(disks)

    def _print_results(self, results):
        """TODO."""
        result = ['iteration,iops,bw,io,mean disk util']
        for count, data in enumerate(results):
            result.append('%s,%s' % (count+1, data))

        result.append(self._calc_average(results))
        result.append(self._calc_median(results))
        if self.iterations > 1:
            result.append(self._calc_stdev(results))

        return '\n'.join(result)

    @staticmethod
    def _calc_average(results):
        """Return averages of results."""
        total = len(results)

        iops = sum([result.iops for result in results]) / total
        bw = sum([result.bw for result in results]) / total
        io = sum([result.io for result in results]) / total
        util = sum([result.util for result in results]) / total

        return '\naverage,%.3f,%.3f,%.3f,%.3f' % (iops, bw, io, util)

    @staticmethod
    def _calc_median(results):
        """Return averages of results."""
        iops = statistics.median([result.iops for result in results])
        bw = statistics.median([result.bw for result in results])
        io = statistics.median([result.io for result in results])
        util = statistics.median([result.util for result in results])

        return 'median,%.3f,%.3f,%.3f,%.3f' % (iops, bw, io, util)

    @staticmethod
    def _calc_stdev(results):
        """Return averages of results."""
        iops = statistics.stdev([result.iops for result in results])
        bw = statistics.stdev([result.bw for result in results])
        io = statistics.stdev([result.io for result in results])
        util = statistics.stdev([result.util for result in results])

        return 'std dev,%.3f,%.3f,%.3f,%.3f' % (iops, bw, io, util)

    def _run_fio(self, test):
        """Run FIO itself."""
        self._log.info('running %s test', test)
        if self.raid_disk:
            fio_cmd = self.fio_raid_disk.format(
                name=test, type=test, disk=self.raid_disk
            )
        else:
            fio_cmd = self.fio_boot_disk.format(name=test, type=test)

        self.instance.execute(fio_cmd)
        output = self.instance.execute('sudo cat fio.json')
        self.save_to_file(output, suffix=test)

        # clean up between tests
        self.instance.execute('sudo rm *')

        try:
            data = json.loads(output)
        except json.decoder.JSONDecodeError:
            self._log.error(fio_cmd)
            self._log.error('JSON result failure:')
            self._log.error(output)
            self.instance.delete()
            sys.exit(1)

        result = FioResult()
        result.iops = data['jobs'][0][test]['iops']
        result.bw = data['jobs'][0][test]['bw']
        result.io = data['jobs'][0][test]['io_bytes']
        result.util = self._calc_disk_mean(data['disk_util'])

        return result


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
        '--iterations', type=int, default=5,
        help='number of test iterations to run'
    )

    return parser.parse_args()


def run_boot_testing():
    """TODO."""
    args = _setup_args()

    test = FioTest(
        'ec2', args.instance_type, args.release,
        args.iterations, args.log_dir
    )

    test.run()
    print(test.csv_result)


if __name__ == '__main__':
    sys.exit(run_boot_testing())
