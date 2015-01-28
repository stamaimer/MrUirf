import requests
import networkx
import argparse
import json
import time

ids = []

nodes = []
links = []

def get_followers(id):

    pass

def get_following(id):

    pass 

if __name__ == '__main__':

    argument_parser = argparse.ArgumentParser(description='')

    argument_parser.add_argument('-i', 'id', help='')

    argument_parser.add_argument('-d', 'depth', help='')

    args = argument_parser.parse_args()

    id = args.id

    max_depth = args.depth

    ids.append({'id':id, 'depth':0})

    for id in ids:

        if id['depth'] > max_depth:

            pass

        else:

            get_followers(id)
            get_following(id)
