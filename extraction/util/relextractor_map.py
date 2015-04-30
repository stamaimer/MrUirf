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
    jun_set = ['',   'TO',  'CC',  'CD',  'UH',  'RP',  # for junk
               'IN', 'MD',  'LS',  'EX',  'POS', '-LRB-', 
               '-NONE-',    '$',   '#',   '\'',  ':', '`']

    if   pos in adv_set: return adv_set[0]
    elif pos in adj_set: return adj_set[0]
    elif pos in det_set: return det_set[0]
    elif pos in prp_set: return prp_set[0]
    elif pos in veb_set: return veb_set[0]
    elif pos in nou_set: return nou_set[0]
    elif pos in jun_set: return jun_set[0]
    else : return pos

def pos_sentence_collection(db, filter):

    sents  = db.twitter_sentences
    peers  = db.twitter_tweets.find(filter)

    for peer_index, peer in enumerate(peers):

        texts    = peer['texts']
        texts_len= len(texts)
        username = peer['username']
        print "STAT: %s %s" % ( username, '-'*50 )
        print "STAT: This is the %s peer." % str(peer_index + 1)
        print "STAT: Start sentences pattern scanning."

        for text_index, text in enumerate(texts):

            if text_index % 300 == 0 :
                print "STAT: %s %% scanned."   \
                % str( 100 * float(text_index) / texts_len )[:5]

            if len(text['entity_types']) == 0 : continue

            pos     = [convert_pos(item[1]) for item in text['pos']]
            pos     = [item for item in pos if not item == '']
            pos_str = " ".join( pos )
            pos_lst = re.split(r'[.|,]', pos_str)

            for item in pos_lst:
                if len(item) > 0 and item[0] == ' ': item = item[1:]
                if len(item) > 0 and item[-1]== ' ': item = item[:len(item)-1]
                if len(item) ==0: continue

                pattern = sents.find_one({'pattern':item})
                if pattern == None:
                    data = {}
                    data['pattern'] = item
                    set_first       = {'username':username, 'index':text_index, 
                                       'entity':[], 'relevance_index':[]}
                    data['set']     = [set_first]
                    sents.insert(data)
                else:
                    sets = pattern['set']
                    for set in sets:
                        if text_index == set['index'] and \
                           username   == set['username']:
                            break
                    else:
                        set_new = {'username':username, 'index':text_index,
                                   'entity':[], 'relevance_index':[]}
                        sets.append(set_new)
                        sents.update({'pattern':item}, {'$set':{'set':sets}})

        print "SUCC: Scan done."
        print
        print

def evaluate(db):

    sents   = db.twitter_sentences
    patterns= sents.find()
    result  = []

    for pattern in patterns:

        item = {}
        item['pattern'] = pattern['pattern']
        item['people'] = []
        item['sentences'] = len(pattern['set'])

        for set in pattern['set']:

            if set['username'] not in item['people']:

                item['people'].append(set['username'])

        item['people'] = len(item['people'])
        result.append(item)

    with file('output.txt', 'w') as f:

        for item in result:

            if item['people'] >= 5:

                f.write('%s\t%s\t%s\n' % (item['pattern'], item['people'], \
                                      item['sentences']))


if __name__ == "__main__":

    client = MongoClient('mongodb://localhost:27017/')
    twdb   = client.msif

    twsents= twdb.twitter_sentences
    tweets = twdb.twitter_tweets
    people = []
    peers = tweets.find({'time':'2015-04-23'})
    for peer in peers:
        people.append(peer['username'])

    people_have = []
    sents = twsents.find()
    for sent in sents:
        sets = sent['set']
        for set in sets:
            peer = set['username']
            if peer not in people_have:
                people_have.append(peer)

    people_not = [peer for peer in people if peer not in people_have]

    for peer in people_not:
        pos_sentence_collection(twdb, {'username':peer})

    #pos_sentence_collection(twdb, {'time':'2015-04-23'})
    #evaluate(twdb)
