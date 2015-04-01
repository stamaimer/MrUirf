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

        print node

        matches = re.search(regex, node)

        if matches:

            match = matches.group(0)

            print match

            return match

        else:

            print 'There is something wrong in regex match'
    else:

        print 'There is something wrong in xpath match'

def extract_info(response):

    tree = html.fromstring(response)

    count = parse(tree, '//*[@id="main_content"]/div/div[1]/table/tbody/tr[2]/td/span/text()')

    count = int(count)

    members = []

    next = ""

    for i in range(count / 20):

        for j in range(20):

            members.append(parse(tree, '//*[@id="main_content"]/div/div[2]/table[%d]/tbody/tr[2]/td/a/span/text()' % j))

        next = parse(tree, '//*[@id="main_content"]/div/div[2]/div/a/@href')

        response = retrieve(host + next)

        tree = html.fromstring((response))

    if next:

        for i in range(count % 20):

            members.append(parse(tree, '//*[@id="main_content"]/div/div[2]/table[%d]/tbody/tr[2]/td/a/span/text()' % i))

        return members

    else:

        return members

def get_followers(task):

    name = task['name']

    depth = task['depth']

    response = retrieve(FOLLOWERS_URL % name)

    followers, next = extract_info(response)

    while next :

        response = retrieve(host + next)

        tmp, next = extract_info(response)

        followers.extend(tmp)

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

    response = retrieve(FOLLOWING_URL % name)

    following, next = extract_info(response)

    while next :

        response = retrieve(host + next)

        tmp, next = extract_info(response)

        following.extend(tmp)

    for user in following:

        if user["screen_name"] not in [task["name"] for task in tasks]:

            tasks.append({"name":user["screen_name"], "depth":depth + 1})

            nodes.append({"name":user["screen_name"], "group":depth + 1})

            links.append({"source":nodes.index({"name":name, "group":depth}),
                          "target":nodes.index({"name":user["screen_name"], "group":depth + 1})})

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

            data = {"nodes":nodes, "links":links}

            with open('twitter.json', 'w') as outfile:

                json.dump(data, outfile)

            break;

        else:

            get_followers(task)
            get_following(task)
