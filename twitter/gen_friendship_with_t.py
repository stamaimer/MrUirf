import tweepy

consumer_key = "6s35FXsv4jD2ar0ZlDYjnt7jZ"
consumer_secret = "oFAlNZr6JGHwCdYGrYNfS3plUSdxg8UlEP2RtiKg59uSYahWRk"
access_token = "1112070588-5bNvcWYSIowvzRbRnSp4jetaCbpLk0xNVFg8egv"
access_token_secret = "rVX3YRtx2Qa5rO9PPqtWP1Fu3HHTK70EuSmBtJXmW7KjE"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser(description="")

    argument_parser.add_argument("login", help="")

    argument_parser.add_argument("depth", help="", type=int)

    args = argument_parser.parse_args()

    sed_login = args.login

    max_depth = args.depth

    start(sed_login, max_depth)