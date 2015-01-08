# -*- coding: utf-8 -*-

import re
import requests
import argparse
from lxml import html

cookie = '''_pk_ref.100001.8cb4=;
_pk_id.100001.8cb4=899247f323ff97d4.1420638380.5.1420718455.1420706391.; bid="l1CF4cZ3HkY"; ll="118254"; __utma=30149280.1512881098.1420638383.1420706367.1420718413.5; __utmc=30149280; __utmz=30149280.1420638383.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); as="http://www.douban.com/people/yimei/"; ps=y; push_noty_num=0; push_doumail_num=0; __utmv=30149280.6698; ct=y; _pk_ses.100001.8cb4=*; __utmb=30149280.26.10.1420718413; __utmt=1; dbcl2="66986303:Y+CneOSsKTo"; ck="2CpG"'''

def crawl_people(user_id):

    response = requests.get('http://www.douban.com/people/%s' % user_id)

    if 200 == response.status_code:

        tree = html.fromstring(response.text)

        following = tree.xpath("//div[@id='friend']/h2/span/a/text()")

        print following[0].encode('utf-8')

        SEARCH_PAT = re.compile(r'(?<=成员)\d+')

        matches = SEARCH_PAT.search(following[0].encode('utf-8'))

        if matches != None:

            print matches.group(0)

        following_count = int(matches.group(0))

        follower = tree.xpath("//p[@class='rev-link']/a/text()")

        print follower[0].encode('utf-8')

        SEARCH_PAT = re.compile(r'\d+(?=人关注)')

        matches = SEARCH_PAT.search(follower[0].encode('utf-8'))

        if matches != None:

            print matches.group(0)

        follower_count = int(matches.group(0))

    else:

        print response.status_code

    headers = {'cookie' : cookie,
               'referer' : 'http:/www.douban.com/people/%s/' % user_id,
               'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:34.0) Gecko/20100101 Firefox/34.0'}

    response = requests.get('http://www.douban.com/people/%s/contacts' % user_id, headers=headers)

    if 200 == response.status_code:

        print response.text.encode('utf-8')

        tree = html.fromstring(response.text)

        for i in range(following_count):

            xpath = '/html/body/div[3]/div[1]/div/div[1]/dl[%d]/dd/a/text()' % (i + 1)

            print xpath

            following = tree.xpath(xpath)

            print following

            print following[0].encode('utf-8')

    else:

        print response.status_code

#    response = requests.get('http://www.douban.com/people/%s/rev_contacts' % user_id)

if __name__ == '__main__':

    args_parser = argparse.ArgumentParser()

    args_parser.add_argument('user_id')

    args = args_parser.parse_args()

    user_id = args.user_id

    crawl_people(user_id)
