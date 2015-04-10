# -*- coding: utf-8 -*-

from nltk.tokenize      import word_tokenize
from nltk               import pos_tag
from nltk.tag.stanford  import NERTagger
from nltk               import ne_chunk

sample = [
        u'Blog entry: summary of Weiwei Wang’s new PRL on magnon driven domain wall motion with DMI',
        u'@IanBDunne Our kids are still excited about Barbie being pushed of the Van-der-Graaf generator from the pressure wave. Good job!',
        u'#piday2015 works best in American date notation. Still nice, though.',
        u'these women taught English, they are now lying here!'
    ]

for text in sample:
    tokens = word_tokenize(text)
    pos_tg = pos_tag(tokens)
    ne     = ne_chunk(pos_tg, binary = True)
    print ne

# snerer = NERTagger('english.all.3class.distsim.crf.ser.gz',
#                    'stanford-ner.jar')
# print snerer.tag([pos_t])

