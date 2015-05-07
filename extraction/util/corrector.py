import re
from pymongo  import MongoClient
from datetime import datetime, date

def twitter_time_corrector():

    client = MongoClient('mongodb://localhost:27017/')
    tweets = client.mruirf.twitter_tweets
    peers  = tweets.find()

    for peer in peers:
        peer_time = peer['time']
        p_time_lst= peer_time.split('-')
        year = int(p_time_lst[0])
        month= int(p_time_lst[1])
        day  = int(p_time_lst[2])
        peer_time = date(year, month, day)

        texts  = peer['texts']
        for text in texts[::-1]:
            text_time = text['time']
            if re.match(r'\d+s', text_time): text_time = str(peer_time)
            if re.match(r'now',  text_time): text_time = str(peer_time)
            t_time_lst= text_time.split('-')
            year = int(t_time_lst[0])
            month= int(t_time_lst[1])
            day  = int(t_time_lst[2])
            text_time = date(year, month, day)

            if text_time > peer_time:
                text_time = date(year-1, month, day)
            text['time'] = str(text_time)

        tweets.update({'username':peer['username']}, {'$set':{'texts':texts}})

def twitter_entity_corrector():

    client = MongoClient('mongodb://localhost:27017/')
    tweets = client.msif.twitter_tweets
    peers  = tweets.find({'time':'2015-04-23'})

    for peer in peers:
        username = peer['username']
        texts    = peer['texts']
        for text in texts:
            entities = text['entity']
            for entity in entities:
                entity['relevance'] = {}
            text['entity'] = entities
        tweets.update({'username':username}, {'$set':{'texts':texts}})


def twitter_flag_corrector():

    client = MongoClient('mongodb://localhost:27017/')
    tweets = client.mruirf.twitter_tweets
    peers  = tweets.find()

    for peer in peers:
        username = peer['username']
        texts    = peer['texts']
        for text in texts:
            flag = text['flag']
            if len(flag) == 4:
                flag += '0'
                text['flag'] = flag
        tweets.update({'username':username}, {'$set':{'texts':texts}})

def pattern_relevance_index_corrector():

    client = MongoClient('mongodb://localhost:27017/')
    twsent = client.msif.twitter_sentences
    sents  =twsent.find({'pattern':'RB VB NN NN NN NN NN NN NN'})

    for sent in sents:
        pattern = sent['pattern']
        sets    = sent['set']
        for set in sets:
            relevance_indice = [int(r) for r in set['relevance_index'] if not r
                                == u'']
            set['relevance_index'] = relevance_indice
        twsent.update({'pattern':pattern}, {'$set':{'set':sets}})

if __name__ == "__main__":

    twitter_time_corrector()
    pass
