# -*- coding: utf-8 -*-

import re
import json
from nltk               import pos_tag
from nltk               import ne_chunk
from nltk.stem.wordnet  import WordNetLemmatizer    as Lemmatizer
from util.mitie         import named_entity_extractor
from util.tokenizer_ark import tokenizeRawTweetText as tokenizer

# extractor for short text, such as twitter and facebook
def extractor(peer_text):
    lemmatizer= Lemmatizer()
    entities  = []

    # redundant entities infusion will implement latter

    # tokenization
    print "tokenizing."
    for item in peer_text:
        content = item['content']

        # tokenization
        tokens  = tokenizer(content)
        # normalization
        for i in range(len(tokens)): tokens[i] = lemmatizer.lemmatize(tokens[i])

        item['tokens'] = tokens

    # pos tagging
    print "pos tagging."
    for item in peer_text:
        tokens  = item['tokens']
        tokens_p= pos_tag(tokens)

        item['pos'] = tokens_p

    # entities recognition
    print "nering 1."
    for item in peer_text:
        tokens_p= item['pos']

        entity  = {}
        ne_mid  = ne_chunk(tokens_p, binary = True)
        ne_tag  = re.findall(r'(NE \S+/\S+)', str(ne_mid))

        for i in range(len(ne_tag)):
            tag_list = re.split(r'\W', ne_tag[i])
            entity[tag_list[1]] = []

        item['entity'] = entity

    print "nering 2."
    ner = named_entity_extractor('util/ner_model.dat')
    for item in peer_text:
        tokens  = item['tokens']

        entity  = {}
        ent_mid = ner.extract_entities(tokens)

        for e in entity:
            entity_text = " ".join(tokens[i] for i in e[0])
            entity[entity_text] = []

        item['entity1'] = entity

    for t in peer_text:
        print '-'*50
        print t['entity']
        print t['entity1']

if __name__ == "__main__":

    with file('tweets.json', 'r') as f:
        tweets = json.load(f)
    with file('status.json', 'r') as f:
        status = json.load(f)

    for peer in status:
        name     = peer.keys()[0] 
        print name, '-'*50
        entities = extractor(peer[name])
