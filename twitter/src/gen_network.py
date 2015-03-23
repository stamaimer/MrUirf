import urllib
import base64
import requests
import networkx
import argparse

CONSUMER_KEY = "6s35FXsv4jD2ar0ZlDYjnt7jZ"
CONSUMER_SECRET = "oFAlNZr6JGHwCdYGrYNfS3plUSdxg8UlEP2RtiKg59uSYahWRk"

ENDPOINT = "https://api.twitter.com/oauth2/token"

def urlencode(str):

    return urllib.quote(str, "")

def b64encode(str):

    return base64.b64encode(str)

def get_bearer_token(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET):

    bearer_token_credentials = ':'.join([urlencode(consumer_key), urlencode(consumer_secret)])

    b64encoded_bearer_token_credentials = b64encode(bearer_token_credentials)

    headers, payload = {}, {}

    headers["Authorization"] = ' '.join(["Basic", b64encoded_bearer_token_credentials])

    headers["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8"

    payload["grant_type"] = "client_credentials"

    response = requests.post(ENDPOINT, headers=headers, data=payload)

    bearer_access_token = response.json()["access_token"]

    return bearer_access_token

if __name__ == "__main__":

    print get_bearer_token()
