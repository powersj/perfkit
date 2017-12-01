"""Program entry point and arg parser."""
import argparse
import sys

from . import delete
from . import inventory
from . import launch
from . import stop


def main():
    """Entry point for cloud test suite."""
    parser = argparse.ArgumentParser(prog='ec2')
    subparsers = parser.add_subparsers(dest='subcmd')
    subparsers.required = True

    arg_create = subparsers.add_parser('launch')
    arg_create.add_argument('instance_type',
                            help='instance type to boot e.g. t2.micro')
    arg_create_group = arg_create.add_mutually_exclusive_group()
    arg_create_group.add_argument('--release',
                                  help='ubuntu release to use, default: LTS')
    arg_create_group.add_argument('--ami',
                                  help='AMI to use e.g. ami-a3d3df39')

    arg_delete = subparsers.add_parser('delete')
    arg_delete.add_argument('instance_ids', nargs='+',
                            help='instance ids to delete')

    arg_list = subparsers.add_parser('list')
    arg_list.add_argument('tag_filter', nargs='*',
                          help='owner tag to filter by')
    arg_list_group = arg_list.add_mutually_exclusive_group()
    arg_list_group.add_argument('--csv', action='store_true', dest='csv_out',
                                help='output in CSV')
    arg_list_group.add_argument('--json', action='store_true', dest='json_out',
                                help='output in JSON')

    arg_stop = subparsers.add_parser('stop')
    arg_stop.add_argument('instance_ids', nargs='+',
                          help='instance ids to stop')

    args = parser.parse_args()
    cmd = vars(args).pop('subcmd')
    arguments = vars(args)

    return {
        'delete': delete.delete,
        'launch': launch.launch,
        'list': inventory.list_instances,
        'stop': stop.stop,
    }[cmd](**arguments)


if __name__ == "__main__":
    sys.exit(main())
