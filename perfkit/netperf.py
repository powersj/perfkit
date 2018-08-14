#!/usr/bin/env python3
"""Netperf Testing."""

import argparse
import statistics
import sys
import time

import distro_info

from . import BaseTest


class NetperfTest(BaseTest):
    """Netperf Test Object."""

    test_name = 'netperf'

    def __init__(self, cloud, instance_type, release, iterations, log_dir):
        """Initialize Netperf Test."""
        super().__init__(cloud, instance_type, release, iterations, log_dir)

        self.slave = None
        self.tcp_send = []
        self.udp_send = []
        self.tcp_receive = []

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
        self.instance.execute('sudo apt-get install --yes netperf')

        # place both in the same availability zone
        placement = {
            'AvailabilityZone': self.instance.availability_zone
        }
        self.slave = self.create_instance(Placement=placement)
        self.slave.execute('sudo apt-get update')
        self.slave.execute('sudo apt-get install --yes netperf')

    def execute(self):
        """Run the test."""
        self.tcp_send.append(self._run_netperf(test='TCP_STREAM'))
        self.udp_send.append(self._run_netperf(test='UDP_STREAM'))
        self.tcp_receive.append(self._run_netperf(test='TCP_MAERTS'))

    def cleanup(self):
        """Tear down instances."""
        self.slave.delete()
        self.instance.delete()

    def analyze(self):
        """Analyze collected results and produce final output."""
        result = [
            'Single stream TCP and UDP performance',
            'Command,netperf',
            '\niteration,TCP send,UDP send,TCP receive'
        ]

        for index, (tcp_s, udp_s, tcp_r) in enumerate(
                zip(self.tcp_send, self.udp_send, self.tcp_receive)):
            result.append('%s,%s,%s,%s' % (index, tcp_s, udp_s, tcp_r))

        result.append(self._calc_average())
        result.append(self._calc_median())
        if self.iterations > 1:
            result.append(self._calc_stdev())

        self.csv_result = '\n'.join(result)
        self.save_to_file(self.csv_result, prefix='results')

    def _calc_average(self):
        """Return averages of results."""
        return '\naverage,%.2f,%.2f,%.2f' % (
            sum(self.tcp_send)/len(self.tcp_send),
            sum(self.udp_send)/len(self.udp_send),
            sum(self.tcp_receive)/len(self.tcp_receive),
        )

    def _calc_median(self):
        """Return averages of results."""
        return 'median,%.2f,%.2f,%.2f' % (
            statistics.median(self.tcp_send),
            statistics.median(self.udp_send),
            statistics.median(self.tcp_receive),
        )

    def _calc_stdev(self):
        """Return averages of results."""
        return 'std dev,%.2f,%.2f,%.2f' % (
            statistics.stdev(self.tcp_send),
            statistics.stdev(self.udp_send),
            statistics.stdev(self.tcp_receive),
        )

    def _run_netperf(self, test):
        """Run netperf."""
        self._log.info('running %s', test)
        cpus = self.instance.execute('grep -c processor /proc/cpuinfo')
        slave_ip = self.slave.execute('hostname -I')
        netperf_cmd = (
            'sudo netperf -t {test} -H {server} -l 600 -c -C'
            ' -n {cpus}'.format(test=test, server=slave_ip, cpus=cpus)
        )

        output = self.instance.execute(netperf_cmd)
        self.save_to_file(output, suffix=test)

        if test == 'UDP_STREAM':
            result = self._netperf_output_bw(output, -2, 5)
        else:
            result = self._netperf_output_bw(output, -1, 4)

        self._log.info('sleeping between tests')
        time.sleep(120)

        return float(result)

    @staticmethod
    def _netperf_output_bw(text, line, field):
        """Return specific field from line in raw netperf output."""
        results = text.split('\n')[line]
        return ' '.join(results.split()).split(' ')[field]


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
        '--iterations', type=int, default=4,
        help='number of test iterations to run'
    )

    return parser.parse_args()


def run_netperf_testing():
    """TODO."""
    args = _setup_args()

    test = NetperfTest(
        'ec2', args.instance_type, args.release,
        args.iterations, args.log_dir
    )

    test.run()
    print(test.csv_result)


if __name__ == '__main__':
    sys.exit(run_netperf_testing())
