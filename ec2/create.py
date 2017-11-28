#!/usr/bin/env python3
"""Launch an AWS EC2 Instance."""
import glob
import os
import sys
import time

import botocore
import boto3
import paramiko


def create(instance_type, release, ami):
    """Launch EC2 instance."""
    if not ami:
        ami = get_daily_ubuntu_image_ami(release)

    instance_id = launch_instance(instance_type, ami)
    ip_addr = wait_for_instance(instance_id)
    prep_instance(ip_addr)


def get_daily_ubuntu_image_ami(release):
    """Given a particular OS, find the latest daily image."""
    print('searching for daily AMI of %s' % (release))
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


def launch_instance(instance_type, ami):
    """Launch an instance, return id."""
    print('launching %s with %s' % (instance_type, ami))
    ec2 = boto3.resource('ec2')
    owner_tag = {
        'ResourceType': 'instance',
        'Tags': [
            {
                'Key': 'Owner',
                'Value': os.getlogin(),
            },
        ]
    }

    try:
        instances = ec2.create_instances(MinCount=1, MaxCount=1, ImageId=ami,
                                         KeyName=os.getlogin(),
                                         InstanceType=instance_type,
                                         TagSpecifications=[owner_tag])
    except botocore.exceptions.ClientError as error:
        print('error: %s' % (error.response['Error']['Message']))
        sys.exit(1)

    return instances[0].id


def prep_instance(ip_addr):
    """SSH and upload latest set of test scripts and install dependencies."""
    print('attempting to ssh ubuntu@%s' % (ip_addr))
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    retries = 12
    for _ in range(retries):
        try:
            client.connect(ip_addr, username='ubuntu')
            push_test_scripts(client)
            client.close()
            return
        except (TimeoutError, paramiko.ssh_exception.NoValidConnectionsError):
            time.sleep(10)

    print('error: could not SSH to instance after %s seconds' % (10 * retries))
    sys.exit(1)


def push_test_scripts(client):
    """Push test scripts to system under test."""
    print('pushing test scripts')
    sftp = client.open_sftp()

    test_script_dir = 'bin/'
    for localfile in glob.glob('%s**/*' % test_script_dir, recursive=True):
        remotefile = localfile.replace(test_script_dir, '')
        if os.path.isdir(localfile):
            sftp.mkdir(remotefile)
        else:
            sftp.put(localfile, remotefile)
            sftp.chmod(remotefile, os.stat(localfile).st_mode)

    sftp.close()


def wait_for_instance(instance_id):
    """Wait for instance to get to running state."""
    print('waiting for instance')
    session = boto3.session.Session()
    client = session.client(service_name='ec2')

    retries = 12
    for _ in range(retries):
        response = client.describe_instance_status(InstanceIds=[instance_id])

        try:
            state = response['InstanceStatuses'][0]['InstanceState']['Name']

            print(state)
            if state == 'pending':
                time.sleep(10)
                continue
            else:
                ec2 = boto3.resource('ec2')
                instance = ec2.Instance(instance_id)
                return instance.public_ip_address

        except IndexError:
            time.sleep(10)
            continue

    print('error: instance is not in running state after %s seconds' %
          (retries * 10))
    sys.exit(1)
