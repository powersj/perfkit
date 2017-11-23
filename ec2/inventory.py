#!/usr/bin/env python3
"""List AWS EC2 Instances in various formats."""
import json

import boto3
from tabulate import tabulate

from .instance import Ec2Instance


def list_instances(tag_filter=None, csv_flag=False, json_flag=False):
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
