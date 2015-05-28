# -*- coding: utf-8 -*-

'''
    MEMO
    1. lowering all tokens will downsize the output of entity extractor
'''

import re
import json
from pymongo            import MongoClient
from nltk               import pos_tag
from nltk               import ne_chunk
from nltk.stem.wordnet  import WordNetLemmatizer    as Lemmatizer
from util.mitie         import named_entity_extractor
from util.tokenizer_ark import tokenizeRawTweetText as tokenizer
from util.tokenizer     import tokenizer_bat
from util.postagger     import pos_bat
from util.nerclassifier import ner_bat

# extractor for short text, such as twitter and facebook
def preprocess(coll, username):

    peer      = coll.find_one({'username': username})
    peer_text = peer['texts']
    username  = peer['username']
    entities  = []

    # tokenization
    # --------------------------------------------------
    print "STAT: Start tokenizing."

    # 'tokenzier_bat' function is a func to execute a set of text
    # in this process, the func does:
    #   1. tokenization.
    #   2. normalization.
    #   3. lowering.
    #   4. update tokens, tokens_lower in mongodb
    #   5. update tokenization flag bit. 
    #       if flag is '1', then skip the tokenization.
    #       if flag is '0', then set the flag to '1' after processing.
    tokenizer_bat(coll, username)
    print "STAT: ---------------------------------------"

    # pos tagging
    # --------------------------------------------------
    print "STAT: Start pos tagging."

    # 'pos_bat' function is a func to execute a set of tokens
    # in this process, the func does:
    #   1. pos tagging.
    #   2. update pos tokens in mongodb.
    #   3. update pos tagging flag bit.
    #       if tokenization flag is '1' and pos flag is '0', then pos tagging.
    #       if tokenization flag is '0', then stop executing.
    #       if pos flag is '1', then skip the pos tagging.
    pos_bat(coll, username)
    print "STAT: ---------------------------------------"

    # entities recognition
    # --------------------------------------------------
    print "STAT: Start entities recognition."

    # 'ner_bat' function is a func to execute a set of texts
    # in this process, the func does:
    #   1. entities recognition.
    #   2. update entities in mongodb.
    #   3. update ner flag bit
    #       if pos flag is '1' and ner flag is '0', then nering.
    #       if pos flag is '0', then stop executing.
    #       if ner flag is '1', then skip the nering.
    ner_bat(coll, username)
    print "STAT: ---------------------------------------"

if __name__ == "__main__":

    client = MongoClient('mongodb://localhost:27017/')
    tweets = client.msif.twitter_tweets
    status = client.msif.facebook_status

    # set no time out
    # in python 1.x you could set "find(timeout=False)"
    # however, in python 2.x, subprocess.call does not have a timeout argument
    # you could not do like so
    peers  = status.find({'time':'2015-05-22'})

    #tweets.update_one({'_id': peers[0]['_id']}, {'$set': {'time':'2014-7-10' }})

    for i, peer in enumerate(peers[:2]):

        print "STAT: %s peer under executing." % str(i+1)
        name     = peer["name"].encode('utf8')
        username = peer["username"]
        print name, '-'*50

        try:
            entities = preprocess(status, username)
        except:
            pass

    # because in former line, we set cursor no time out
    # now we should make sure the cursor closed
    # that means all of the data exhausted
    peers.close()
