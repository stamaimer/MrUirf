import base64
import requests

BEARER_TOKEN_URL        = "https://api.twitter.com/oauth2/token"

def get_bearer_token(consumer_key, consumer_secret):

    bearer_token_credentials    = consumer_key + ":" +consumer_secret

    bearer_token_credentials_b64= base64.b64encode(bearer_token_credentials)

    headers, payload            = {}, {}

    headers['Authorization']    = "Basic " + bearer_token_credentials_b64

    headers['Content-Type']     = "application/x-www-form-urlencoded;\
                                   charset=UTF-8"
    payload['grant_type']       = "client_credentials"

    response = requests.post(BEARER_TOKEN_URL, data=payload, headers=headers)

    bearer_token = response.json()['access_token']

    return bearer_token
