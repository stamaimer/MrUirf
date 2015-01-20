# -*- coding: utf-8 -*-

import requests

from oauth import get_bearer_token

CONSUMER_KEY    = "VvbZ6Ur2r00Zyzk22FVDltRhT"
CONSUMER_SECRET = "v0FPEoY3QD2PQO8KLDNthxBsrB3PpkxNXZOFwnEJBnagMCF52L"
BEARER_TOKEN    = "null_initial_value"

host		= "https://api.twitter.com"
api_url		={'profile'	: '/1.1/users/show.json',
		  'tweets' 	: '/1.1/statuses/user_timeline.json',
		  'friends'	: '/1.1/friends/ids.json',
		  'followers'	: '/1.1/followers/ids.json',}

def set_bearer_token():

    global BEARER_TOKEN

    BEARER_TOKEN = get_bearer_token(CONSUMER_KEY, CONSUMER_SECRET)

def get_headers(oauth_type):

    if "application_only" == oauth_type:

        return {'Authorization' : "Bearer %s" % BEARER_TOKEN}

    else : return None  # prepared for signed_oauth

def gain_data(http_method, api_name, params, oauth_type, message_body=None):

    url = host + api_url[api_name] + params

    headers = get_headers(oauth_type)

    if "get" == http_method:

        response = requests.get(url, headers=headers)

    elif "post" == http_method:

        response = requests.post(url, data=message_body, headers=headers)

    else : response = None # prepared for other http methods

    if 200 == response.status_code:

        return response.json()

    else:

	#此处错误处理未完善
	#整个推特数据采集模块中错误在此集中处理

        print response.status_code

        return None

def gain_profile(screen_name="", user_id=""):

    if   "" != screen_name : params = "?screen_name=%s" % screen_name

    elif "" != user_id	   : params = "?user_id=%s"	% user_id

    else : params = None

    return gain_data("get", "profile", 	params, "application_only")

def gain_tweets(screen_name, count="200"):

    params = "?screen_name=%s&count=%s" % (screen_name, count)

    return gain_data("get", "tweets", 	params, "application_only")

def gain_friends(screen_name):

    params = "?screen_name=%s" % screen_name

    return gain_data("get", "friends",	params, "application_only")

def gain_followers(screen_name):

    params = "?screen_name=%s" % screen_name

    return gain_data("get", "followers",params, "application_only")

if '__main__' == __name__ :

    set_bearer_token()

    profile 	= gain_profile(user_id = "2820122167")

    tweets 	= gain_tweets('curmium')

    friends 	= gain_friends('curmium')

    followers 	= gain_followers('curmium')

    print profile

    print tweets

    print friends

    print followers

    for item in profile.keys():

	print item
