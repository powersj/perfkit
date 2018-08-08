#!/usr/bin/env python3
"""Collect software versions from test system."""

import argparse
import re
import sys

import distro_info

from . import BaseTest


class InfoTest(BaseTest):
    """System info test object."""

    binaries = [
        'systemd',
        'cloud-init',
        'fio',
        'netperf',
        'landscape-client'
    ]

    test_name = 'info'

    def __init__(self, cloud, instance_type, release, iterations, log_dir):
        """Initialize Info Collection Test."""
        super().__init__(cloud, instance_type, release, iterations, log_dir)

        self.versions = {}
        self.datasource = ''
        self.ci_log = ''
        self.ci_log_output = ''

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
        self._log.info('collecting versions')
        self.instance.execute('sudo apt-get update')
        self.versions['kernel'] = self.instance.execute('uname --r')
        for binary in self.binaries:
            self.versions[binary] = self._parse_version(binary)

        self._log.info('collecting cloud-init details')
        self.datasource = self.instance.execute(
            'cat /var/lib/cloud/instance/datasource'
        )
        self.ci_log = self.instance.execute('cat /var/log/cloud-init.log')
        self.ci_log_output = self.instance.execute(
            'cat /var/log/cloud-init-output.log'
        )

    def cleanup(self):
        """Tear down instances."""
        self.instance.delete()

    def analyze(self):
        """Analyze collected results and produce final output."""
        result = [
            'Instance Performance Qualification\n',
            'Test,Description',
            'boot,Initial boot and reboot systemd-analyze times',
            'fio,Peak 4K seq. read and write IOPS on boot drive',
            'fio-nvme,fio test on additional NVMe drives',
            'netperf,Single stream TCP and UDP performance',
            'cloud-init,Verify cloud-init and cloud-id',
            'landscape-client,Add instance to Landscape',
            'aws,EBS and Network hot-plug and console functionality',
            '\nSoftware Versions',
        ]

        for binary, version in sorted(self.versions.items()):
            result.append('%s,%s' % (binary, version))

        result.extend([
            '\nDescription,Verify cloud-init and cloud-id',
            'ds-identify,%s' % self.pastebinit(self.datasource),
            'cloud-init.log,%s' % self.pastebinit(self.ci_log),
            'cloud-init-output.log,%s' % self.pastebinit(self.ci_log_output)
        ])

        self.csv_result = '\n'.join(result)
        self.save_to_file(self.csv_result, prefix='results')

    def _parse_version(self, binary):
        """TODO."""
        result = self.instance.execute('apt-cache show %s' % binary)

        try:
            version = re.search(r'Version:\s(.+?)\n', result).group(1)
        except (AttributeError, IndexError):
            version = 'unknown'

        return version


def _setup_args():
    """TODO."""
    parser = argparse.ArgumentParser(
        prog='info', description='Collect general system information'
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

    return parser.parse_args()


def run_info_testing():
    """TODO."""
    args = _setup_args()

    test = InfoTest(
        'ec2', args.instance_type, args.release, 1, args.log_dir
    )

    test.run()
    print(test.csv_result)


if __name__ == '__main__':
    sys.exit(run_info_testing())
