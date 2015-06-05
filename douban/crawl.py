# -*- coding: utf-8 -*-

import re
import json
import requests
import argparse
from lxml import html



login_url = 'https://www.douban.com/accounts/login'

homepage_url = 'http://www.douban.com/people/%s/'

follower_url = homepage_url + 'rev_contacts'

following_url = homepage_url + 'contacts'



session = requests.Session()



form_email = ''

form_password = ''



def login():

    payload = {'login' : '登录',
               'source' : 'None',
               'form_email' : form_email, 
               'form_password' : form_password,
               }

    response = session.post(login_url, data = payload)

    print response.status_code

    print response.text.encode('utf-8')


def retrieve(url):

    while 1:

        #检查是否已经超过请求次数限制，做出相应措施

        print 'request : %s' % url

        response = session.get(url, allow_redirects = False)

        if 200 == response.status_code:

            print 'request : %s success' % url

            return response

        else:

            print 'request : %s %d' % (url, response.status_code)



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



def crawl(user_id):

    response = retrieve(homepage_url % user_id)

    tree = html.fromstring(response.text)

    following_count = parse(tree, "//div[@id='friend']/h2/span/a/text()", r'(?<=成员)\d+')

    follower_count = parse(tree, "//p[@class='rev-link']/a/text()", r'\d+(?=人关注)')

    response = retrieve(following_url % user_id)

    tree = html.fromstring(response.text)

    for i in range(int(following_count)):

        following = parse(tree, "//*[@id='content']/div/div[1]/dl[%d]/dd/a/text()" % (i + 1))

        print following



if __name__ == '__main__':

    args_parser = argparse.ArgumentParser()

    args_parser.add_argument('user_id')

    args = args_parser.parse_args()

    user_id = args.user_id

    login()

    #crawl(user_id)
