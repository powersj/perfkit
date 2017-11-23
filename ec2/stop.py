#!/usr/bin/env python3
"""Stop AWS EC2 instances."""
import sys

import botocore
import boto3


def stop(instance_ids=None):
    """Stop AWS EC2 instances."""
    ec2 = boto3.resource('ec2')

    for instance_id in instance_ids:
        instance = ec2.Instance(instance_id)

        try:
            instance.stop()
        except botocore.exceptions.ClientError as error:
            print('error: %s' % (error.response['Error']['Message']))
            sys.exit(1)
