# This file is part of perfkit. See LICENSE file for license information.
"""Perfkit."""

import logging

import pycloudlib


class BaseTest:
    """Base test object."""

    def __init__(self):
        """Initialize base test."""
        self._log = logging.getLogger(__name__)
        self.cloud = pycloudlib.EC2()

    def execute(self, instance_type, release, iterations):
        """Execute a test."""
        raise NotImplementedError

    def parse_results(self, **kwargs):
        """Parse test results."""
        raise NotImplementedError
