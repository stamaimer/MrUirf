# -*- coding: utf-8 -*-

from pymongo     import MongoClient




if __name__ == "__main__":

    client = MongoClient('mongodb://localhost:27017/')

    twcoll = client.msif.twitter_tweets

    peers  = twcoll.find()

    peer   = peers[5]

    texts  = peer['texts']

    for text in texts:

        print '#'*80

        pos    = text['pos']

        for pos_token in pos:

            print pos_token[1], 

            if pos_token[1] == '.':

                print
                print '-'*80

        print
