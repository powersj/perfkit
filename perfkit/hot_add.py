#!/usr/bin/env python3
"""Hot-add storage and network to an instance."""

import argparse
import sys
import time

from . import BaseTest


class HotAddTest(BaseTest):
    """Hot-Add Object."""

    test_name = 'hot-add'

    def __init__(self, cloud, instance_type, release, iterations, log_dir,
                 num_network_devs=1, num_storage_devs=1):
        """Initialize Hot-Add Test."""
        super().__init__(cloud, instance_type, release, iterations, log_dir)

        self.dmesg = ''
        self.ip_a = ''
        self.lsblk = ''
        self.num_network_devs = num_network_devs
        self.num_storage_devs = num_storage_devs

    def run(self):
        """Combine provision, execute, and cleanup and run iterations."""
        self.provision()
        self.execute()
        self.cleanup()
        self.analyze()

    def provision(self):
        """Create and setup instances for testing."""
        self.instance = self.create_instance()

    def execute(self):
        """Run the test."""
        for index in range(self.num_network_devs):
            self._log.info('adding network device %s of %s',
                           index+1, self.num_network_devs)
            self.instance.add_network_interface()

        for index in range(self.num_storage_devs):
            self._log.info('adding storage device %s of %s',
                           index+1, self.num_storage_devs)
            self.instance.add_volume()

        # make sure we wait for everything to get added
        self._log.info('sleeping to allow instance to settle')
        time.sleep(60)

        self._log.info('collecting system information')
        self.dmesg = self.instance.execute('dmesg')
        self.ip_a = self.instance.execute('ip a')
        self.lsblk = self.instance.execute('lsblk')

    def cleanup(self):
        """Tear down instances."""
        self.instance.delete()

    def analyze(self):
        """Analyze collected results and produce final output."""
        self.csv_result = '\n'.join([
            'Description,EBS and Network hot-plug and console functionality\n'
            'Add via Hotplug',
            'ENI Devices,%s' % self.pastebinit(self.ip_a),
            'EBS Devices,%s' % self.pastebinit(self.lsblk),
            'dmesg,%s' % self.pastebinit(self.dmesg),
        ])

        self.save_to_file(self.csv_result, prefix='results')


def _setup_args():
    """TODO."""
    parser = argparse.ArgumentParser(
        prog='hot-add',
        description='EBS and Network hot-plug and console functionality'
    )

    parser.add_argument(
        '--log-dir', default='logs', help='dir to write logs'
    )
    parser.add_argument(
        'instance_type', help='Instance type to test'
    )
    parser.add_argument(
        '--release', required=True,
        help='Ubuntu release to test; default is latest LTS'
    )
    parser.add_argument(
        '--network', type=int, default=1,
        help='Number of network devices to add'
    )
    parser.add_argument(
        '--storage', type=int, default=1,
        help='Number of storage devices to add'
    )

    return parser.parse_args()


def run_hot_add_testing():
    """TODO."""
    args = _setup_args()

    test = HotAddTest(
        'ec2', args.instance_type, args.release,
        1, args.log_dir, args.network, args.storage
    )

    test.run()
    print(test.csv_result)


if __name__ == '__main__':
    sys.exit(run_hot_add_testing())
