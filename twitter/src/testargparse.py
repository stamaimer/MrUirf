import argparse

argument_parse = argparse.ArgumentParser()

argument_parse.add_argument('positional_arg', help='')

args = argument_parse.parse_args()


