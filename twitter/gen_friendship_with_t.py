import tweepy

consumer_key = "6s35FXsv4jD2ar0ZlDYjnt7jZ"
consumer_secret = "oFAlNZr6JGHwCdYGrYNfS3plUSdxg8UlEP2RtiKg59uSYahWRk"
access_token = "1112070588-5bNvcWYSIowvzRbRnSp4jetaCbpLk0xNVFg8egv"
access_token_secret = "rVX3YRtx2Qa5rO9PPqtWP1Fu3HHTK70EuSmBtJXmW7KjE"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()

for tweet in public_tweets:
    print tweet.text