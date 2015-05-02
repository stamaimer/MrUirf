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
42 texts per 3 hours, as for total corpus or peer, the speed is 12 texts / hour.
However, these are 7 texts do not have entity, needing no relevance extraction,
so as for each text, the speed is around one text per 6 minutes.
'''

import threading
from pymongo     import MongoClient
from stopwords   import stopwords_mysql, stopwords_nltk, punctuation

def peer_relevance_chi_square(coll, peer_username, file):

    pass

def text_relevance_chi_square(coll, text, file):

    flag     = text['flag']
    tokens   = text['tokens']
    content  = text['content']
    entities = text['entity']

    print "STAT: %s" % ('-'*60)
    file.write("STAT: %s" % ('-'*60))
    file.write('\n')

    print "STAT: Tweet: %s" % " ".join(content.encode('utf8').split('\n'))
    file.write("STAT: Tweet: %s" % " ".join(content.encode('utf8').split('\n')))
    file.write('\n')

    for entity in entities:

        print "STAT: Entity: %s" % str(entity)
        file.write("STAT: Entity: %s" % str(entity))
        file.write('\n')

        entity_word = entity['word']
        entity_type = entity['type']

        # exile_words = stopwords_nltk()
        exile_words = stopwords_mysql()

        # entity itself need not execute relevance
        entity_word_list = entity_word.lower().split()
        for word in entity_word_list: exile_words.append(word)
        exile_puncs = punctuation()
        exile_words = exile_words + exile_puncs

        # calculate the relevance scores of every word and the entity
        for token in [t for t in tokens if t.lower() not in exile_words]:
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
                file.write("STAT: Relevance: %s, \tX2: %s" \
                           % (token.encode('utf8'), X2))
                file.write('\n')

    print 
    file.write('\n')

    return

if __name__ == '__main__':

    client = MongoClient('mongodb://localhost:27017/')

    twcoll = client.msif.twitter_tweets

    sample = twcoll.find_one({'username':'@CFinchMOISD'})

    tweets = sample['texts']

    logfile= file('log.txt', 'w+r')

    for tweet in tweets:

        text_relevance_chi_square(twcoll, tweet, logfile)

    logfile.close()
