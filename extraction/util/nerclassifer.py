# -*- coding: utf-8 -*-

import re
from nltk.tokenize      import word_tokenize
from nltk               import pos_tag
from nltk.tag.stanford  import NERTagger
from nltk               import ne_chunk
from mitie              import *

def ner_mit(texts):
    entities = []

    ner = named_entity_extractor('ner_model.dat')
    for text in texts:
        tokens = tokenize(text.encode('utf8'))
        entity = ner.extract_entities(tokens)

        print tokens

        for e in entity:
            range = e[0]
            tag   = e[1]
            score = e[2]
            score_text = "{:0.3f}".format(score)
            entity_text = " ".join(tokens[i] for i in range)
            # print "   Score: " + score_text + ": " + tag + ": " + entity_text

            entities.append(entity_text)

    del ner
    return entities

def ner_nltk(texts):
    entities   = []

    for text in texts:
        tokens = word_tokenize(text)
        pos_tg = pos_tag(tokens)
        ne     = ne_chunk(pos_tg, binary = True)
        ne_tag = re.findall(r'(NE \S+/\S+)', str(ne))

        for i in range(len(ne_tag)):
            tag_list = re.split(r'\W', ne_tag[i])
            entities.append(tag_list[1])

    return entities

if __name__ == '__main__':

    sample = [
        u'Blog entry: summary of Weiwei Wang’s new PRL on magnon driven domain wall motion with DMI',
        u'@IanBDunne Our kids are still excited about Barbie being pushed of the Van-der-Graaf generator from the pressure wave. Good job!',
        u'#piday2015 works best in American date notation. Still nice, though.',
        u'these women taught English, they are now lying here!',
        u'', u' '
    ]

print ner_mit(sample)
print ner_nltk(sample)

# snerer = NERTagger('english.all.3class.distsim.crf.ser.gz',
#                    'stanford-ner.jar')
# print snerer.tag([pos_t])

