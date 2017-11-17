#!/usr/bin/env python3
"""Launch an AWS EC2 Instances."""
import argparse
import os
import sys
import time

import botocore
import boto3


def find_ubuntu_daily_image(release):
    """Given a particular OS, find the latest daily image."""
    image_filter = ('ubuntu/images-testing/hvm-ssd/'
                    'ubuntu-%s-daily-amd64-server-*' % (release))

    session = boto3.session.Session()
    client = session.client(service_name='ec2')
    response = client.describe_images(Filters=[{'Name': 'name',
                                                'Values': [image_filter]}])
    images = sorted(response['Images'], key=lambda k: k['CreationDate'])

    try:
        return images[-1]['ImageId']
    except IndexError:
        print('error: cannot find daily image for "%s"' % (release))
        sys.exit(1)


def wait_for_instance(instance_id):
    """Wait for instance to get to running state."""
    timeout = 120
    session = boto3.session.Session()
    client = session.client(service_name='ec2')

    for _ in range(int(timeout / 10)):
        time.sleep(10)

        response = client.describe_instance_status(InstanceIds=[instance_id])
        try:
            state = response['InstanceStatuses'][0]['InstanceState']['Name']
        except IndexError:
            continue

        if state == 'pending':
            continue
        else:
            return

    print('error: instance not up after %s seconds' % (timeout))


def create_instance(instance_type, ami, key, owner):
    """Launch an instance, return id."""
    owner_tag = {
        'ResourceType': 'instance',
        'Tags': [
            {
                'Key': 'Owner',
                'Value': owner,
            },
        ]
    }

    ec2 = boto3.resource('ec2')
    try:
        instances = ec2.create_instances(MinCount=1, MaxCount=1, ImageId=ami,
                                         KeyName=key,
                                         InstanceType=instance_type,
                                         TagSpecifications=[owner_tag])
    except botocore.exceptions.ClientError as error:
        print('error: %s' % (error.response['Error']['Message']))
        sys.exit(1)

    return instances[0].id


def wait_for_ssh(instance_id):
    """Wait for SSH to become ready."""
    ...


def prep_instance(ip, key):
    """Upload latest set of test scripts and install dependencies.

    Essentially runs:
    rsync --verbose --recursive -e "ssh -i keys/$KEY.pem
        -o StrictHostKeyChecking=no" ./bin/* "$USER"@"$IP":~
    ssh install_deps.sh
    """
    ...


def ec2_launch_instance(instance_type, release, ami, key, owner):
    """Launch EC2 instance."""
    owner = owner if owner else os.getlogin()
    key = key if key else os.getlogin()
    ami = ami if ami else find_ubuntu_daily_image(release)

    instance_id = create_instance(instance_type, ami, key, owner)
    print(instance_id)
    wait_for_instance(instance_id)
    ip = wait_for_ssh(instance_id)
    print(ip)
    prep_instance(ip, key)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('--type', required=True,
                        help='Instance type to boot (e.g. t2.large)')

    GROUP = PARSER.add_mutually_exclusive_group(required=True)
    GROUP.add_argument('--release', help='Ubuntu release to find daily AMI')
    GROUP.add_argument('--ami', help='AMI number to use (e.g. ami-a3d3df39)')

    PARSER.add_argument('--key',
                        help='Keyname to use on instance; defaults to $USER')
    PARSER.add_argument('--owner',
                        help='Owner to tag instance with; defaults to $USER')

    ARGS = PARSER.parse_args()
    ec2_launch_instance(ARGS.type, ARGS.release, ARGS.ami, ARGS.key,
                        ARGS.owner)
