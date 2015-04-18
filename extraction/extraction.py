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

# extractor for short text, such as twitter and facebook
def extractor(client, peer):
    peer_text = peer['tweets']
    lemmatizer= Lemmatizer()
    entities  = []

    # tokenization
    # --------------------------------------------------
    print "tokenizing."
    for item in peer_text:
        content = item['content']

        # tokenization
        tokens  = tokenizer(content)

        # normalization
        for i in range(len(tokens)): 
            tokens[i] = lemmatizer.lemmatize(tokens[i])

        # lower
        lowers = []
        for i in range(len(tokens)):
            lowers.append(tokens[i].lower())

        item['tokens']      = tokens
        item['token_lower'] = lowers

    # pos tagging
    # --------------------------------------------------
    print "pos tagging."
    for item in peer_text:
        tokens  = item['tokens']
        tokens_p= pos_tag(tokens)

        item['pos'] = tokens_p

    # entities recognition
    # --------------------------------------------------

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



if __name__ == "__main__":

    client = MongoClient('mongodb://localhost:27017/')
    tweets = client.msif.twitter_tweets
    peers  = tweets.find().limit(2)

    with file('status.json', 'r') as f:
        status = json.load(f)

    with file('tweet.json', 'w') as f:
        peer = {}
        peer['name'] = peers[0]['name']
        peer['username'] = peers[0]['username']
        peer['tweets'] = peers[0]['tweets']
        peer['time'] = peers[0]['time']
        peer['link'] = peers[0]['link']
        json.dump(peer, f)

    for peer in peers:
        name     = peer["name"]
        print name, '-'*50
        entities = extractor(client, peer)

