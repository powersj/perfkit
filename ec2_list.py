#!/usr/bin/env python3
"""List AWS EC2 Instances in various formats."""
import argparse
import json

import boto3
from tabulate import tabulate


class Ec2Instance(object):
    """Generic EC2 Instance Class."""

    def __init__(self, instance):
        """Init class."""
        self.instance_id = instance.id
        self.type = instance.instance_type
        self.state = instance.state['Name']
        self.ami = instance.image.id
        self.ip_public = instance.public_ip_address
        self.ip_private = instance.private_ip_address
        self.owner = self._determine_owner(instance.tags)

    @staticmethod
    def _determine_owner(tags):
        """Determine owner of the instance based on tags."""
        if not tags:
            return ''

        owner = ''
        for tag in tags:
            if tag['Key'] == 'Owner':
                owner = tag['Value']

        return owner

    def __str__(self):
        """Table format."""
        return('%s %s %s %s %s %s %s' %
               (self.instance_id, self.type, self.state, self.ami,
                self.ip_public, self.ip_private, self.owner))

    def to_csv(self):
        """Object as valid csv string."""
        return('%s,%s,%s,%s,%s,%s,%s' %
               (self.instance_id, self.type, self.state, self.ami,
                self.ip_public, self.ip_private, self.owner))

    def to_json(self):
        """Object as json-like object to be used with json.dumps."""
        return {
            "id": self.instance_id,
            "type": self.type,
            "state": self.state,
            "ami": self.ami,
            "ip_public": self.ip_public,
            "ip_private": self.ip_private,
            "owner": self.owner
        }


def ec2_list_instances(tag_filter=None, csv_flag=False, json_flag=False):
    """List all EC2 instances."""
    ec2 = boto3.resource('ec2')

    if tag_filter:
        results = ec2.instances.filter(
            Filters=[{'Name': 'tag-value', 'Values': tag_filter}])
    else:
        results = ec2.instances.all()

    instances = []
    for result in results:
        instances.append(Ec2Instance(result))

    instances = sorted(instances, key=lambda d: (d.state, d.owner, d.type))

    if csv_flag:
        print('id,type,state,ami,ip_public,ip_private,owner')
        print('\n'.join([instance.to_csv() for instance in instances]))
    elif json_flag:
        print(json.dumps([instance.to_json() for instance in instances],
                         indent=4))
    else:
        table = []
        for instance in instances:
            table.append(str(instance).split(' '))
        print(tabulate(table, headers=['id', 'type', 'state', 'ami',
                                       'ip_public', 'ip_private', 'owner']))


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('filter', nargs='*', help='Owner tag to filter by')

    GROUP = PARSER.add_mutually_exclusive_group()
    GROUP.add_argument('--csv', action="store_true", help='Output in CSV')
    GROUP.add_argument('--json', action="store_true", help='Output in JSON')

    ARGS = PARSER.parse_args()
    ec2_list_instances(ARGS.filter, ARGS.csv, ARGS.json)
