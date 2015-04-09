# -*- coding: utf-8 -*-

import os
import json
import time
import oauth
import requests
import argparse

import sys

sys.path.append("../")

import session

requester = session.get_session()

nodes = []
links = []

sleep_count = 0

CONSUMER_KEY = "6s35FXsv4jD2ar0ZlDYjnt7jZ"
CONSUMER_SECRET = "oFAlNZr6JGHwCdYGrYNfS3plUSdxg8UlEP2RtiKg59uSYahWRk"

LOOKUP_URL = "https://api.twitter.com/1.1/users/lookup.json"

FOLLOWING_URL = "https://api.twitter.com/1.1/friends/ids.json"
FOLLOWERS_URL = "https://api.twitter.com/1.1/followers/ids.json"

headers = {"Authorization" : "Bearer " + oauth.get_bearer_token(CONSUMER_KEY, CONSUMER_SECRET)}

ratelimit_remaining = "30"
ratelimit_reset = time.time()

def set_ratelimit_info(headers):

    global ratelimit_remaining

    ratelimit_remaining = headers["X-Rate-Limit-Remaining"]

    global ratelimit_reset

    ratelimit_reset = int(headers["X-Rate-Limit-Reset"])

def retrieve(url, params):

    while 1:

        try:

            print "ratelimit_remaining : %s" % ratelimit_remaining

            if '0' == ratelimit_remaining:

                interval = ratelimit_reset - time.time()

                if interval > 0:

                    global sleep_count

                    sleep_count += 1

                    print "the %d times sleep, sleeping %f seconds..." % (sleep_count, interval)

                    time.sleep(interval)

            print "request : %s" % url

            response = requester.get(url, params = params, headers = headers)

            if 200 == response.status_code:

                print "request : %s success" % url

                return response

            else:

                set_ratelimit_info(response.headers)

                print "request : %s %d" % (response.url, response.status_code)

                print json.dumps(response.json(), indent = 4)

                if 404 == response.status_code:

                    return None

        except :

            raise

def find_by_name(name):

    for node in nodes:

        if node["name"] == name:

            return nodes.index(node)

def get_followers(node):

    name = node["name"]

    group = node["group"]

    params = {"user_id":name, "cursor":-1, "count":5000, "stringify_ids":"true"} 

    response = retrieve(FOLLOWERS_URL, params)

    set_ratelimit_info(response.headers)

    followers = response.json()["ids"]

    while 0 != response.json()["next_cursor"]:

        params["cursor"] = response.json()["next_cursor"]

        response = retrieve(FOLLOWERS_URL, params)

        set_ratelimit_info(response.headers)

        followers.extend(response.json()["ids"])

    for user in followers:

        if user not in [ele["name"] for ele in nodes]:

            tmpu = {"name":user, "group":group + 1}

            nodes.append(tmpu)

            links.append({"source":nodes.index(tmpu),
                          "target":nodes.index(node)})

        else:

            links.append({"source":find_by_name(user),
                          "target":nodes.index(node)})

def get_following(node):

    name = node["name"]

    group = node["group"]

    params = {"user_id":name, "cursor":-1, "count":5000, "stringify_ids":"true"} 

    response = retrieve(FOLLOWING_URL, params)

    set_ratelimit_info(response.headers)

    following = response.json()["ids"]

    while 0 != response.json()["next_cursor"]:

        params["cursor"] = response.json()["next_cursor"]

        response = retrieve(FOLLOWING_URL, params)

        set_ratelimit_info(response.headers)

        following.extend(response.json()["ids"])

    for user in following:

        if user not in [ele["name"] for ele in nodes]:

            tmpu = {"name":user, "group":group + 1}

            nodes.append(tmpu)

            links.append({"source":nodes.index(node),
                          "target":nodes.index(tmpu)})

        else:

            links.append({"source":nodes.index(node),
                          "target":find_by_name(user)})

def start(login, depth):

    nodes.append({"name":login, "group":0})

    for node in nodes:

        if node["group"] > depth:

            print "generate graph ..."

            data = {"nodes":nodes, "links":links}

            with open("twitter.json", 'w') as outfile:

                json.dump(data, outfile)

            return os.path.abspath("twitter.json")

        else:

            get_followers(node)
            get_following(node)

def get_user_id(name):

    params = {"screen_name":name, "include_entities":"false"}
    
    response = retrieve(LOOKUP_URL, params)

    print response.json()[0]["id_str"]

    return response.json()[0]["id_str"]

if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser(description="")

    argument_parser.add_argument("login", help="")

    argument_parser.add_argument("depth", help="", type=int)

    args = argument_parser.parse_args()

    sed_login = args.login

    max_depth = args.depth

    start(sed_login, max_depth)
