# -*- coding: utf-8 -*-

import os
import sys
import json
import session
import argparse
import itertools
from lxml import html
from multiprocessing import Process, Lock

nodes = []#
links = []#
tasks = []#

requester = session.get_session()

percent, group1, group2 = 0.0, 0, 0#

lock = Lock()

AMOUNT_OF_PROCESS = 8

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

def extract_info(url):

    response = retrieve(url)

    if response:

        tree = html.fromstring(response.content)

        members = itertools.chain(parse(tree, MXPATH))

        next = parse(tree, NXPATH)[0]

        while next:

            response = retrieve(HOST + next)

            if response:

                tree = html.fromstring(response.content)

                members = itertools.chain(members, parse(tree, MXPATH))

                next = parse(tree, NXPATH)[0]

            else:

                break

        return members

    else:

        return itertools.chain()

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

            if followers_count >= 6000 \
            or following_count >= 6000 \
            or following_count == 2001 \
            or following_count * 10 < followers_count:

                return False

            else:

                return True

    else:

        return False

def worker(login, depth):

    while 1:

        if 1 == AMOUNT_OF_PROCESS:

            print "generate graph ..."

            data = {"nodes":nodes, "links":links}

            with open(login + "_twitter.json", 'w') as outfile:

                json.dump(data, outfile)

            return os.path.abspath( login + "_twitter.json")

        lock.acquire()

        try:

            node = tasks.pop(0)

        except:

            global AMOUNT_OF_PROCESS

            AMOUNT_OF_PROCESS -= 1

            lock.release()

            return

        lock.release()

        name = node["name"]

        group = node["group"]

        if group == -1:

            lock.acquire()

            global AMOUNT_OF_PROCESS

            AMOUNT_OF_PROCESS -= 1

            lock.release()

            return

        if group > depth:

            lock.acquire()

            for i in xrange(AMOUNT_OF_PROCESS - 2):

                tasks.insert(0, {"name":"", "group":-1})

            lock.release()

            return

        else:

            # lock.acquire()

            # global percent, group1, group2

            # if 1 == group:

            #     if not group1:

            #         group1 = sum(( 1 for ele in nodes if ele["group"] == 1 ))

            #         print "amounts of group1 : %d" % group1

            #     percent = nodes.index(node) / float(group1)

            # elif 2 == group:

            #     if not group2:

            #         group2 = sum(( 1 for ele in nodes if ele["group"] == 2 ))

            #         print "amounts of group2 : %d" % group2

            #     percent = (nodes.index(node) - group1) / float(group2)

            # print "%s is serving %s,\t\t group : %d,\t\t percent : %f" % (threading.current_thread().name, name, group, percent)

            # lock.release()

            print "%s is serving %s,\t\t group : %d" % (multiprocessing.current_process().name, name, group)

            if is_valid(name):

                following = extract_info(FOLLOWING_URL % name)
                followers = extract_info(FOLLOWERS_URL % name)

                intersection = set(following).intersection(followers)

                for user in intersection:

                    for i in xrange(group + 1):

                        tmpu = {"name":user, "group":i}

                        lock.acquire()

                        if tmpu in nodes:

                            links.append({"source":nodes.index(node), "target":nodes.index(tmpu)})

                            lock.release()

                            break

                        lock.release()

                    else:

                        tmpu = {"name":user, "group":group + 1}

                        lock.acquire()

                        nodes.append(tmpu)
                        tasks.append(tmpu)

                        links.append({"source":nodes.index(node), "target":nodes.index(tmpu)})

                        lock.release()

            else:

                print "%s is invalid" % name


def start(login, depth):

    node = {"name":login, "group":0}

    nodes.append(node)

    if is_valid(login):

        following = extract_info(FOLLOWING_URL % login)
        followers = extract_info(FOLLOWERS_URL % login)

        intersection = set(following).intersection(followers)

        for user in intersection:

            tmpu = {"name":user, "group":1}

            nodes.append(tmpu)
            tasks.append(tmpu)

            links.append({"source":nodes.index(node), "target":nodes.index(tmpu)})

    else:

        print "%s is invalid" % login

        sys.exit(0)

    process = [ None for i in xrange(AMOUNT_OF_PROCESS) ]

    for i in xrange(AMOUNT_OF_PROCESS):

        process[i] = Process(target=worker, args=(login, depth))

        process[i].start()

if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser(description="")

    argument_parser.add_argument("login", help="")

    argument_parser.add_argument("depth", help="", type=int)

    args = argument_parser.parse_args()

    sed_login = args.login

    max_depth = args.depth

    start(sed_login, max_depth)
