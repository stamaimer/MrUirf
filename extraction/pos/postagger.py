# -*- coding: utf-8 -*-

from nltk import pos_tag
from nltk.tag.stanford import POSTagger, NERTagger
from nltk.tokenize import word_tokenize


if __name__ == "__main__":

    sample = [
        'these women taught English, they are now lying here!'
    ]

    tokens = word_tokenize(sample[0])
    print pos_tag(tokens)
    stagger= POSTagger('english-bidirectional-distsim.tagger',
                       'stanford-postagger.jar')
    print stagger.tag(tokens)
    snerer = NERTagger('english.all.3class.distsim.crf.ser.gz',
                       'stanford-ner.jar')
    print snerer.tag(sample[0])
