# -*- coding: utf-8 -*-

import re
from pymongo     import MongoClient

def convert_pos(pos):

    adv_set = ['RB', 'RBR', 'RBS', 'WRB']               # for adverb
    adj_set = ['JJ', 'JJR', 'JJS']                      # for adjective
    det_set = ['',   'DT', 'PDT', 'WDT']                # for determiner
    prp_set = ['PR', 'PRP', 'PRP$','WP',  'WP$']        # for pronoun
    veb_set = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'] # for verb
    nou_set = ['NN', 'NNS', 'NNP', 'NNPS']              # for noun
    jun_set = ['',   'TO',  'CC',  'CD',  'UH',  'RP', 
               'IN', 'MD',  'LS',  'EX',  'POS']        # for junk

    if   pos in adv_set: return adv_set[0]
    elif pos in adj_set: return adj_set[0]
    elif pos in det_set: return det_set[0]
    elif pos in prp_set: return prp_set[0]
    elif pos in veb_set: return veb_set[0]
    elif pos in nou_set: return nou_set[0]
    elif pos in jun_set: return jun_set[0]
    else : return pos

def pos_sentence_collection(coll):

    pass

if __name__ == "__main__":

    client = MongoClient('mongodb://localhost:27017/')
    twcoll = client.msif.twitter_tweets

    peers  = twcoll.find()
    peer   = peers[5]
    texts  = peer['texts']

    result = []

    for peer in peers[5:101]:
        texts = peer['texts']

        for text in texts:
            pos    = text['pos']
            for item in pos: item[1] = convert_pos(item[1])

            entity_types = text['entity_types']
            if len(entity_types) == 0 : continue

            pos_str= " ".join([token[1] for token in pos 
                               if not token[1]=='-NONE-' and not token[1]==''])
            pos_lst= re.split(r'[.|,|:|\'|`]', pos_str)

            for item in pos_lst:
                if len(item) > 0 and item[0] == ' ': item = item[1:]
                if len(item) > 0 and item[-1]== ' ': item = item[:len(item)-1]
                if len(item) ==0: continue
                if item not in result: 
                    result.append(item)

    #for item in result:
    #    print "#"*80
    #    print item
    print len(result)
    result.sort()
    with file('types.txt', 'w') as f:
        for t in result:
            f.write(str(t))
            f.write('\n')
