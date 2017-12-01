#!/usr/bin/env python3
"""Terminate AWS EC2 instances."""
import sys

import botocore
import boto3


def delete(instance_ids=None):
    """Terminate AWS EC2 instances."""
    ec2 = boto3.resource('ec2')

    for instance_id in instance_ids:
        instance = ec2.Instance(instance_id)

        try:
            instance.terminate()
        except botocore.exceptions.ClientError as error:
            print('error: %s' % (error.response['Error']['Message']))
            sys.exit(1)
