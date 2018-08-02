#!/usr/bin/env python3
"""Collect software versions from test system."""

from . import BaseTest


class Test(BaseTest):
    """System info test object."""

    def execute(self, instance_type, release):
        """Collect data."""
        image_id = self.cloud.daily_image(release)
        instance = self.cloud.launch(image_id, instance_type=instance_type)
        instance.execute('sudo apt-get update')

        commands = [
            'uname --kernel-release',
            'apt-cache show systemd',
            'apt-cache show cloud-init',
            'apt-cache show fio',
            'apt-cache show netperf',
            'apt-cache show landscape-client',
        ]

        for cmd in commands:
            self._run_command(instance, cmd)

        instance.delete()

        return ""

    def parse_results(self, **kwargs):
        """Parse test results."""
        raise NotImplementedError

    @staticmethod
    def _run_command(instance, command):
        """TODO."""
        out, _, return_code = instance.execute(command)

        if return_code != 0:
            print('oops: something went wrong collecting %s' % command)

        print('$ %s\n%s\n' % (command, out))
