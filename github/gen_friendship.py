# -*- coding: utf-8 -*-

import requests
import argparse
import json
import time

nodes = []
links = []

CLIENT_ID = "1c6409e7a4219e6dea66"
CLIENT_SECRET = "44636a9d327c1e47aba28a9b50a22b39ac4caeb4"

ROOT_ENDPOINT = "https://api.github.com"
FOLLOWERS_ENDPOINT = ROOT_ENDPOINT + "/users/%s/followers"
FOLLOWING_ENDPOINT = ROOT_ENDPOINT + "/users/%s/following"

headers = {"Accept" : "application/vnd.github.v3+json", "User-Agent" : "stamaimer"}

ratelimit_remaining = "5000"
ratelimit_reset = time.time()

def set_ratelimit_info(headers):

    global ratelimit_remaining

    ratelimit_remaining = headers['X-RateLimit-Remaining']

    global ratelimit_reset

    ratelimit_reset = int(headers['X-RateLimit-Reset'])

def retrieve(url):

    while 1:

        try:

            print "ratelimit_remaining : %s" % ratelimit_remaining

            if '0' == ratelimit_remaining:

                interval = ratelimit_reset - time.time()

                if interval > 0:

                    print "sleeping %f seconds..." % (interval)
                
                    time.sleep(interval)

            print "request : %s" % url

            response = requests.get(url, params = {"client_id" : CLIENT_ID, "client_secret" : CLIENT_SECRET}, headers = headers)

            if 200 == response.status_code:

                print "request : %s success" % url

                return response

            else:

                set_ratelimit_info(response.headers)

                print "request : %s %d" % (url, response.status_code)

                print json.dumps(response.json(), indent = 4)

                if 404 == response.status_code:

                    return None

        except :

            raise

def find_by_name(name):

    for node in nodes:

        if name == node['name']:

            return nodes.index(node)

def get_followers(node):

    name = node["name"]

    group = node["group"]

    response = retrieve(FOLLOWERS_ENDPOINT % name)

    set_ratelimit_info(response.headers)

    if response:

        followers = response.json()

        for user in followers:

            if user["login"] not in [ele["name"] for ele in nodes]:

                tmpu = {"name":user["login"], "group":group + 1}

                nodes.append(tmpu)

                links.append({"source":nodes.index(tmpu), "target":nodes.index(node)})

            else:

                links.append({"source":find_by_name(user["login"]), "target":nodes.index(node)})

def get_following(node):

    name = node["name"]

    group = node["group"]

    response = retrieve(FOLLOWING_ENDPOINT % name)

    set_ratelimit_info(response.headers)

    if response:

        following = response.json()

        for user in following:

            if user["login"] not in [ele["name"] for ele in nodes]:

                tmpu = {"name":user["login"], "group":group + 1}

                nodes.append(tmpu)

                links.append({"source":nodes.index(node), "target":nodes.index(tmpu)})

            else:

                links.append({"source":nodes.index(node), "target":find_by_name(user["login"])})

def start(login, depth):

    nodes.append({"name":login, "group":0})

    for node in nodes:

        if node["group"] > depth:

            print "generate graph ..."

            data = {"nodes":nodes, "links":links}

            with open("github.json", 'w') as outfile:

                json.dump(data, outfile)

            break

        else:

            get_followers(node)
            get_following(node)

if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser(description="")

    argument_parser.add_argument("login", help="")

    argument_parser.add_argument("depth", help="", type=int)

    args = argument_parser.parse_args()

    sed_login = args.login

    max_depth = args.depth

    start(sed_login, max_depth)
