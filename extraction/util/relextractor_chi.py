# -*- coding: utf-8 -*-

'''
    MEMO
    2015-5-2
    1. In this file we use chi square to calculate relevance words of entities.
The result of chi square is much better than pos pattern entity-relevance map.
However, one of urgent flaws of chi square is it cost much time to execute one
peer, getting all of relevance of every entity. Finally, we determined to
rewrite function 'relevance_chi_square' to a multi-thread function.
    Before we reconstruct this function, the approximate speed of execution is
42 texts per 3 hours, as for total corpus or peer, the speed is 14 texts / hour.
However, these are 7 texts do not have entity, needing no relevance extraction,
so as for each text, the speed is around one text per 6 minutes.
    2. After rewriting the function to multi-threading, we find the executions
lows down to 9 texts per hour. So we determined to improve our VPS to double
cores.
    3. After imporved my VPS CPU to double cores, the execution just speed up 
slightly, around 11 texts per hour. Finally we determined to reconstruct the 
function to multi-processing.
    2015-5-3
    1. After reconstructed function to multi-processing, (6 processes and 30
texts a set), the execution speed doubled, to 24 texts per hour. It might
because of the improving of CPU core amount. So we determined improve our cpu
cores to 4 or 8 to speed up.
    2. After improved CPU cores amount to 8, the execution speed up to 64 texts
per hour.
    3. Then we improve average processes of single core from 2 to 4, the speed
go up to 86 texts per hour, and we could estimate that if we increase tasks pool
size from 96 to a higher level, the speed will still increase.

    2015-5-4
    1. @CFinchMOISD(username) chi square relevance extraction has done.
'''

import time
from multiprocessing import Process, Queue, Manager, cpu_count
from pymongo         import MongoClient
from stopwords       import stopwords_mysql, stopwords_nltk, punctuation

def peer_relevance_chi_square(text_coll, peer_username, corpus_coll):

    peer    = text_coll.find_one({'username':peer_username})
    username= peer['username']
    texts   = peer['texts']
    tasks   = []
    buffer  = Queue()
    result  = Manager().list()
    for index, text in enumerate(texts):
        tasks.append({'index':index, 'text':text})

    process_count = cpu_count() * 4
    #process_count = 1

    while True:
        try:    [buffer.put(tasks.pop(0)) for i in xrange(320)]
        except: pass

        processes = [None for i in xrange(process_count)]
        for i in xrange(len(processes)):
            processes[i]=Process(target=text_agent,
                                 args=(corpus_coll, buffer, result))
            processes[i].start()
        for i in xrange(len(processes)):
            processes[i].join()

        for item in result: texts[item['index']] = item['text']
        text_coll.update({'username':username}, {'$set':{'texts':texts}})

        if len(tasks) == 0: break

def text_agent(corpus_coll, buffer, result):

    while True:
        try:    task = buffer.get_nowait()
        except: break
        task_index = task['index']
        task_text  = task['text']
        text_done  = text_relevance_chi_square(corpus_coll, task_text)
        task['text']=text_done
        result.append(task)

def text_relevance_chi_square(corpus_coll, text):

    # check flag: flag[3] means relevance flag for chi square
    flag     = text['flag']
    if flag[2] == '0': return text # need ner done before
    if flag[3] == '1': return text # have already done

    tokens   = text['tokens']
    content  = text['content']
    entities = text['entity']

    print "STAT: %s" % ('-'*60)
    print "STAT: Text: %s" % " ".join(content.encode('utf8').split('\n'))

    for entity in entities:

        print "STAT: Entity: %s" % str(entity)

        entity_word = entity['word']
        entity_type = entity['type']
        entity_rele = entity['relevance']
        entity_rele['chi_square'] = []

        # exile_words = stopwords_nltk()
        exile_words = stopwords_mysql()

        # entity itself need not execute relevance
        entity_word_list = entity_word.lower().split()
        for word in entity_word_list: exile_words.append(word.encode('utf8'))
        exile_puncs = punctuation()
        exile_words = exile_words + exile_puncs

        # calculate the relevance scores of every word and the entity
        for token in [t for t in tokens if t.lower().encode('utf8') not in exile_words]:    
            n11 = 0.0   # token hit     |   type hit
            n10 = 0.0   # token hit     |   type not hit
            n01 = 0.0   # token not hit |   type hit
            n00 = 0.0   # token not hit |   type not hit

            corpus      = corpus_coll.find({'time':'2015-04-23'})
            for corpus_peer in corpus:
                corpus_texts = corpus_peer['texts']

                for corpus_text in corpus_texts:
                    ct_entity_types = corpus_text['entity_types']
                    ct_tokens       = corpus_text['token_lower']

                    if token.lower() in ct_tokens:
                        if entity_type in ct_entity_types:  n11 += 1
                        else :                              n10 += 1
                    else:
                        if entity_type in ct_entity_types:  n01 += 1
                        else :                              n00 += 1

            n   = n11 + n10 + n01 + n00
            e11 = n * ((n11+n10)/n) * ((n11+n01)/n)
            e10 = n * ((n10+n11)/n) * ((n10+n00)/n)
            e01 = n * ((n01+n11)/n) * ((n01+n00)/n)
            e00 = n * ((n00+n10)/n) * ((n00+n01)/n)
            X2  = 0

            pairs = [{'n':n11, 'e':e11}, {'n':n10, 'e':e10},
                     {'n':n01, 'e':e01}, {'n':n00, 'e':e00}] 
            for pair in[pair for pair in pairs if not pair['e'] == 0]:
                X2 += ((pair['n'] - pair['e']) ** 2) / pair['e']

            # if X2 value greater than or equal to 10.83
            # means the relevance rate of entity and token is greater than 0.999
            if X2 >= 10.83: 
                print "STAT: Relevance: %s, \tX2: %s" % (token.encode('utf8'),X2)
                entity_rele['chi_square'].append(token)

        # this entity relevance words extraction done.
        entity['relevance'] = entity_rele

    # all entities relevance words extraction done.
    text['entity'] = entities
    text['flag']   = flag[0:3] + '1' + flag[4:]
    print

    return text

if __name__ == '__main__':

    client = MongoClient('mongodb://localhost:27017/')
    text_coll  = client.msif.twitter_tweets
    corpus_coll= client.msif.twitter_tweets
    # peer_relevance_chi_square(twcoll, '@CFinchMOISD')
    peer_relevance_chi_square(text_coll, '@amyshearn', corpus_coll)
    
