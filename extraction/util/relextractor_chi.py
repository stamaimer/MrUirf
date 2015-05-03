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
'''

import time
from multiprocessing import Process, Queue, Manager, cpu_count
from pymongo         import MongoClient
from stopwords       import stopwords_mysql, stopwords_nltk, punctuation


def peer_relevance_chi_square(coll, peer_username, file):

    peer    = coll.find_one({'username':peer_username})
    texts   = peer['texts']
    tasks   = []
    buffer  = Queue()
    result  = Manager().list()
    for index, text in enumerate(texts):
        tasks.append({'index':index, 'text':text})

    process_count = cpu_count() * 3

    while True:
        try:    [buffer.put(tasks.pop(0)) for i in xrange(30)]
        except: pass

        processes = [None for i in xrange(process_count)]
        for i in xrange(len(processes)):
            processes[i] = Process(target = text_agent, args=(coll,buffer,file))
            processes[i].start()
        for i in xrange(len(processes)):
            processes[i].join()

        if len(tasks) == 0: break

def text_agent(coll, buffer, file):

    while True:
        try:    task = buffer.get_nowait()
        except: break
        task_index = task['index']
        task_text  = task['text']
        text_relevance_chi_square(coll, task_text, file)

def text_relevance_chi_square(coll, text, file):

    flag     = text['flag']
    tokens   = text['tokens']
    content  = text['content']
    entities = text['entity']
    log_str  = ""

    print "STAT: %s" % ('-'*60)
    log_str += "STAT: %s" % ('-'*60)
    log_str += '\n'

    print "STAT: Tweet: %s" % " ".join(content.encode('utf8').split('\n'))
    log_str += "STAT: Tweet: %s" % " ".join(content.encode('utf8').split('\n'))
    log_str += '\n'

    for entity in entities:

        print "STAT: Entity: %s" % str(entity)
        log_str += "STAT: Entity: %s" % str(entity)
        log_str += '\n'

        entity_word = entity['word']
        entity_type = entity['type']

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

            corpus      = coll.find({'time':'2015-04-23'})
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
                print "STAT: Relevance: %s, \tX2: %s" % (token.encode('utf8'), X2)
                log_str += "STAT: Relevance: %s, \tX2: %s" \
                           % (token.encode('utf8'), X2)
                log_str += '\n'

    print 
    log_str += '\n'
    file.write(log_str)

    return

if __name__ == '__main__':

    client = MongoClient('mongodb://localhost:27017/')

    twcoll = client.msif.twitter_tweets

    logfile= file('log.txt', 'w+r')

    peer_relevance_chi_square(twcoll, '@CFinchMOISD', logfile)

    ''' code before multi-threading

    sample = twcoll.find_one({'username':'@CFinchMOISD'})

    tweets = sample['texts']

    for tweet in tweets:

        text_relevance_chi_square(twcoll, tweet, logfile)

    '''
