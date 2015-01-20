import urllib
import base64
import requests

def urlencode(str):

    return urllib.quote(str, '')

def b64encode(str):

    return base64.b64encode(str)

BEARER_TOKEN_URL = "https://api.twitter.com/oauth2/token"

def get_bearer_token(consumer_key, consumer_secret):

    bearer_token_credentials     = ':'.join([urlencode(consumer_key), urlencode(consumer_secret)])

    bearer_token_credentials_b64 = b64encode(bearer_token_credentials)

    headers, payload             = {}, {}

    headers['Authorization']     = ' '.join(['Basic', bearer_token_credentials_b64])

    headers['Content-Type']      = 'application/x-www-form-urlencoded;charset=UTF-8'

    payload['grant_type']        = "client_credentials"

    response = requests.post(BEARER_TOKEN_URL, data=payload, headers=headers)

    print response.request.data

    bearer_token = response.json()['access_token']

    return bearer_token
