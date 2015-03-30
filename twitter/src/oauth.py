import urllib
import base64
import requests

BEARER_TOKEN_URL = "https://api.twitter.com/oauth2/token"

def urlencode(str):

    return urllib.quote(str, "")

def b64encode(str):

    return base64.b64encode(str)

def get_bearer_token(consumer_key, consumer_secret):

    bearer_token_credentials = ':'.join([urlencode(consumer_key), urlencode(consumer_secret)])

    b64encoded_bearer_token_credentials = b64encode(bearer_token_credentials)

    headers, payload = {}, {}

    headers["Authorization"] = "Basic " + b64encoded_bearer_token_credentials

    headers["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8"

    payload["grant_type"] = "client_credentials"

    response = requests.post(BEARER_TOKEN_URL, headers=headers, data=payload)

    if 200 == response.status_code:

        return response.json()["access_token"]

    else:

        print response.status_code, response.json()

        return None