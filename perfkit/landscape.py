#!/usr/bin/env python3
"""Use landscape to import a system.

The landscape_api is Python 2 only and pycloudlib is Python 3 only. As
a result this uses the landscape-api CLI instead of the native Python
library.
"""

import argparse
import ast
import json
import sys
import time
import uuid

from . import BaseTest


class LandscapeTest(BaseTest):
    """Landscape Object."""

    test_name = 'landscape'

    def __init__(self, cloud, instance_type, release, log_dir):
        """Initialize Landscape Test."""
        super().__init__(cloud, instance_type, release, 1, log_dir)

        self.computer_id = None
        self.hardware_info = ''
        self.computer_title = 'perfkit-%s-%s-%s' % (
            self.instance_type, self.release, str(uuid.uuid4())[:8]
        )

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
        self._register_computer()
        self._accept_computer()
        self._get_hardware_info()

        self._log.info('removing computer from landscape')
        self.subp('landsape-api remove-computers %s' % self.computer_id)

    def cleanup(self):
        """Tear down instances."""
        self.instance.delete()

    def analyze(self):
        """Analyze collected results and produce final output."""
        data = json.dumps(self.hardware_info, indent=4, sort_keys=True)

        self.csv_result = '\n'.join([
            'Description,Add instance to Landscape\n'
            'Hardware,%s' % self.pastebinit(data),
        ])

        self.save_to_file(self.hardware_info)
        self.save_to_file(self.csv_result, prefix='results')

    def _accept_computer(self):
        """Accept computer into Landscape."""
        out, _ = self.subp('landscape-api get-pending-computers')
        pending_computers = ast.literal_eval(out)

        for pending in pending_computers:
            if pending['title'] == self.computer_title:
                self._log.info('accepting pending computer: %s', pending['id'])
                out, _ = self.subp(
                    'landscape-api accept-pending-computers %s' % pending['id']
                )
                self.computer_id = ast.literal_eval(out)[0]['id']
                self._log.info('accepted computer: %s', self.computer_id)

        if not self.computer_id:
            self._log.error('No computer ID found. Exiting.')
            self.instance.delete()
            sys.exit(1)

    def _get_computer(self):
        """Return computer based on id."""
        cmd = (
            "landscape-api get-computers --query 'id:%s' --with-hardware" %
            self.computer_id
        )
        out, _ = self.subp(cmd)

        try:
            return ast.literal_eval(out)[0]
        except IndexError:
            return []

    def _get_hardware_info(self):
        """Get computer hardware info."""
        while 'hardware' not in self.hardware_info:
            self._log.info('sleeping to wait for hardware info')
            time.sleep(30)

            self.hardware_info = self._get_computer()

    def _register_computer(self):
        """Register system with Landscape."""
        self._log.info('instaling client & registering system')
        self.instance.execute('sudo apt-get update')
        self.instance.execute('sudo apt-get install --yes landscape-client')

        self.instance.execute(
            'sudo landscape-config --computer-title "%s"'
            ' --account-name canonical-server --silent'
            % self.computer_title
        )

        # wait for system to be registered
        self._log.info('sleeping to allow registration')
        time.sleep(10)


def _setup_args():
    """TODO."""
    parser = argparse.ArgumentParser(
        prog='landscape',
        description='Add instance to Landscap & gather hardware info'
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

    return parser.parse_args()


def run_landscape_testing():
    """TODO."""
    args = _setup_args()

    test = LandscapeTest(
        'ec2', args.instance_type, args.release, args.log_dir
    )

    test.run()
    print(test.csv_result)


if __name__ == '__main__':
    sys.exit(run_landscape_testing())
