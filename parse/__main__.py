"""Program entry point and arg parser."""
import argparse

from parse.discover import launch

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser('parse')
    PARSER.add_argument('directory',
                        help='directory with logs to parse')
    ARGS = PARSER.parse_args()

launch(ARGS.directory)
