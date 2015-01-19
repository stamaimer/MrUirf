import urllib
import base64
import requests

CONSUMER_KEY = '6s35FXsv4jD2ar0ZlDYjnt7jZ'
CONSUMER_SECRET = 'oFAlNZr6JGHwCdYGrYNfS3plUSdxg8UlEP2RtiKg59uSYahWRk'

def urlencode(str):

    return urllib.quote(str, '')

def b64encode(str):

    return base64.b64encode(str)

if __name__ == '__main__':

    bearer_token_credentials = b64encode(':'.join([urlencode(CONSUMER_KEY), urlencode(CONSUMER_SECRET)]))

    headers = {'Authorization' : 'Basic %s' % bearer_token_credentials,
               'Content-Type'  : 'application/x-www-form-urlencoded;charset=UTF-8'}

    payload = 'grant_type=client_credentials'

    response = requests.post('https://api.twitter.com/oauth2/token',
                             data=payload,
                             headers=headers)

    print response.json()
