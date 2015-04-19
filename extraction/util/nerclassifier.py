# -*- coding: utf-8 -*-

'''
    In this file, we introduce two types of ner tools, mitie and nltk.ne_chunk.
    In short, in mitie's readme file, we can learn the entities recognition from
mitie have four types: 
    1. PERSON, for people
    2. LOCATION, for geo location
    3. ORGANIZATION, for org
    4. MSIC, for other types of entities
    In terms of nltk, there are 9 types of entities recorded in docs, PERCENT,
FACILITY, ORGANIZATION, PERSON, LOCATION, DATE, TIME, MONEY, and GPE. However,
actually there are only 3 types:
    1. PERSON, for people
    2. ORGANIZATION, for org
    3. GPE, for geo-political entity, the same as LOCATION
    Finally, to detect full set of entities, we determine to combine these two
ner tools. And inducing 4 types of entities, PERSON, LOCATION, ORGANIZATION and
MSIC.
'''

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
            print "   Score: " + score_text + ": " + tag + ": " + entity_text

            entities.append(entity_text)

    del ner
    return entities

def ner_nltk(texts):
    entities   = []

    for text in texts:
        tokens = word_tokenize(text)
        pos_tg = pos_tag(tokens)
        ne     = ne_chunk(pos_tg)

        #print ne
        ne_tag = re.findall(r'((GPE|PERSON|ORGANIZATION) \S+/\S+)', str(ne))
        print ne_tag

        for i in range(len(ne_tag)):
            tag_list = re.split(r'\W', ne_tag[i][0])
            print ' '*10,tag_list
            entities.append(tag_list[1])

    return entities

# [ner_bat]
# @input: peer_id
# @brief: ner all texts of a peer
#         1. store in mongodb directly
#         2. modify ner flag bit
def ner_bat(coll, peer_id):

    peer    = coll.find_one({'_id': peer_id})
    texts   = peer['texts']
    count_s = 0     # count for success
    count_w = 0     # count for done before
    count_e = 0     # count for error

    print "STAT: Nering 1."
    ner = named_entity_extractor('util/ner_model.dat')

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
    for text in texts:
        flag    = text['flag']

        if flag[1:2] == '1' and flag[2:3] == '1':

            tokens_p = text['pos']

            entity   = {}

            # extractor raw entity
            ne_mid = ne_chunk(tokens_p, binary = True)

            # filter entity
            ne_tag = re.findall(r'(NE \S+/\S+)', str(ne_mid))

            for i in range(len(ne_tag)):
                tag_list = re.split(r'\W', ne_tag[i])
                entity[tag_list[1]] = []

            # remove redundant
            ent_low = [e.lower() for e in text['entity']]
            for i in [i for i in entity if i.lower() not in ent_low]:
                text['entity'][i] = []

    coll.update_one({'_id':peer_id}, {'$set': {'texts':texts}})
    print "SUCC: Nering done."
    print "STAT: %s texts executed, %s have done before and %s errors." \
            % (count_s, count_w, count_e)

if __name__ == '__main__':

    sample = [
        u'Blog entry: summary of Weiwei Wang’s new PRL on magnon driven domain wall motion with DMI',
        u'@IanBDunne Our kids are still excited about Barbie being pushed of the Van-der-Graaf generator from the pressure wave. Good job!',
        u'#piday2015 works best in American date notation. Still nice, though.',
        u'these women taught English, they are now lying here!',
        u'today is 6th June, a great festival',
        u'this t-shirt cost me 10 dollar.',
        u'two fifty a m, 1:30 p.m.',
        u'175 million Canadian Dollars, GBP 10.40',
        u'Murray River, Mount Everest',
        u'twenty pct, 18.75 %',
    ]

    # print ner_mit(sample)
    print ner_nltk(sample)

    # snerer = NERTagger('english.all.3class.distsim.crf.ser.gz',
    #                    'stanford-ner.jar')
    # print snerer.tag([pos_t])

