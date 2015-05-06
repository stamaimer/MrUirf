# -*- coding: utf-8 -*-

'''
    MEMO
    2015-4-30
    1. In the first test, we choose the peers crawled in 2015-04-23, totally 100
peers, as corpus. In this corpus, we induce more than 300,000 tweets and more
than 60,000 patterns. So we want to filter out a set of patterns, which peers
using most and the size of the set will not be too big. After evaluation, we
found that those patterns talked by more than 40 peers are frequently used, and
the tweets in these patterns make up nearly 60 percent. Finally we determined to
use this set.
    2. Then we find that the patterns used by more than 40 people are always
short ones, which do not contain any infomation. So we need filter pattern
length also. In the evaluate we find the patterns whose length greater than or
equal to 8 make up nearly 80 percent. Finally we determined to filter out those
patterns longer than or equal to 8. However, the rule together with the rule
above: used by more than 40 people, the result only make up 5 percent in all
tweets. To make the test set larger, we modify the rules: 1. the pattern longer
than or equal to 7, which make up 90 percent patterns; 2. the pattern used by
more than 10 peers, which means used by more than 10 percent peers in corpus, as
if in a larger corpus like real twitter, it is still a huge and convinced test
set. Filtering under these two rule, we filter out 10 percent tweets.
    2015-5-1
    1. To determine how many texts should be marked for one pattern, in our test
corpus there are nearly 600 patterns and 30,000 texts, 50 texts for 1 pattern on
average. We determined to mark 20 percent of them, so finally we filter 10 texts
from each pattern to mark.
'''

import re
from pymongo     import MongoClient

def get_green_str(word):
    return "\x1b[32m%s\x1b[0m" % word

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
                    data['flag']    = '0'   # if in this pattern more than 5 sets
                                            # are flaged, then set flag to 1
                    set_first       = {'username':username, 'index':text_index, 
                                       'entity':[], 'relevance_index':[],
                                       'flag':'0'}
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
                                   'entity':[], 'relevance_index':[], 'flag':'0'}
                        sets.append(set_new)
                        sents.update({'pattern':item}, {'$set':{'set':sets}})

        print "SUCC: Scan done."
        print
        print

def filter_pattern(db, peers_limit, pattern_len = 0):

    twsent  = db.twitter_sentences
    sents   = twsent.find()

    result  = []
    for sent in sents:
        item = {}
        item['pattern'] = sent['pattern']
        item['peers'] = []
        item['sentences'] = len(sent['set'])
        for set in sent['set']:
            if set['username'] not in item['peers']:
                item['peers'].append(set['username'])
        item['peers'] = len(item['peers'])
        result.append(item)

    filter = []
    for item in result:
        if item['peers'] >= peers_limit:
            if len(item['pattern'].split()) >= pattern_len:
                filter.append(item)

    return filter

def evaluate_peers_limit(db, peers_limit, pattern_len = 0):

    twsent  = db.twitter_sentences
    sents   = twsent.find()
    all     = sum([len(sent['set']) for sent in sents])
    filter  = filter_pattern(db, peers_limit, pattern_len)
    fter    = sum([item['sentences'] for item in filter])

    print "fter in all: %s %%" % str(100 * float(fter) / all)
    print "patterns: %d" % len(filter)

    with file('frequent_patterns.txt', 'w') as f:
        for item in filter:
            f.write('%s\t%s\t%s\n' % (item['pattern'], item['peers'], \
                    item['sentences']))

def evaluate_pattern_len(db, pattern_len):

    twsent  = db.twitter_sentences
    sents   = twsent.find()
    all     = sents.count()
    result  = []

    for sent in sents:
        if len(sent['pattern'].split()) >= pattern_len:
            result.append(sent)
    result = len(result)

    print "result in all: %s %%" % str(100 * float(result) / all)

def manual_mark(db, pattern_set):

    twsent  = db.twitter_sentences
    tweets  = db.twitter_tweets

    for pattern in pattern_set:
        pattern = pattern['pattern']
        pattern_l=pattern.split()
        sent = twsent.find_one({'pattern':pattern})
        if not sent == None:
            sent_flag = sent['flag']
            # check if marked
            if sent_flag == '1' : continue
            print "STAT: Start marking %d pattern." \
                  % (twsent.find({'flag':'1'}).count()+1)
            print "STAT: Pattern: %s." % pattern

            sets = sent['set']
            for set_index, set in enumerate(sets[::-1][:10]):
                set_flag = set['flag']
                # check if marked
                if set_flag == '1' : continue
                print "STAT: Mark %d text of the pattern." % (set_index+1)

                set_entity=set['entity']
                set_rele = set['relevance_index']
                username = set['username']
                text_index=set['index']
                peer = tweets.find_one({'username':username})
                texts= peer['texts']
                text = texts[text_index]
                pos  = [(pos[0], convert_pos(pos[1])) for pos in text['pos']]
                entities=[entity['word'] for entity in text['entity']]

                # segment pos list by '.' and ','
                pos_l, tmp  = [], []
                for p in pos: 
                    if p[1] == '.' or p[1] == ',': 
                        pos_l.append(tmp)
                        tmp = []
                    else: tmp.append(p)
                pos_l.append(tmp)

                # filter pos segment
                for pos_seg in pos_l:
                    pos_seg_c = [pos[1] for pos in pos_seg if not pos[1] == '']
                    if pos_seg_c == pattern_l:
                        pos = pos_seg
                        break

                # print
                index_str, pos_str, text_str = "", "", ""
                pos_index_filter = 0
                for pos_index, item in enumerate(pos):

                    if ( pos_index + 1 ) % 8 == 0:
                        print index_str.encode('utf8')
                        print pos_str.encode('utf8')
                        print text_str.encode('utf8')
                        index_str, pos_str, text_str = "", "", ""

                    word = item[0]
                    tag  = item[1]
                    word_len = len(word)
                    tab_num  = word_len / 8 + 1

                    # get real index (for those tag in (NN, PR, VB, JJ, RB))
                    if tag == '' : real_index = ''
                    else:
                        real_index = pos_index_filter
                        pos_index_filter += 1

                    # filter entity word, and make it green
                    if word in entities:
                        if real_index not in set_entity:
                            set_entity.append(real_index)
                        real_index= get_green_str(real_index)
                        word      = get_green_str(word)
                        tag       = get_green_str(tag)

                    # add str
                    index_str += str(real_index)+ '\t'*tab_num
                    pos_str   += tag            + '\t'*tab_num
                    text_str  += word           + '\t'

                print index_str.encode('utf8')
                print pos_str.encode('utf8')
                print text_str.encode('utf8')

                # marking ---------------------------------------------------
                while True:
                    set_rele = raw_input('The indice of relevance: ').split()
                    set_rele = [int(r) for r in set_rele if not r == '']
                    ensure   = raw_input('Finish this text?(y/n): ')
                    set_flag = '1'
                    if ensure == 'y':
                        set['entity'] = set_entity
                        set['relevance_index'] = set_rele
                        set['flag'] = set_flag
                        twsent.update({'pattern':pattern}, {'$set':{'set':sets}})
                        print "SUCC: Text done."
                        break
                # marking ---------------------------------------------------
                print "STAT: %s" % ('-'*60)

            twsent.update({'pattern':pattern}, {'$set':{'flag':'1'}})
            print "SUCC: Pattern done."

def text_relevance_pos_pattern(coll, text):

    # check flag
    flag = text['flag']
    if flag[2] == '0': return text # need ner done before
    if flag[4] == '1': return text # have already done

    # convert text to segment
    pos = [(p[0], convert_pos(p[1])) for p in text['pos']]
    pattern_list = []
    pattern      = {'pos':[]}
    for p in pos:
        if p[1] == '': continue
        if p[1] == '.' or p[1] == ',':
            pattern['words'] = [i[0] for i in pattern['pos']]
            pattern['tags']  = [i[1] for i in pattern['pos']]
            pattern['pattern']=" ".join(pattern['tags'])
            del pattern['pos']
            del pattern['tags']
            pattern_list.append(pattern)
            pattern = {'pos':[]}
        pattern['pos'].append(p)

    # pos pattern relevance extraction
    entities = text['entity']
    for entity in entities:
        entity_word = entity['word']
        entity_rele = entity['relevance']
        entity_rele['pos_pattern'] = []

        for pattern in pattern_list:
            words = pattern['words']

            if entity_word in words:
                entity_index = words.index(entity_word)
                sentence     = coll.find_one({'pattern':pattern['pattern']})
                if sentence == None or sentence['flag'] == '0': continue
                set_f=[s for s in sentence['set'] if entity_index in s['entity']]
                rele_indice  = [s['relevance_index'] for s in set_f]
                all_rele_count=sum([len(item) for item in rele_indice])
                average_words= int(round(float(all_rele_count)/len(rele_indice)))

                rele_frequ = {}
                for set in rele_indice:
                    for index in set:
                        if index not in rele_frequ: rele_frequ[index] = 1
                        else: rele_frequ[index]+=1

                frequent_sort= rele_frequ.values()
                frequent_sort.sort()
                frequent     =frequent_sort[average_words-1]

                for i in rele_frequ:
                    if rele_frequ[i] >= frequent:
                        entity_rele['pos_pattern'].append(words[i])
        entity['relevance'] = entity_rele

    text['entity'] = entities

    #######################################################################
    # ATTENTION:
    # because pos pattern relevance rxtractor train set is not marked done,
    # we could not set flag for pos pattern from 0 to 1
    # text['flag'] = text['flag'][0:4] + '1' + text['flag'][5:]
    #######################################################################

    return text

if __name__ == "__main__":

    client = MongoClient('mongodb://localhost:27017/')
    twdb   = client.msif

    input = raw_input("What mode?(mark/extr): ")
    # pos_sentence_collection(twdb, {'time':'2015-04-23'})
    # evaluate_pattern_len(twdb, 7)
    # evaluate_peers_limit(twdb, 10, 7)

    if input == "mark":
        # marker
        patterns = filter_pattern(twdb, 10, 7)
        manual_mark(twdb, patterns)

    elif input == "extr":
        # relevance word extraction
        peer = twdb.twitter_tweets.find_one({'username':'@CFinchMOISD'})
        texts= peer['texts']
        indice=[1113, 1280, 1356]
        texts= [text for i, text in enumerate(texts) if i in indice]
        for text in texts:
            text_done = text_relevance_pos_pattern(twdb.twitter_sentences, text)
            entities = text_done['entity']
            for entity in entities:
                print entity

    ''' to fix cursor timeout
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
    '''

