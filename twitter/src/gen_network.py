import json
import time
import numpy
import urllib
import base64
import requests
import networkx
import argparse

from networkx.readwrite import json_graph

tasks = []

nodes = []
links = []

CONSUMER_KEY = "6s35FXsv4jD2ar0ZlDYjnt7jZ"
CONSUMER_SECRET = "oFAlNZr6JGHwCdYGrYNfS3plUSdxg8UlEP2RtiKg59uSYahWRk"

BEARER_TOKEN_URL = "https://api.twitter.com/oauth2/token"

ratelimit_remaining = ''
ratelimit_reset = time.time()

def urlencode(str):

    return urllib.quote(str, "")

def b64encode(str):

    return base64.b64encode(str)

def get_bearer_token(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET):

    bearer_token_credentials = ':'.join([urlencode(consumer_key), urlencode(consumer_secret)])

    b64encoded_bearer_token_credentials = b64encode(bearer_token_credentials)

    headers, payload = {}, {}

    headers["Authorization"] = "Basic " + b64encoded_bearer_token_credentials

    headers["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8"

    payload["grant_type"] = "client_credentials"

    response = requests.post(BEARER_TOKEN_URL, headers=headers, data=payload)

    if 200 == response.status_code:

        return response.json()["access_token"]

    else:

        print response.status_code, response.json()

        return None

if __name__ == "__main__":

    print get_bearer_token()

    argument_parser = argparse.ArgumentParser(description="")

    argument_parser.add_argument('login', help='')

    argument_parser.add_argument('depth', help='', type=int)

    args = argument_parser.parse_args()

    sed_login = args.login

    max_depth = args.depth

    tasks.append({'name':sed_login, 'depth':0})

    nodes.append({'name':sed_login, 'group':0})

    for task in tasks:

        if task['depth'] > max_depth:

            print 'generate graph ...'

            tmp = []

            for i in range(len(nodes)):

                if nodes[i]['group'] == max_depth + 1:

                    tmp.append(nodes[i])

                    for link in links:

                        if link['target'] == i or link['source'] == i:

                            links.remove(link)

            for item in tmp:

                nodes.remove(item)

            data = {}

            data['nodes'] = nodes
            data['links'] = links

            with open('graph.json', 'w') as outfile:

                json.dump(data, outfile)

            graph = json_graph.node_link_graph(data, directed=True, multigraph=False)

            numpy.set_printoptions(threshold='nan')

            print networkx.to_numpy_matrix(graph)

            break;

        else:

            get_followers(task)
            get_following(task)
