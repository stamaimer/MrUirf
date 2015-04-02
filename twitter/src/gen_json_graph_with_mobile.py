import re
import json
import numpy
import requests
import networkx
import argparse

from lxml import html

from networkx.readwrite import json_graph

tasks = []

nodes = []
links = []

host = "https://mobile.twitter.com"

FOLLOWING_URL = "https://mobile.twitter.com/%s/following"
FOLLOWERS_URL = "https://mobile.twitter.com/%s/followers"

def retrieve(url):

    while 1:

        try:

            print 'request : %s' % url

            response = requests.get(url)

            if 200 == response.status_code:

                print 'request : %s success' % url

                return response

            else:

                print 'request : %s %d' % (url, response.status_code)

                if 404 == response.status_code:

                    return None

        except :

            raise

def find_by_name(name):

    for node in nodes:

        if node["name"] == name:

            return nodes.index(node)

def parse(tree, xpath, regex = '.*'):

    nodes = tree.xpath(xpath)

    if 1 == len(nodes):

        node = nodes[0].encode('utf-8')

        matches = re.search(regex, node)

        if matches:

            match = matches.group(0)

            return match

        else:

            print 'There is something wrong in regex match'

    elif len(nodes) > 1:

        return nodes[1:]

    else:

        print 'There is something wrong in xpath match'

def extract_info(response):

    tree = html.fromstring(response)

    count = parse(tree, "//span[@class='count']/text()")

    count = int(count.replace(',', ''))

    members = []

    next = ""

    for i in range(count / 20):

        members.extend(parse(tree, "//span[@class='username']/text()"))

        next = parse(tree, '//*[@id="main_content"]/div/div[2]/div/a/@href')

        response = retrieve(host + next)

        tree = html.fromstring(response.content)

    if count % 20 :

        members.extend(parse(tree, "//span[@class='username']/text()"))

    return members

def get_followers(task):

    name = task['name']

    depth = task['depth']

    response = retrieve(FOLLOWERS_URL % name)

    followers = extract_info(response.content)

    for user in followers:

        if user not in [task["name"] for task in tasks]:

            tasks.append({"name":user, "depth":depth + 1})

            nodes.append({"name":user, "group":depth + 1})

            links.append({"source":nodes.index({"name":user, "group":depth + 1}),
                          "target":nodes.index({"name":name, "group":depth})})

        else:

            links.append({"source":find_by_name(user),
                          "target":nodes.index({"name":name, "group":depth})})

def get_following(task):

    name = task['name']

    depth = task['depth']

    response = retrieve(FOLLOWING_URL % name)

    following = extract_info(response.content)

    for user in following:

        if user not in [task["name"] for task in tasks]:

            tasks.append({"name":user, "depth":depth + 1})

            nodes.append({"name":user, "group":depth + 1})

            links.append({"source":nodes.index({"name":name, "group":depth}),
                          "target":nodes.index({"name":user, "group":depth + 1})})

        else:

            links.append({"source":nodes.index({"name":name, "group":depth}),
                          "target":find_by_name(user)})

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

            data = {"nodes":nodes, "links":links}

            with open('twitter.json', 'w') as outfile:

                json.dump(data, outfile)

            break;

        else:

            get_followers(task)
            get_following(task)
