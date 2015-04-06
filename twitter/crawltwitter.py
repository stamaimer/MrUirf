import sys
import tweepy
import argparse

consumer_key = '6s35FXsv4jD2ar0ZlDYjnt7jZ'
consumer_secret = 'oFAlNZr6JGHwCdYGrYNfS3plUSdxg8UlEP2RtiKg59uSYahWRk'
access_token = '1112070588-5bNvcWYSIowvzRbRnSp4jetaCbpLk0xNVFg8egv'
access_token_secret = 'rVX3YRtx2Qa5rO9PPqtWP1Fu3HHTK70EuSmBtJXmW7KjE'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

if __name__ == '__main__':

    argument_parser = argparse.ArgumentParser(description='')

    argument_parser.add_argument('screen_name', help='The screen name, handle, or alias that this user identifies themselves with.\
                                                      screen_names are unique. Typically a maximum of 15 characters long,\
                                                      but some historical accounts may exist with longer names.')

    argument_parser.add_argument('depth', help='', type=int)

    args = argument_parser.parse_args()

    screen_name = args.screen_name

    depth = args.depth

    if depth < 1 or depth > 3:

        print 'depth value %d is invalid. valid range is 1~3.' % depth

        sys.exit('invalid depth value')

    print screen_name, depth

    matches = api.lookup_users(screen_names=[screen_name])

    print matches
