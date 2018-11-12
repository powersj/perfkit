#!/usr/bin/env python3
"""FIO NVMe Testing."""

import argparse
import json
import sys

from .fio import FioTest


class FioNvmeTest(FioTest):
    """FIO NVMe Test Object."""

    test_name = 'fio-nvme'

    def provision(self):
        """Create and setup instances for testing."""
        self.instance = self.create_instance()
        self.instance.execute('sudo apt-get update')
        self.instance.execute('sudo apt-get install --yes fio')
        self.instance.execute('sudo apt-get install --yes mdadm')
        self.raid_disk = self._create_raid_0()

    def _create_raid_0(self):
        """Create RAID 0 with given disks."""
        disks = self._find_free_nvme_disks()

        if not disks:
            self.instance.delete()
            self._log.error('No disks to test')
            sys.exit(1)
        elif len(disks) == 1:
            return '%s' % disks[0]
        else:
            mdadm_cmd = (
                'sudo mdadm --create /dev/md0 --level=0 --name=TEST_RAID'
                ' --raid-devices=%s %s' % (len(disks), ' '.join(disks))
            )

            self.instance.execute(mdadm_cmd)
            return '/dev/md0'

    def _find_free_nvme_disks(self):
        """Find available and free nvme disks."""
        output = self.instance.execute('lsblk --json')
        data = json.loads(output)

        devices = []
        for dev in data['blockdevices']:
            if dev['name'].startswith('nvme'):
                if 'children' not in dev:
                    devices.append('/dev/%s' % dev['name'])

        return devices


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
        '--release', required=True,
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

    test = FioNvmeTest(
        'ec2', args.instance_type, args.release,
        args.iterations, args.log_dir
    )

    test.run()
    print(test.csv_result)


if __name__ == '__main__':
    sys.exit(run_boot_testing())
