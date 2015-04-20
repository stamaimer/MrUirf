# -*- coding: utf-8 -*-

from pymongo    import MongoClient

def relevance_chi_square(coll, tweet):

    tweets = coll.find()


if __name__ == '__main__':

    client = MongoClient('mongodb://localhost:27017/')

    tweets = client.msif.twitter_tweets

    #sample = tweets.find({})

    all = tweets.find()

    sample = all[50]

    name = sample['username']
    texts = sample['texts']

    print name
    print len(texts)
