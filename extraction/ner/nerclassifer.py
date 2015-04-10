# -*- coding: utf-8 -*-

from nltk.tokenize      import word_tokenize
from nltk               import pos_tag
from nltk.tag.stanford  import NERTagger
from nltk               import ne_chunk

s = 'my name is wisky!'
tokens = word_tokenize(s)
pos_tg = pos_tag(tokens)
ne     = ne_chunk(pos_tg, binary = True)
print ne
# snerer = NERTagger('english.all.3class.distsim.crf.ser.gz',
#                    'stanford-ner.jar')
# print snerer.tag([pos_t])

