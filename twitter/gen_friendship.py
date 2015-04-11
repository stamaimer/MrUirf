# -*- coding: utf-8 -*-

import os
import re
import gc
import time
import json
import session
import argparse
import itertools
from lxml import html

requester = session.get_session()

nodes = []
links = []

HOST = "https://mobile.twitter.com"

FOLLOWING_URL = HOST + "/%s/following"
FOLLOWERS_URL = HOST + "/%s/followers"

MXPATH = "//span[@class='username']/text()"

def retrieve(url):

    while 1:

        try:

            print "request : %s" % url

            time.sleep(0.1)

            response = requester.get(url)

            if 200 == response.status_code:

                print "request : %s success" % response.url

                return response

            else:

                print "request : %s %d" % (response.url, response.status_code)

                if 404 == response.status_code:#anything else?

                    return None
                
        except :

            raise

def find_by_name(name):

    for node in nodes:

        if node["name"] == name:

            return nodes.index(node)

def parse(tree, xpath):

    nodes = tree.xpath(xpath)

    if 1 == len(nodes):#for count and cursor

        return nodes[0]

    elif len(nodes) > 1:#for username

        return nodes[1:]

    else:#something wrong

        print "something wrong in parse"

        return ''

def extract_info(content):

    tree = html.fromstring(content)

    count = parse(tree, "//span[@class='count']/text()")

    members = itertools.chain()

    try:

        count = int(count.replace(',', ''))

    except:

        return members

    if count >= 10000:

        return members

    next = ""

    for i in xrange(int(count / 20)):

        members = itertools.chain(members, parse(tree, MXPATH))

        next = parse(tree, "//*[@id='main_content']/div/div[2]/div/a/@href")

        response = retrieve(HOST + next)

        tree = html.fromstring(response.content)

    if count % 20 :

        members = itertools.chain(members, parse(tree, MXPATH))

    return members

def get_followers(node):

    name = node["name"]

    group = node["group"]

    response = retrieve(FOLLOWERS_URL % name)

    if response:

        followers = extract_info(response.content)

        del response

        for user in followers:

            if user not in (ele["name"] for ele in nodes):

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

    response = retrieve(FOLLOWING_URL % name)

    if response:

        following = extract_info(response.content)

        del response

        for user in following:

            if user not in (ele["name"] for ele in nodes):

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

            with open(login + ".json", 'w') as outfile:

                json.dump(data, outfile)

            return os.path.abspath( login + ".json")

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
