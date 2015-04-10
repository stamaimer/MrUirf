# -*- coding: utf-8 -*-

from nltk.tokenize      import word_tokenize
from nltk               import pos_tag
from nltk.tag.stanford  import NERTagger

s = 'my name is wisky!'
token = word_tokenize(s)
pos_t = pos_tag(token)
print pos_t
snerer = NERTagger('english.all.3class.distsim.crf.ser.gz',
                   'stanford-ner.jar')
print snerer.tag([pos_t])

