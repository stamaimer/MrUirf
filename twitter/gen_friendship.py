# -*- coding: utf-8 -*-

import os
import sys
import json
import session
import argparse
import itertools
import multiprocessing

from lxml import html

HOST = "https://mobile.twitter.com"

HOMEPAGES_URL = HOST + "/%s"
FOLLOWING_URL = HOST + "/%s/following"
FOLLOWERS_URL = HOST + "/%s/followers"

VXPATH = "//a[@class='badge']/img"
CXPATH = "//div[@class='statnum']/text()"
MXPATH = "//span[@class='username']/text()"
NXPATH = "//*[@id='main_content']/div/div[2]/div/a/@href"

def retrieve(url, requester):

    while 1:

        try:

            response = requester.get(url)

            if 200 == response.status_code:

                return response

            else:

                print "request : %s %d" % (response.url, response.status_code)

                if 404 == response.status_code:

                    return None
                
        except :

            raise

def parse(tree, xpath):

    eles = tree.xpath(xpath, smart_strings=False)

    if 1 == len(eles):

        return eles

    elif len(eles) > 1:

        return eles[1:]

    else:

        return [0]

def extract_info(url, requester):

    response = retrieve(url, requester)

    if response:

        tree = html.fromstring(response.content)

        members = itertools.chain(parse(tree, MXPATH))

        next = parse(tree, NXPATH)[0]

        while next:

            response = retrieve(HOST + next, requester)

            if response:

                tree = html.fromstring(response.content)

                members = itertools.chain(members, parse(tree, MXPATH))

                next = parse(tree, NXPATH)[0]

            else:

                break

        return members

    else:

        return itertools.chain()

def is_valid(name, requester):

    response = retrieve(HOMEPAGES_URL % name, requester)

    if response:

        tree = html.fromstring(response.content)

        verify = parse(tree, VXPATH)[0]

        if verify:

            return False

        else:

            count = parse(tree, CXPATH)

            following_count = int(count[0].replace(',', ''))
            followers_count = int(count[1].replace(',', ''))

            if followers_count >= 6000 \
            or following_count >= 6000 \
            or following_count == 2001 \
            or following_count * 10 < followers_count:

                return False

            else:

                return True

    else:

        return False

def worker(login, depth, requester, nodes, links, tasks, lock, indices):

    while 1:

        try:

            node = tasks.get_nowait()

        except:

            print "%s terminate..." % multiprocessing.current_process().name

            return

        name = node[0]

        group = node[1]

        if group > depth:

            print "%s terminate..." % multiprocessing.current_process().name

            return

        else:

            current_indices = nodes[node]

            print "%s is serving %s,\t\t group : %d,\t\t %d left" % (multiprocessing.current_process().name, name, group, tasks.qsize())

            if is_valid(name, requester):

                following = extract_info(FOLLOWING_URL % name, requester)
                followers = extract_info(FOLLOWERS_URL % name, requester)

                intersection = set(following).intersection(followers)

                for user in intersection:

                    for i in xrange(group + 1):

                        tmpu = (user, i)

                        try:

                            exist = nodes[tmpu]

                            links.append({"source":current_indices, "target":nodes[tmpu]})

                            break

                        except:

                            continue

                    else:

                        if group == 2:

                            continue

                        tmpu = (user, group + 1)

                        lock.acquire()

                        nodes[tmpu] = indices; indices+=1

                        lock.release()

                        tasks.put(tmpu)

                        links.append({"source":current_indices, "target":nodes[tmpu]})

            else:

                print "%s is invalid" % name

def start(login, depth):

    nodes = multiprocessing.Manager().dict()
    tasks = multiprocessing.Queue()
    links = multiprocessing.Manager().list()

    lock = multiprocessing.Lock()

    indices = 0

    AMOUNT_OF_PROCESS = multiprocessing.cpu_count() * 6

    node = (login, 0)

    nodes[node] = indices; indices+=1

    requester = session.get_session()

    if is_valid(login, requester):

        following = extract_info(FOLLOWING_URL % login, requester)
        followers = extract_info(FOLLOWERS_URL % login, requester)

        intersection = set(following).intersection(followers)

        for user in intersection:

            tmpu = (user, 1)

            nodes[tmpu] = indices; indices+=1

            tasks.put(tmpu)

            links.append({"source":nodes[node], "target":nodes[tmpu]})

    else:

        print "%s is invalid" % login

        sys.exit(0)

    requests = [ session.get_session() for i in xrange(AMOUNT_OF_PROCESS) ]

    process = [ None for i in xrange(AMOUNT_OF_PROCESS) ]

    for i in xrange(AMOUNT_OF_PROCESS):

        process[i] = multiprocessing.Process(target=worker, args=(login, depth, requests[i], nodes, links, tasks, lock, indices))

        process[i].start()

    for i in xrange(AMOUNT_OF_PROCESS):

        process[i].join()

    print "generate graph ..."

    data = {"nodes":[{"name":node[0], "group":node[1]} for node in dict(nodes).iteritems()], "links":[link for link in links]}

    with open(login + "_twitter.json", 'w') as outfile:

        json.dump(data, outfile)

    return os.path.abspath( login + "_twitter.json")

if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser(description="")

    argument_parser.add_argument("login", help="")

    argument_parser.add_argument("depth", help="", type=int)

    args = argument_parser.parse_args()

    sed_login = args.login

    max_depth = args.depth

    start(sed_login, max_depth)
