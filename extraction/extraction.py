# -*- coding: utf-8 -*-

import json
from nltk               import pos_tag
from nltk               import ne_chunk
from nltk.stem.wordnet  import WordNetLemmatizer
from util.tokenizer_ark import tokenizeRawTweetText
from util.mitie         import named_entity_extractor

if __name__ == "__main__":

    with file('tweets.json', 'r') as f:
        tweets = json.load(f)
    with file('status.json', 'r') as f:
        status = json.load(f)

    print status

