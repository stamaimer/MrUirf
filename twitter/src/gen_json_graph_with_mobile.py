import re
import json
import requests
import argparse

from lxml import html

nodes = []
links = []

HOST = "https://mobile.twitter.com"

FOLLOWING_URL = "https://mobile.twitter.com/%s/following"
FOLLOWERS_URL = "https://mobile.twitter.com/%s/followers"

MXPATH = "//span[@class='username']/text()"

def retrieve(url):

    while 1:

        try:

            print "request : %s" % url

            response = requests.get(url)

            if 200 == response.status_code:

                print "request : %s success" % url

                return response

            else:

                print "request : %s %d" % (url, response.status_code)

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

        return None

def extract_info(content):

    tree = html.fromstring(content)

    count = parse(tree, "//span[@class='count']/text()")

    count = int(count.replace(',', ''))

    members = []

    next = ""

    for i in range(count / 20):

        members.extend(parse(tree, MXPATH))

        next = parse(tree, "//*[@id='main_content']/div/div[2]/div/a/@href")

        response = retrieve(HOST + next)

        tree = html.fromstring(response.content)

    if count % 20 :

        members.extend(parse(tree, MXPATH))

    return members

def get_followers(node):

    name = node["name"]

    group = node["group"]

    response = retrieve(FOLLOWERS_URL % name)

    followers = extract_info(response.content)

    for user in followers:

        if user not in [node["name"] for node in nodes]:

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

    following = extract_info(response.content)

    for user in following:

        if user not in [node["name"] for node in nodes]:

            tmpu = {"name":user, "group":group + 1}

            nodes.append(tmpu)

            links.append({"source":nodes.index(node),
                          "target":nodes.index(tmpu)})

        else:

            links.append({"source":nodes.index(node),
                          "target":find_by_name(user)})

def start(login, depth):

    nodes.append({"name":sed_login, "group":0})

    for node in nodes:

        if node["group"] > max_depth:

            print "generate graph ..."

            data = {"nodes":nodes, "links":links}

            with open("twitter.json", 'w') as outfile:

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
