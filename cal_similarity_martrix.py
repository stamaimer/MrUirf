import numpy
import argparse

if __name__ == '__main__':

    argument_parser = argparse.ArgumentParser(description='')

    argument_parser.add_argument('path2adjmatg', help='')
    argument_parser.add_argument('path2adjmatt', help='')

    args = argument_parser.parse_args()

    path2adjmatg = args.path2adjmatg
    path2adjmatt = args.path2adjmatt


