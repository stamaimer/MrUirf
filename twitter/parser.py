from collector import gain_tweets, gain_followers_id, gain_friends_id

def compare_dict(dict_1, dict_2):

    if dict_1.keys() != dict_2.keys() : return None

    for key in dict_1.keys() :

        if dict_1[key] != dict_2[key] :

            print ", ".join((key, str(dict_1[key]), str(dict_2[key])))

def dicts_filter(dicts, list):

    result = []

    for item in dicts :

        tmp = {}

        for key in list : tmp[key] = item[key]

        result.append(tmp)

    return result

def relation_handler(followings, followers):

    mutual, oneway, strange = [], [], []

    followings.sort(), followers.sort()

    mutual = [u for u in followings if u in followers]

    oneway = [u for u in followings if u not in mutual] + [u for u in followers if u not in mutual]

    return mutual, oneway, strange

def user_parser(screen_name):

    tweets 	= gain_tweets(screen_name)

    mutual, oneway, strange = relation_handler(gain_friends_id(screen_name), gain_followers_id(screen_name))

    print mutual
    print oneway
    print strange

if '__main__' == __name__ :

   user_parser('curmium') 
