import urllib
import base64
import requests

CONSUMER_KEY = "6s35FXsv4jD2ar0ZlDYjnt7jZ"
CONSUMER_SECRET = "oFAlNZr6JGHwCdYGrYNfS3plUSdxg8UlEP2RtiKg59uSYahWRk"

BEARER_TOKEN_ENDPOINT = "https://api.twitter.com/oauth2/token"

def urlencode(str):

    return urllib.quote(str, "")

def b64encode(str):

    return base64.b64encode(str)

def get_bearer_token(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET):

    bearer_token_credentials = ':'.join([urlencode(consumer_key), urlencode(consumer_secret)])

    b64encoded_bearer_token_credentials = b64encode(bearer_token_credentials)

    headers, payload = {}, {}

    headers["Authorization"] = "Basic " + b64encoded_bearer_token_credentials

    headers["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8"

    payload["grant_type"] = "client_credentials"

    response = requests.post(BEARER_TOKEN_ENDPOINT, headers=headers, data=payload)

    if 200 == response.status_code:

        return response.json()["access_token"]

    else:

        print response.status_code, response.json()

        return None

if __name__ == "__main__":

    print get_bearer_token()
