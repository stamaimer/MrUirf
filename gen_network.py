import requests
import networkx
import argparse
import json
import time



ids = []



nodes = []
links = []



client_id = '1c6409e7a4219e6dea66'

client_secret = '44636a9d327c1e47aba28a9b50a22b39ac4caeb4'

root_endpoint = 'https://api.github.com'

headers = {'Accept' : 'application/vnd.github.v3+json', 'User-Agent' : 'stamaimer'}



followers_endpoint = root_endpoint + '/users/%s/followers'
following_endpoint = root_endpoint + '/users/%s/following'



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



def get_followers(id):

    response = retrieve(followers_endpoint % id['id'])

    set_ratelimit_info(response.headers)

    if response:

        users = response.json()

        for user in users:

            if user['login'] not in [ id['id'] for id in ids ]:

                ids.append({'id':user['login'], 'depth':id['depth'] + 1})

                nodes.append({'name':user['login'], 'group':0})

                links.append({'source':nodes.index({'name':id['id'], 'group':0}), 'target':nodes.index({'name':user['login'], 'group':0})})

            else:

                links.append({'source':nodes.index({'name':id['id'], 'group':0}), 'target':nodes.index({'name':user['login'], 'group':0})})



def get_following(id):

    response = retrieve(following_endpoint % id['id'])

    set_ratelimit_info(response.headers)

    if response:

        users = response.json()

        for user in users:

            if user['login'] not in [ id['id'] for id in ids ]:

                ids.append({'id':user['login'], 'depth':id['depth'] + 1})

                nodes.append({'name':user['login'], 'group':0})

                links.append({'source':nodes.index({'name':user['login'], 'group':0}), 'target':nodes.index({'name':id['id'], 'group':0})})

            else:

                links.append({'source':nodes.index({'name':user['login'], 'group':0}), 'target':nodes.index({'name':id['id'], 'group':0})})



if __name__ == '__main__':

    argument_parser = argparse.ArgumentParser(description='')

    argument_parser.add_argument('id', help='')

    argument_parser.add_argument('depth', help='')

    args = argument_parser.parse_args()

    id = args.id

    max_depth = args.depth

    ids.append({'id':id, 'depth':0})

    nodes.append({'name':id, 'group':0})

    for id in ids:

        if id['depth'] > max_depth:

            graph = {}

            graph['nodes'] = nodes
            graph['links'] = links

            print json.dumps(graph, indent=4)

        else:

            get_followers(id)
            get_following(id)
