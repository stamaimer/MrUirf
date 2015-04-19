# -*- coding: utf-8 -*-

import os
import gc
import sys
import json
import session
import argparse
import itertools
import multiprocessing

from lxml import html

import cProfile

nodes = multiprocessing.Manager().list()
links = multiprocessing.Queue()
tasks = multiprocessing.Queue()

lock = multiprocessing.Lock()

percent = 0.0

group1 = 0
group2 = 0

AMOUNT_OF_PROCESS = multiprocessing.cpu_count() * 4

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

                # print '.'

                return response

            else:

                print "request : %s %d" % (response.url, response.status_code)

                if 404 == response.status_code:#anything else?

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

        return [None]

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
@profile
def worker(login, depth, requester):

    while 1:

        try:

            node = tasks.get_nowait()

        except:

            print "%s terminate..." % multiprocessing.current_process().name

            return

        name = node["name"]

        group = node["group"]

        if group > depth:

            print "%s terminate..." % multiprocessing.current_process().name

            return

        else:

            lock.acquire()

            global percent, group1, group2

            if 1 == group:

                if not group1:

                    group1 = sum(( 1 for ele in nodes if ele["group"] == 1 ))

                    print "amounts of group1 : %d" % group1

                percent = nodes.index(node) / float(group1)

            elif 2 == group:

                if not group2:

                    group2 = sum(( 1 for ele in nodes if ele["group"] == 2 ))

                    print "amounts of group2 : %d" % group2

                percent = (nodes.index(node) - group1) / float(group2)

            print "%s is serving %s,\t\t group : %d,\t\t percent : %f" % (multiprocessing.current_process().name, name, group, percent)

            lock.release()

            if is_valid(name, requester):

                following = extract_info(FOLLOWING_URL % name, requester)
                followers = extract_info(FOLLOWERS_URL % name, requester)

                intersection = set(following).intersection(followers)

                #gc.disable()

                for user in intersection:

                    for i in xrange(group + 1):

                        tmpu = {"name":user, "group":i}

                        if tmpu in nodes:

                            links.put({"source":nodes.index(node), "target":nodes.index(tmpu)})

                            break

                        # try:

                        #     indices = nodes.index(tmpu)

                        #     links.put({"source":nodes.index(node), "target":nodes.index(tmpu)})

                        #     break

                        # except ValueError:

                        #     continue

                    else:

                        tmpu = {"name":user, "group":group + 1}

                        nodes.append(tmpu)

                        tasks.put(tmpu)

                        links.put({"source":nodes.index(node), "target":nodes.index(tmpu)})

                #gc.enable()

            else:

                print "%s is invalid" % name

def profiler(login, depth, requester):

    cProfile.runctx("worker(login, depth, requester)", globals(), locals(), "prof_%s.prof" % multiprocessing.current_process().name)

def start(login, depth):

    node = {"name":login, "group":0}

    nodes.append(node)

    requester = session.get_session()

    if is_valid(login, requester):

        following = extract_info(FOLLOWING_URL % login, requester)
        followers = extract_info(FOLLOWERS_URL % login, requester)

        intersection = set(following).intersection(followers)

        for user in intersection:

            tmpu = {"name":user, "group":1}

            nodes.append(tmpu)

            tasks.put(tmpu)

            links.put({"source":nodes.index(node), "target":nodes.index(tmpu)})

    else:

        print "%s is invalid" % login

        sys.exit(0)

    requests = [ session.get_session() for i in xrange(AMOUNT_OF_PROCESS) ]

    process = [ None for i in xrange(AMOUNT_OF_PROCESS) ]

    for i in xrange(AMOUNT_OF_PROCESS):

        process[i] = multiprocessing.Process(target=worker, args=(login, depth, requests[i]))

        process[i].start()

    for i in xrange(AMOUNT_OF_PROCESS):

        process[i].join()

    # worker(login, depth, requester)

    print "generate graph ..."

    data = {"nodes":[node for node in nodes], "links":[link for link in links]}

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
