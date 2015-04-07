# -*- coding: utf-8 -*-

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

            name_list.extend( [ ele.text for ele in handle.find_elements_by_xpath(FRIENDS_XPATH) ] )
            link_list.extend( [ ele.get_attribute("href") for ele in handle.find_elements_by_xpath(FRIENDS_XPATH) ] )
            
            i = i + 1
        
    count = lambda : sum([1 for node in nodes if node["group"] == group])

    get_friends.count = count()

    print "name : %s, link : %s, group : %d, percent : %f" % (name, link, group, nodes.index(node) / get_friends.count)

    for fname, flink in zip(name_list, link_list):

        if flink not in [ele["link"] for ele in nodes]:

            tmpu = {"name":fname, "link":flink, "group":group + 1}

            nodes.append(tmpu)

            links.append({"source":nodes.index(node), "target":nodes.index(tmpu)})

        else:

            links.append({"source":nodes.index(node), "target":find_by_link(flink)})

def start(name, link, depth):

    handle = login("stamaimer@gmail.com", "bl4u-awsf")

    nodes.append({"name":name, "link":link, "group":0})

    for node in nodes:

        if node["group"] > depth:

            print "generate graph..."

            data = {"nodes":nodes, "links":links}

            with open("facebook.json", 'w') as outfile:

                json.dump(data, outfile)

            break

        else:

            get_friends(handle, node)

if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser(description="")

    argument_parser.add_argument("name", help="")

    argument_parser.add_argument("link", help="")

    argument_parser.add_argument("depth", help="")

    args = argument_parser.parse_args()

    name = args.name

    link = args.link

    depth = args.depth

    start(name, link, depth)
