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

def pos_bat(coll, peer_id):

    peer    = coll.find_one({'_id': peer_id})
    texts   = peer['texts']
    count_s = 0     # count for success
    count_w = 0     # count for done before
    count_e = 0     # count for error

    print "STAT: Nering 1."
    ner = named_entity_extractor('./ner_model.dat')

    for text in texts:

        flag   = text['flag']
        content= text['content']

        # memo:
        # the first flag bit refer to tokenization flag bit.
        # the second flag bit refer to pos tagging flag bit.
        # the third flag bit refer to ner flag bit.
        if flag[1:2] == '1' and flag[2:3] == '0':

            tokens = text['tokens']
            for i in range(len(tokens)):
                tokens[i] = tokens[i].encode('utf8')

            entity  = {}
            ent_mid = ner.extract_entities(tokens)

            for e in ent_mid:
                entity_text = " ".join(tokens[i] for i in e[0])
                entity[entity_text] = []

            text['entity'] = entity
            text['flag'] = flag[0:2] + '1' + flag[3:]
            count_s += 1

        elif flag[1:2] == '0':
            count_e += 1

        elif flag[2:3] == '1':
            count_w += 1

        else:
            count_e += 1

    # delete ner classifier
    del ner

    print "STAT: Nering 2."
    

    coll.update_one({'_id':peer_id}, {'$set': {'texts':texts}})

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

