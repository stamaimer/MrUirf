# -*- coding: utf-8 -*-

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
    for item in peer_text:
        content = item['content']

        # tokenization
        tokens  = tokenizer(content)
        # normalization
        for i in range(len(tokens)): tokens[i] = lemmatizer.lemmatize(tokens[i])

        item['tokens'] = tokens

    # pos tagging
    for item in peer_text:
        tokens  = item['tokens']
        tokens_p= pos_tag(tokens)

        item['pos'] = tokens_p

    print peer_text

if __name__ == "__main__":

    with file('tweets.json', 'r') as f:
        tweets = json.load(f)
    with file('status.json', 'r') as f:
        status = json.load(f)

    for peer in status:
        name     = peer.keys()[0] 
        print name, '-'*50
        entities = extractor(peer[name])
