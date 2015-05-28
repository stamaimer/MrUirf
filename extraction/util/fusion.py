# -*- coding:utf8 -*

from pymongo import MongoClient

def fusion(user_id, tw_coll, tw_username, fb_coll, fb_username, id_coll):

    tw_peer     = tw_coll.find_one({'username':tw_username})
    fb_peer     = fb_coll.find_one({'username':fb_username})
    tw_texts    = tw_peer['texts']
    fb_texts    = fb_peer['texts']
    individual  = {}
    individual['user_id']     = user_id
    individual['tw_username'] = tw_username
    individual['fb_username'] = fb_username
    individual['entities']    = []

    data = []
    data.append({'source_sns':'twitter', 'texts':tw_texts})
    data.append({'source_sns':'facebook','texts':fb_texts})

    for media in data:
        source_sns = media['source_sns']
        texts      = media['texts']
        for index, text in enumerate(texts):
            source_index= str(index)
            source_time = text['time']
            entities    = text['entity']

            for entity in entities:

                entity_word = entity['word']
                entity_relevance   = []
                for func in entity['relevance']:
                    for relevance_word in entity['relevance'][func]:
                        if relevance_word not in entity_relevance: 
                            entity_relevance.append(relevance_word)
                for i in xrange(len(individual['entities'])):
                    i_entity_word = individual['entities'][i]['word']
                    i_entity_source=individual['entities'][i]['sources']
                    i_entity_rele = individual['entities'][i]['relevance_s']
                    if i_entity_word == entity_word:
                        source_item = {}
                        source_item['sns'] = source_sns
                        source_item['index']=source_index
                        source_item['time'] =source_time
                        i_entity_source.append(source_item)
                        for relevance_word in entity_relevance:
                            for j in xrange(len(i_entity_rele)):
                                i_relevance_word = i_entity_rele[j]['word']
                                i_relevance_source=i_entity_rele[j]['sources']
                                if i_relevance_word == relevance_word:
                                    source_i = {}
                                    source_i['sns'] = source_sns
                                    source_i['index']=source_index
                                    i_entity_rele[j]['sources'].append(source_i)
                                    break
                            else:
                                relevance_item = {}
                                relevance_item['word'] = relevance_word
                                relevance_item['sources'] = []
                                source_item = {}
                                source_item['sns'] = source_sns
                                source_item['index']=source_index
                                relevance_item['sources'].append(source_item)
                                i_entity_rele.append(relevance_item)
                        individual['entities'][i]['sources'] = i_entity_source
                        individual['entities'][i]['relevance_s'] = i_entity_rele
                        break
                else:
                    entity_item = {}
                    entity_item['word'] = entity_word
                    entity_item['sources'] = []
                    entity_item['relevance_s'] = []
                    source_item = {}
                    source_item['sns'] = source_sns
                    source_item['index']=source_index
                    source_item['time']= source_time
                    entity_item['sources'].append(source_item)
                    for relevance_word in entity_relevance:
                        relevance_item = {}
                        relevance_item['word'] = relevance_word
                        relevance_item['sources'] = []
                        source_item = {}
                        source_item['sns'] = source_sns
                        source_item['index']=source_index
                        relevance_item['sources'].append(source_item)
                        entity_item['relevance_s'].append(relevance_item)
                    individual['entities'].append(entity_item)

    id_coll.insert(individual)
    dividi_rele_source_mode(user_id, id_coll)
    divide_entity_source(user_id, id_coll)

def divide_entity_source(user_id, id_coll):

    individual = id_coll.find_one({'user_id':user_id})
    entities   = individual['entities']

    for entity in entities:
        entity_source = []
        for source in entity['sources']:
            if source['sns'] not in entity_source:
                entity_source.append(source['sns'])
        entity['source_count'] = entity_source
        if not len(entity['word'].split()) == 1: entity['source_count']=[]

    result = []
    for entity in entities:
        source_count = entity['source_count']
        if len(source_count) == 2:
            result.append(entity)
    id_coll.update_one({'user_id':user_id}, {'$set':{'match_entities':result}})

    result = []
    for entity in entities:
        source_count = entity['source_count']
        if len(source_count) == 1 and source_count[0] == 'twitter':
            result.append(entity)
    id_coll.update_one({'user_id':user_id},{'$set':{'twitter_entities':result}})

    result = []
    for entity in entities:
        source_count = entity['source_count']
        if len(source_count) == 1 and source_count[0] == 'facebook':
            result.append(entity)
    id_coll.update_one({'user_id':user_id},{'$set':{'facebook_entities':result}})

def dividi_rele_source_mode(user_id, id_coll):

    individual = id_coll.find_one({'user_id':user_id})
    entities = individual['entities']

    for entity in entities:
        relevance_s = entity['relevance_s']
        for index, rele in enumerate(relevance_s):
            relevance_mode = []
            rele_sources = rele['sources']
            for source in rele_sources:
                if source['sns'] not in relevance_mode:
                    relevance_mode.append(source['sns'])
            relevance_s[index]['mode'] = relevance_mode
        entity['relevance_s'] = relevance_s

    id_coll.update_one({'user_id':user_id},{'$set':{'entities':entities}})

def get_entities(user_id, mode, page_no):

    client = MongoClient('mongodb://localhost:27017/')
    id_coll= client.msif.individual

    # param mode is aimed to point out what kind of texts should be fetched.
    # 0 means match entities
    # 1 means entities only in twitter
    # 2 means entities only in facebook
    individual = id_coll.find_one({'user_id':int(user_id)})
    result = []
    if mode == '0': result = individual['match_entities']
    if mode == '1': result = individual['twitter_entities']
    if mode == '2': result = individual['facebook_entities']

    page_no = int(page_no)
    return result[(page_no-1)*5:page_no*5]

if __name__ == "__main__":

    client = MongoClient("mongodb://localhost:27017/")
    tweets = client.msif.twitter_tweets
    status = client.msif.facebook_status
    individual = client.msif.individual

    user_id = 3
    tw_username= "@amyshearn"
    fb_username= "@amy.shearn"

    fusion(user_id, tweets, tw_username, status, fb_username, individual)

    #entities = get_entities(user_id, '0', '1')
    #print entities[0]
    #print len(entities)
