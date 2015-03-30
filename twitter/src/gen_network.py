import json
import time
import numpy
import oauth
import requests
import networkx
import argparse

from networkx.readwrite import json_graph

tasks = []

nodes = []
links = []

CONSUMER_KEY = "6s35FXsv4jD2ar0ZlDYjnt7jZ"
CONSUMER_SECRET = "oFAlNZr6JGHwCdYGrYNfS3plUSdxg8UlEP2RtiKg59uSYahWRk"

FOLLOWING_URL = "https://api.twitter.com/1.1/friends/list.json"
FOLLOWERS_URL = "https://api.twitter.com/1.1/followers/list.json"

headers = {"Authorization" : 'Bearer ' + oauth.get_bearer_token(CONSUMER_KEY,
                                                                CONSUMER_SECRET)}

ratelimit_remaining = '30'
ratelimit_reset = time.time()

def set_ratelimit_info(headers):

    global ratelimit_remaining

    ratelimit_remaining = headers['X-Rate-Limit-Remaining']

    global ratelimit_reset

    ratelimit_reset = int(headers['X-Rate-Limit-Reset'])

def retrieve(url, params):

    while 1:

        try:

            print 'ratelimit_remaining : %s' % ratelimit_remaining

            if '0' == ratelimit_remaining:

                print 'sleeping %f seconds...' % (ratelimit_reset - time.time())

                time.sleep(ratelimit_reset - time.time())

            print 'request : %s' % url

            response = requests.get(url, params = params, headers = headers)

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

        if node["name"] == name:

            return nodes.index(node)

def get_followers(task):

    name = task['name']

    depth = task['depth']

    params = {'screen_name':name, 'cursor':-1, 'count':200, 'skip_status':"true", 'include_user_entities':'false'} 

    response = retrieve(FOLLOWERS_URL, params)

    set_ratelimit_info(response.headers)

    followers = response.json()["users"]

    while 0 != response.json()["next_cursor"]:

        params["cursor"] = response.json()["next_cursor"]

        response = retrieve(FOLLOWERS_URL, params)

        set_ratelimit_info(response.headers)

        followers.extend(response.json()["users"])

    for user in followers:

        if user["screen_name"] not in [task["name"] for task in tasks]:

            tasks.append({"name":user["screen_name"], "depth":depth + 1})

            nodes.append({"name":user["screen_name"], "group":depth + 1})

            links.append({"source":nodes.index({"name":user["screen_name"], "group":depth + 1}),
                          "target":nodes.index({"name":name, "group":depth})})

        else:

            links.append({"source":find_by_name(user["screen_name"]),
                          "target":nodes.index({"name":name, "group":depth})})

def get_following(task):

    name = task['name']

    depth = task['depth']

    params = {'screen_name':name, 'cursor':-1, 'count':200, 'skip_status':"true", 'include_user_entities':'false'} 

    response = retrieve(FOLLOWING_URL, params)

    set_ratelimit_info(response.headers)

    following = response.json()["users"]

    while 0 != response.json()["next_cursor"]:

        params["cursor"] = response.json()["next_cursor"]

        response = retrieve(FOLLOWING_URL, params)

        set_ratelimit_info(response.headers)

        following.extend(response.json()["users"])

    for user in following:

        if user["screen_name"] not in [task["name"] for task in tasks]:

            tasks.append({"name":user["screen_name"], "depth":depth + 1})

            nodes.append({"name":user["screen_name"], "group":depth + 1})

            links.append({"source":nodes.index({"name":name, "group":depth}),
                          "target":nodes.index({"name":user["screen_name"], "group":depth} + 1)})

        else:

            links.append({"source":nodes.index({"name":name, "group":depth}),
                          "target":find_by_name(user["screen_name"])})

if __name__ == "__main__":

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
