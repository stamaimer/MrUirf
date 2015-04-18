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
def extractor(coll, peer_id):

    peer      = coll.find_one({'_id': peer_id})
    peer_text = peer['texts']
    peer_id   = peer['_id']
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
    tokenizer_bat(coll, peer_id)

    # pos tagging
    # --------------------------------------------------
    print "STAT: Start pos tagging."

    # 'pos_bat' function is a func to execute a set of tokens
    # in this process, the func does:
    #   1. pos tagging.
    #   2. update pos tokens in mongodb.
    #   3. update pos tagging flag bit.
    pos_bat(coll, peer_id)

    # entities recognition
    # --------------------------------------------------
    print "STAT: Start entities recognition."

    # 'ner_bat' function is a func to execute a set of texts
    # in this process, the func does:
    #   1. entities recognition.
    #   2. update entities in mongodb.
    #   3. update ner flag bit
    ner_bat(coll, peer_id)

    s = '''
    print "nering 1."
    # load ner classifier
    ner = named_entity_extractor('util/ner_model.dat')

    for item in peer_text:
        tokens  = item['tokens']
        for i in range(len(tokens)):
            tokens[i] = tokens[i].encode('utf8')

        entity  = {}
        ent_mid = ner.extract_entities(tokens)

        for e in ent_mid:
            entity_text = " ".join(tokens[i] for i in e[0])
            entity[entity_text] = []

        item['entity'] = entity

    # delete ner classifier
    del ner

    print "nering 2."
    for item in peer_text:
        tokens_p= item['pos']

        entity  = {}

        # extractor raw entity
        ne_mid  = ne_chunk(tokens_p, binary = True)

        # filter entity
        ne_tag  = re.findall(r'(NE \S+/\S+)', str(ne_mid))

        for i in range(len(ne_tag)):
            tag_list = re.split(r'\W', ne_tag[i])
            entity[tag_list[1]] = []

        # remove redundant
        ent_low = [e.lower() for e in item['entity']]
        for i in [i for i in entity if i.lower() not in ent_low]:
            item['entity'][i] = []

    for item in peer_text:
        print item['content'].encode('utf8')
        print item['entity']

    # relation words extractor
    # --------------------------------------------------
    print "relation words extracting."
    for item in peer_text:
        entity  = item['entity']
    '''


if __name__ == "__main__":

    client = MongoClient('mongodb://localhost:27017/')
    tweets = client.msif.twitter_tweets
    peers  = tweets.find().limit(2)

    with file('status.json', 'r') as f:
        status = json.load(f)

    #tweets.update_one({'_id': peers[0]['_id']}, {'$set': {'time':'2014-7-10' }})

    for peer in peers:
        name     = peer["name"]
        peer_id  = peer["_id"]
        print name, '-'*50
        entities = extractor(tweets, peer_id)

