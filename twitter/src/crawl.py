import requests

from oauth import get_bearer_token

CONSUMER_KEY    = "VvbZ6Ur2r00Zyzk22FVDltRhT"
CONSUMER_SECRET = "v0FPEoY3QD2PQO8KLDNthxBsrB3PpkxNXZOFwnEJBnagMCF52L"
BEARER_TOKEN    = "null_initial_value"

def set_bearer_token():

    global BEARER_TOKEN

    BEARER_TOKEN = get_bearer_token(CONSUMER_KEY, CONSUMER_SECRET)

def get_profile(screen_name):

    url = "https://api.twitter.com/1.1/users/show.json?screen_name=%s" % screen_name

    headers = {'Authorization' : "Bearer %s" % BEARER_TOKEN}

    return requests.get(url, headers=headers).json()

def get_tweets(screen_name):

    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=%s&count=200" % screen_name

    headers = {'Authorization' : "Bearer %s" % BEARER_TOKEN}

    return requests.get(url, headers=headers).json()

if '__main__' == __name__ :

    set_bearer_token()

    profile = get_profile('curmium'),

    tweets = get_tweets('curmium')

    print profile

    print tweets
