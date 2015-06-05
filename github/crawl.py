# -*- coding: utf-8 -*-

import requests
import argparse
import pymongo
import json
import time



client_id = ''

client_secret = ''

root_endpoint = 'https://api.github.com'

headers = {'Accept' : 'application/vnd.github.v3+json', 'User-Agent' : ''}



mongo_client = pymongo.MongoClient('mongodb://username:pwd@127.0.0.1:27017/msif')

msif = mongo_client.msif

github_users = msif.github_users



endpoint = root_endpoint + '/users?since=%d'



ratelimit_remaining = '5000'

ratelimit_reset = time.time()



def set_ratelimit_info(headers):

    global ratelimit_remaining

    ratelimit_remaining = headers['X-RateLimit-Remaining']

    global ratelimit_reset

    ratelimit_reset = int(headers['X-RateLimit-Reset'])



def retrieve(url):

    while 1:

        try:

            print 'ratelimit_remaining : %s' % ratelimit_remaining

            if '0' == ratelimit_remaining:

                print 'sleeping %f seconds...' % (ratelimit_reset - time.time())

                time.sleep(ratelimit_reset - time.time())

            print 'request : %s' % url

            response = requests.get(url, params = {'client_id' : client_id, 'client_secret' : client_secret}, headers = headers)

            if 200 == response.status_code:

                print 'request : %s success' % url

                return response

            else:

                set_ratelimit_info(response.headers)

                print 'request : %s %d' % (url, response.status_code)

                print json.dumps(response.json(), indent = 4)

                if 404 == response.status_code:

                    return None

        except requests.exceptions.ConnectionError:

            print 'requests.exceptions.ConnectionError'

            last_insert_id = github_users.find().limit(1).sort([('$natural', -1)])[0]['id']

            url = endpoint + '?since=%d' % last_insert_id

            get_all_users(url)



def get_single_user(url):

    response = retrieve(url)

    if response:

        set_ratelimit_info(response.headers)

        user = response.json()

        github_users.insert(user)

        print user['login']



def stuff(response):

    next_url = response.links['next']['url']

    set_ratelimit_info(response.headers)

    users = response.json()

    for user in users:

        get_single_user(user['url'])

    return next_url



def get_all_users(url):

    response = retrieve(url)

    if response:

        next_url = stuff(response)

    while next_url:

        response = retrieve(next_url)

        if response:

            next_url = stuff(response)



if __name__ == '__main__':

    argument_parser = argparse.ArgumentParser(description='')

    argument_parser.add_argument('-s', '--since', help='', type=int)

    args = argument_parser.parse_args()

    if args.since:

        get_all_users(endpoint % args.since)

    else:

        get_all_users(endpoint % 0)
