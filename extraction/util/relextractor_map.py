# -*- coding: utf-8 -*-

from pymongo     import MongoClient




if __name__ == "__main__":

    client = MongoClient('mongodb://localhost:27017/')

    twcoll = client.msif.twitter_tweets

    peers  = twcoll.find()

    peer   = peers[5]

    texts  = peer['texts']

    text   = texts[0]

    pos    = text['pos']

    print pos
