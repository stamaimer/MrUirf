# -*- coding: utf-8 -*-

import os
import json
import session
import argparse
import itertools
from lxml import html

nodes = []
links = []

requester = session.get_session()

percent, group1, group2 = 0.0, 0, 0

HOST = "https://mobile.twitter.com"

HOMEPAGES_URL = HOST + "/%s"
FOLLOWING_URL = HOST + "/%s/following"
FOLLOWERS_URL = HOST + "/%s/followers"

VXPATH = "//a[@class='badge']/img"
CXPATH = "//div[@class='statnum']/text()"
MXPATH = "//span[@class='username']/text()"
NXPATH = "//*[@id='main_content']/div/div[2]/div/a/@href"

def retrieve(url):

    while 1:

        try:

            # print "request : %s" % url

            response = requester.get(url)

            if 200 == response.status_code:

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

    nodes = tree.xpath(xpath, smart_strings=False)

    if 1 == len(nodes):#for count and cursor

        return nodes

    elif len(nodes) > 1:#for name list

        return nodes[1:]

    else:#something wrong

        return [None]

def extract_info(response):

    tree = html.fromstring(response.content)

    members = itertools.chain()

    members = itertools.chain(members, parse(tree, MXPATH))

    next = parse(tree, NXPATH)[0]

    while next:

        response = retrieve(HOST + next)

        tree = html.fromstring(response.content)

        members = itertools.chain(members, parse(tree, MXPATH))

        next = parse(tree, NXPATH)[0]

    return members

def get_followers(node):

    name = node["name"]

    group = node["group"]

    response = retrieve(FOLLOWERS_URL % name)

    if response:

        followers = extract_info(response)

        return followers

        # for user in followers:

        #     for i in xrange(group + 1):

        #         if {"name":user, "group":i} in nodes:

        #             links.append({"source":find_by_name(user), "target":nodes.index(node)})

        #             break

        #     tmpu = {"name":user, "group":group + 1}

        #     nodes.append(tmpu)

        #     links.append({"source":nodes.index(tmpu), "target":nodes.index(node)})

def get_following(node):

    name = node["name"]

    group = node["group"]

    response = retrieve(FOLLOWING_URL % name)

    if response:

        following = extract_info(response)

        return following

        # for user in following:

        #     for i in xrange(group + 1):

        #         if {"name":user, "group":i} in nodes:

        #             links.append({"source":nodes.index(node), "target":find_by_name(user)})

        #             break

        #     tmpu = {"name":user, "group":group + 1}

        #     nodes.append(tmpu)

        #     links.append({"source":nodes.index(node), "target":nodes.index(tmpu)})

def is_valid(name):

    response = retrieve(HOMEPAGES_URL % name)

    if response:

        tree = html.fromstring(response.content)

        verify = parse(tree, VXPATH)[0]

        if verify:

            return False

        else:

            count = parse(tree, CXPATH)

            following_count = int(count[0].replace(',', ''))
            followers_count = int(count[1].replace(',', ''))

            if followers_count >= 6000 or following_count >= 6000 or following_count == 2001 or following_count * 10 < followers_count:

                return False

            else:

                return True

    else:

        return False

def start(login, depth):

    nodes.append({"name":login, "group":0})

    for node in nodes:

        name = node["name"]

        group = node["group"]

        if group > depth:

            print "generate graph ..."

            data = {"nodes":nodes, "links":links}

            with open(login + "_twitter.json", 'w') as outfile:

                json.dump(data, outfile)

            return os.path.abspath( login + "_twitter.json")

        else:

            global percent, group1, group2

            if 0 == group:

                percent = 1

            elif 1 == group:

                if not group1:

                    group1 = sum(( 1 for ele in nodes if ele["group"] == 1 ))

                percent = nodes.index(node) / float(group1)

            elif 2 == group:

                if not group2:

                    group2 = sum(( 1 for ele in nodes if ele["group"] == 2 ))

                percent = (nodes.index(node) - group1) / float(group2)

            print "name : %s, group : %d, percent : %f" % (name, group, percent)

            if is_valid(name):

                following = get_following(node)
                followers = get_followers(node)

                intersection = set(following).intersection(followers)

                for user in intersection:

                    for i in xrange(group + 1):

                        if {"name":user, "group":i} in nodes:

                            break

                    else:

                        tmpu = {"name":user, "group":group + 1}

                        nodes.append(tmpu)

                        links.append({"source":nodes.index(node), "target":nodes.index(tmpu)})
                        links.append({"source":nodes.index(tmpu), "target":nodes.index(node)})

            else:

                print "%s is invalid" % name

if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser(description="")

    argument_parser.add_argument("login", help="")

    argument_parser.add_argument("depth", help="", type=int)

    args = argument_parser.parse_args()

    sed_login = args.login

    max_depth = args.depth

    start(sed_login, max_depth)
