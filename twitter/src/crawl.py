import requests

from oauth import get_bearer_token

CONSUMER_KEY    = "VvbZ6Ur2r00Zyzk22FVDltRhT"
CONSUMER_SECRET = "v0FPEoY3QD2PQO8KLDNthxBsrB3PpkxNXZOFwnEJBnagMCF52L"
BEARER_TOKEN    = "null_initial_value"

def set_bearer_token():

    global BEARER_TOKEN

    BEARER_TOKEN = get_bearer_token(CONSUMER_KEY, CONSUMER_SECRET)

set_bearer_token()

url = "https://api.twitter.com/1.1/statuses/user_timeline.json\
           ?user_id=Limkokwing_MY"

headers = {'Authorization' : "Bearer %s" % BEARER_TOKEN}

response = requests.get(url, headers=headers)

print response.status_code
