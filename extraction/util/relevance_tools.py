from pymongo import MongoClient

if __name__ == "__main__":

    client = MongoClient("mongodb://localhost:27017/")

    tweets = client.msif.twitter_tweets

    peer   = tweets.find_one({'username':'@willgoldstone'})

    texts  = peer['texts']

    word   = raw_input()

    for i, text in enumerate(texts):

        tokens = text['tokens']

        token  = tokens[0]

        if word == token: print i

