"""Program entry point and arg parser."""
import argparse
import sys

from . import create
from . import delete
from . import inventory
from . import stop


def main():
    """Entry point for cloud test suite."""
    parser = argparse.ArgumentParser(prog='ec2')
    subparsers = parser.add_subparsers(dest='subcmd')
    subparsers.required = True

    args_create = subparsers.add_parser('create')
    args_create.add_argument('--type',
                             required=True,
                             dest='instance_type',
                             help='Instance type to boot (e.g. t2.large)')
    args_create_group = args_create.add_mutually_exclusive_group(required=True)
    args_create_group.add_argument('--release',
                                   help='Ubuntu release to use')
    args_create_group.add_argument('--ami',
                                   help='AMI to use (e.g. ami-a3d3df39)')

    args_delete = subparsers.add_parser('delete')
    args_delete.add_argument('instance_ids', nargs='+',
                             help='Instance ids to delete')

    args_list = subparsers.add_parser('list')
    args_list.add_argument('tag_filter',
                           nargs='*',
                           help='Owner tag to filter by')
    args_list_group = args_list.add_mutually_exclusive_group()
    args_list_group.add_argument('--csv',
                                 action="store_true",
                                 dest='csv_flag',
                                 help='Output in CSV')
    args_list_group.add_argument('--json',
                                 action="store_true",
                                 dest='json_flag',
                                 help='Output in JSON')

    args_stop = subparsers.add_parser('stop')
    args_stop.add_argument('instance_ids', nargs='+',
                           help='Instance ids to stop')

    args = parser.parse_args()
    cmd = vars(args).pop('subcmd')
    arguments = vars(args)

    return {
        'create': create.create,
        'delete': delete.delete,
        'list': inventory.list_instances,
        'stop': stop.stop,
    }[cmd](**arguments)


if __name__ == "__main__":
    sys.exit(main())
