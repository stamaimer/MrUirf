# -*- coding: utf-8 -*-

import requests

from oauth import get_bearer_token

CONSUMER_KEY    = "VvbZ6Ur2r00Zyzk22FVDltRhT"
CONSUMER_SECRET = "v0FPEoY3QD2PQO8KLDNthxBsrB3PpkxNXZOFwnEJBnagMCF52L"
BEARER_TOKEN    = "null_initial_value"

host		= "https://api.twitter.com"
api_url		={'profile'		: '/1.1/users/show.json',		# gain user profile
		  'tweets' 		: '/1.1/statuses/user_timeline.json',	# gain user recent tweets
		  'retweeters_id'	: '/1.1/statuses/retweeters/ids.json',	# gain retweeters ids
		  'retweets'		: '/1.1/statuses/retweets',		# gain the info of retweet
		  'friends_id'		: '/1.1/friends/ids.json',		# gain followings ids
		  'friends_list'	: '/1.1/friends/list.json',		# gain followings list(profile)
		  'followers_id'	: '/1.1/followers/ids.json',		# gain followers ids
		  'followers_list'	: '/1.1/followers/list.json',		# gain followers list(profile)
		 }

def set_bearer_token():

    global BEARER_TOKEN

    BEARER_TOKEN = get_bearer_token(CONSUMER_KEY, CONSUMER_SECRET)

def get_headers(oauth_type):

    if "application_only" == oauth_type:

        return {'Authorization' : "Bearer %s" % BEARER_TOKEN}

    else : return None  # prepared for signed_oauth

def gain_data(http_method, api_name, rest_url, oauth_type, message_body=None):

    url = host + api_url[api_name] + rest_url

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

def gain_friends_id(screen_name):

    params = "?screen_name=%s" % screen_name

    return gain_data("get", "friends_id",	params, "application_only")["ids"]

def gain_friends_list(screen_name):

    params = "?screen_name=%s" % screen_name

    return gain_data("get", "friends_list",	params, "application_only")["users"]

def gain_followers_id(screen_name):

    params = "?screen_name=%s" % screen_name

    return gain_data("get", "followers_id",	params, "application_only")["ids"]

def gain_followers_list(screen_name):

    params = "?screen_name=%s" % screen_name

    return gain_data("get", "followers_list",	params, "application_only")["users"]

def gain_retweeters(tweet_id):

    params = "?id=%s" % tweet_id

    return gain_data("get", "retweeters_id",	params,	"application_only")

def gain_retweets(tweet_id):

    rest_url="/%s.json" % tweet_id

    return gain_data("get", "retweets", 	rest_url,"application_only")

def compare_dict(dict_1, dict_2):

    if dict_1.keys() != dict_2.keys() : return None

    for key in dict_1.keys() :

        if dict_1[key] != dict_2[key] :

            print ", ".join((key, str(dict_1[key]), str(dict_2[key])))

def dicts_filter(dicts, list):

    result = []

    for item in dicts :

        tmp = {}

        for key in list : tmp[key] = item[key]

        result.append(tmp)

    return result

def user_parser(screen_name):

    tweets 	= gain_tweets(screen_name)

    followings 	= gain_friends_id(screen_name)

    followers	= gain_followers_id(screen_name)

if '__main__' == __name__ :

    set_bearer_token()

    # example:
    #	screen_name = 'curmium'
    #	user_id = '2820122167'
    #	tweet_id = '557216428772712448'

    user_parser('curmium')

    tweets = gain_tweets('curmium')

    for tweet in tweets:

       print tweet

    compare_dict(tweets[0], tweets[4])

#    keys =  tweets[0].keys()

#    for item in keys:

#	print item
