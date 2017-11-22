"""Program entry point and arg parser."""
import argparse
import os

from parse.discover import launch

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser('parse')
    PARSER.add_argument('directory',
                        help='path to project logs to parse (e.g. logs/cloud')
    ARGS = PARSER.parse_args()

launch(os.path.abspath(ARGS.directory))
