# -*- coding: utf-8 -*-

import os
import json
import time
import argparse
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

nodes = []
links = []

ROOT_ENDPOINT = "https://m.facebook.com"

FRIENDS_XPATH = "//h3[@class='_52jh _5pxc']/a"

percent, group1, group2 = 0.0, 0, 0

def login(email, password):

    broswer = webdriver.Chrome()

    broswer.get(ROOT_ENDPOINT)

    broswer.find_element_by_name("email").send_keys(email)

    broswer.find_element_by_name("pass").send_keys(password + Keys.RETURN)

    print "login sucess..."

    return broswer

def find_by_link(link):

    for node in nodes:

        if node["link"] == link:

            return nodes.index(node)

def get_friends(handle, node):

    name = node["name"]

    link = node["link"]

    group = node["group"]

    if '?' in link:

        link += "&v=friends"

    else:

        link += "?v=friends"

    handle.get(link) 

    name_list = [ ele.text for ele in handle.find_elements_by_xpath(FRIENDS_XPATH) ]
    link_list = [ ele.get_attribute("href") for ele in handle.find_elements_by_xpath(FRIENDS_XPATH) ]
    
    link += "&startindex=%d"

    i = 1

    while True:

        handle.get(link % (24 * i))
        
        try:
            
            handle.find_element_by_xpath("//*[@id='root']/div/div/div/i")

            break

        except selenium.common.exceptions.NoSuchElementException:

            friends = handle.find_elements_by_xpath(FRIENDS_XPATH)

            name_list.extend( [ ele.text for ele in friends ] )
            link_list.extend( [ ele.get_attribute("href") for ele in friends ] )
            
            i = i + 1

    global percent, group1, group2
        
    if 0 == group:

        percent = 1

    elif 1 == group:

        if not group1:

            group1 = sum([ 1 for ele in nodes if ele["group"] == 1 ])

        percent = nodes.index(node) / float(group1)

    elif 2 == group:

        if not group2:

            group2 = sum([ 1 for ele in nodes if ele["group"] == 2 ])

        percent = (nodes.index(node) - group1) / float(group2)

    print "name : %s, link : %s, group : %d, percent : %f, friends : %d" % (name, link, group, percent, len(link_list))

    for fname, flink in zip(name_list, link_list):

        if flink not in [ele["link"] for ele in nodes]:

            tmpu = {"name":fname, "link":flink, "group":group + 1}

            nodes.append(tmpu)

            links.append({"source":nodes.index(node), "target":nodes.index(tmpu)})

        else:

            links.append({"source":nodes.index(node), "target":find_by_link(flink)})

def start(name, link, depth):

    handle = login("", "")

    nodes.append({"name":name, "link":link, "group":0})

    for node in nodes:

        if node["group"] > depth:

            print "generate graph..."

            data = {"nodes":nodes, "links":links}

            with open("facebook.json", 'w') as outfile:

                json.dump(data, outfile)

            return os.path.abspath("facebook.json")

        else:

            get_friends(handle, node)

if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser(description="")

    argument_parser.add_argument("name", help="")

    argument_parser.add_argument("link", help="")

    argument_parser.add_argument("depth", help="", type=int)

    args = argument_parser.parse_args()

    name = args.name

    link = args.link

    depth = args.depth

    start(name, link, depth)
