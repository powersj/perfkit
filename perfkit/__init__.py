# This file is part of perfkit. See LICENSE file for license information.
"""Perfkit."""

import datetime
import logging
import os
import subprocess
import sys

import pycloudlib


class BaseTest:
    """Base test object."""

    test_name = 'unknown'

    def __init__(self, _, instance_type, release, iterations=1, log_dir=''):
        """Initialize base test."""
        self.log_dir = os.path.join(
            log_dir, instance_type, release, self.test_name
        )
        self.setup_logging()
        self._log = logging.getLogger(__name__)

        self.cloud = pycloudlib.EC2()
        self.instance_type = instance_type
        self.release = release
        self.iterations = iterations

        self.csv_result = ''
        self.instance = None

    def run(self):
        """Execute a test."""
        raise NotImplementedError

    def provision(self):
        """Parse test results."""
        raise NotImplementedError

    def execute(self):
        """Parse test results."""
        raise NotImplementedError

    def cleanup(self):
        """Parse test results."""
        raise NotImplementedError

    def create_instance(self):
        """Create an instance for testing."""
        return self._launch_instance()

    def _launch_instance(self):
        """Launch an instance."""
        self._log.info('launching instance')

        try:
            image_id = self.cloud.daily_image(self.release)
        except IndexError:
            self._log.error('Could not find an image for %s', self.release)
            sys.exit(1)

        return self.cloud.launch(
            image_id, instance_type=self.instance_type
        )

    @staticmethod
    def pastebinit(content):
        """Send content to pastebinit and get URL back."""
        process = subprocess.run(
            ['pastebinit'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            input=content.encode('utf-8')
        )

        return process.stdout.rsplit()[0].decode('utf-8')

    def save_to_file(self, string, prefix='', suffix=''):
        """Save the given string to a file in the log directory."""
        date = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        strings = [prefix, self.test_name, suffix, date]
        filename = '%s.log' % '-'.join(filter(None, strings))
        with open(os.path.join(self.log_dir, filename), 'w') as out:
            out.write('%s\n' % string)

    def setup_logging(self):
        """Set up the root logger with format and level."""
        log = logging.getLogger()
        log.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Console Logging
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        log.addHandler(console)

        # File Logging
        os.makedirs(self.log_dir, exist_ok=True)
        filename = '%s-%s.out' % (
            self.test_name,
            datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        )
        file = logging.FileHandler(os.path.join(self.log_dir, filename))
        file.setFormatter(formatter)
        log.addHandler(file)
