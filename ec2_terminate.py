#!/usr/bin/env python3
"""Terminate AWS EC2 instances."""
import argparse
import sys

import botocore
import boto3


def ec2_delete_instances(instance_ids=None):
    """Terminate AWS EC2 instances."""
    ec2 = boto3.resource('ec2')

    for instance_id in instance_ids:
        instance = ec2.Instance(instance_id)

        try:
            instance.terminate()
        except botocore.exceptions.ClientError as error:
            print('error: %s' % (error.response['Error']['Message']))
            sys.exit(1)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('instance_id', nargs='+',
                        help='Instance ids to delete')

    ARGS = PARSER.parse_args()
    ec2_delete_instances(ARGS.instance_id)
