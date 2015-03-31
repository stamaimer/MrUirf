import requests
import networkx
import argparse
import numpy
import json
import time

from networkx.readwrite import json_graph

tasks = []

nodes = []
links = []

client_id = '1c6409e7a4219e6dea66'
client_secret = '44636a9d327c1e47aba28a9b50a22b39ac4caeb4'

root_endpoint = 'https://api.github.com'
followers_endpoint = root_endpoint + '/users/%s/followers'
following_endpoint = root_endpoint + '/users/%s/following'

headers = {'Accept' : 'application/vnd.github.v3+json', 'User-Agent' : 'stamaimer'}

ratelimit_remaining = '5000'
ratelimit_reset = time.time()

def set_ratelimit_info(headers):

    global ratelimit_remaining

    ratelimit_remaining = headers['X-RateLimit-Remaining']

    global ratelimit_reset

    ratelimit_reset = int(headers['X-RateLimit-Reset'])

def retrieve(url):

    while 1:

        try:

            print 'ratelimit_remaining : %s' % ratelimit_remaining

            if '0' == ratelimit_remaining:

                print 'sleeping %f seconds...' % (ratelimit_reset - time.time())

                time.sleep(ratelimit_reset - time.time())

            print 'request : %s' % url

            response = requests.get(url, params = {'client_id' : client_id, 'client_secret' : client_secret}, headers = headers)

            if 200 == response.status_code:

                print 'request : %s success' % url

                return response

            else:

                set_ratelimit_info(response.headers)

                print 'request : %s %d' % (url, response.status_code)

                print json.dumps(response.json(), indent = 4)

                if 404 == response.status_code:

                    return None

        except requests.exceptions.ConnectionError:

            print 'requests.exceptions.ConnectionError'

def find_by_name(name):

    for node in nodes:

        if name == node['name']:

            return nodes.index(node)

def get_followers(task):

    name = task['name']

    depth = task['depth']

    response = retrieve(followers_endpoint % name)

    set_ratelimit_info(response.headers)

    if response:

        followers = response.json()

        for user in followers:

            if user['login'] not in [task['name'] for task in tasks]:

                tasks.append({'name':user['login'], 'depth':depth + 1})

                nodes.append({'name':user['login'], 'group':depth + 1})

                links.append({'source':nodes.index({'name':user['login'], 'group':depth + 1}), 'target':nodes.index({'name':name, 'group':depth})})

            else:

                links.append({'source':find_by_name(user['login']), 'target':nodes.index({'name':name, 'group':depth})})

def get_following(task):

    name = task['name']

    depth = task['depth']

    response = retrieve(following_endpoint % name)

    set_ratelimit_info(response.headers)

    if response:

        following = response.json()

        for user in following:

            if user['login'] not in [task['name'] for task in tasks]:

                tasks.append({'name':user['login'], 'depth':depth + 1})

                nodes.append({'name':user['login'], 'group':depth + 1})

                links.append({'source':nodes.index({'name':name, 'group':depth}), 'target':nodes.index({'name':user['login'], 'group':depth + 1})})

            else:

                links.append({'source':nodes.index({'name':name, 'group':depth}), 'target':find_by_name(user['login'])})

if __name__ == '__main__':

    argument_parser = argparse.ArgumentParser(description='')

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

            for link in links[:]:

                if {"source":link["target"], "target":link["source"]} not in links:

                    links.remove(link)

            graph = json_graph.node_link_graph({"nodes":nodes, "links":links}, directed=False, multigraph=False)

            graphs = list(networkx.connected_component_subgraphs(graph))

            numpy.set_printoptions(threshold='nan')

            for graph in graphs:

                if 0 in graph.nodes():

                    nodes = [node for node in nodes if nodes.index(node) in graph.nodes()]

                    links = [{"source":link[0], "target":link[1]} for link in networkx.to_edgelist(graph)]

                    print networkx.to_numpy_matrix(graph)

            data = {}

            data['nodes'] = nodes
            data['links'] = links

            with open('graph.json', 'w') as outfile:

                json.dump(data, outfile)

            break

        else:

            get_followers(task)
            get_following(task)
