# -*- coding: utf-8 -*-

'''
    BRIEF
    In this file, the function 'get_tweets' will crawl users' tweets.
    And function 'get_followers' will crawl users' followers to enlarge peers.
    Function 'store' will store users' tweets in mongodb.
    And this file only crawl the tweets and followers of selected seed users and 
never recognizing the language, though in this period we only need tweets in
English.

    MEMO
    2015-04-23
    In first test, we prefer to filter out those users whoes tweets count more
than 16000, the more the better. Because we believe the more tweets the user push
the more active the user is, and it is a effective way to downsize seed user, we 
choose those users to construct our corpus. However, we find there exist an 
insidious problem, there exist a sinew between tweet count and follower count. 
To explain in detail, if a user push too many tweets, there may have two factors.
First is that this user use twitter too frequent to make complete sentences or 
include important infomation. Secondly, if a person push tweets happily and
endlessly, he/she might be a famous user and using the twitter account in a 
commercial use, he/she may has many followers, but they always or all the way 
push ads, it's harmful to our system. So in second test, we will try to lower 
our tweets count limit and add followers count limit. 
'''

import re
import json
import requests
from pymongo    import MongoClient
from datetime   import date, datetime, timedelta
from lxml       import html
from lxml       import cssselect

HOST    = "http://mobile.twitter.com"

# tweets json format:
# {
#   "name"      :   name,
#   "username"  :   username,
#   "time"      :   time,
#   "link"      :   link,
#   "tweets"    :   [{'tweet': tw1, 'time': ti1, 'flag': fg1},
#                    {'tweet': tw2, 'time': ti2, 'flag': fg2}]
# }
def get_tweets(peer):
    name = peer['name']
    unam = peer['username']
    link = peer['link']
    time = str(date.today())
    t_cons_xpath = '//*[@id="main_content"]/div[2]/table'
    tweets = {"name":name, "username":unam, "time":time, 
              "link":link, "texts": []}
    page_count = 1

    web_page = requests.get( HOST + link )
    print "STAT: Crawl tweets start."

    while True:
        if page_count == 1 or page_count % 10 == 0:
            print "STAT: Start page %d tweets crawl. link : %s" \
                    % (page_count, link)

        tree     = html.fromstring(web_page.text.encode('utf8'))
        timeline = tree.cssselect('div.timeline')
        t_cons   = timeline[0].cssselect('table.tweet')

        for con in t_cons:
            # check retweet
            try:
                repost = con.cssselect('tr.tweet-content')[0]
                continue
            except: pass

            tweet   = con.cssselect('div.tweet-text')[0].text_content()
            raw_time= con.cssselect('td.timestamp a')[0].text_content()
            time    = timer(raw_time)

            # the flag tag has three flag bit
            # 1. tokenization flag: '0' means no, '1' means already done
            # 2. pos tagging flag
            # 3. ner flag
            # 4. relevance flag for chi square
            # 5. relevance flag for pos pattern
            tweets["texts"].append({'content':tweet, 'time':time, 'flag':'00000'})

        try:
            # refresh link
            link     = timeline[0].cssselect('div.w-button-more a')[0].get("href")
            # refresh web_page
            web_page = requests.get( HOST + link )
            page_count += 1

        except:
            break

    print "SUCC: Crawl %s tweets." % len(tweets['texts'])
    print "SUCC: Crawl tweets done."
    return tweets

def get_followers(peer, filter = False):
    name = peer['name']
    link = peer['link']
    fers = []
    page_count = 1

    web_page = requests.get( HOST + link )
    tree     = html.fromstring(web_page.text.encode('utf8'))
    fer_butt = tree.cssselect('td.stat')[2]
    fer_link = fer_butt.cssselect('a')[0].get('href')
    web_page = requests.get( HOST + fer_link )
    print "STAT: Crawl followers start."

    while True:
        print "STAT: Start page %d followers crawl." % page_count
        tree     = html.fromstring(web_page.text.encode('utf8'))
        foll_line= tree.cssselect('div.user-list')[0]
        f_cons   = foll_line.cssselect('table.user-item')

        for con in f_cons:
            f_fullname  = con.cssselect('strong.fullname')[0].text_content()
            f_username  = con.cssselect('span.username')[0].text_content()
            f_link      = con.cssselect('td.screenname a')[1].get("href")
            fers.append({'name':f_fullname, 'username':f_username,
                         'link':f_link})
        try:
            # refresh link
            link     = foll_line.cssselect('div.w-button-more a')[0].get("href")
            # refresh web_page
            web_page = requests.get( HOST + link )
            page_count += 1
        except:
            break

        # first of all, if page_count over 30000, 
        # server may face the risk of segmentation fault. (server RAM : 1GB)
        # secondly, crawling users' former 10 pages of followers do not break
        # the randomness of sample corpus
        # and honestly, it's no use to crawl too many users in vain
        if page_count > 10 :
            print "WARN: Satisfied and break."
            break

    if filter:
        print "WARN: Filter flag opened."
        print "STAT: Filter start. "
        print "STAT: Filter out users whose tweet less than 10000 but over 5000"
        print "STAT: & followers less than 3000."

        follower_count = len(fers)
        print "STAT: %s selected followers in all." % follower_count

        for i, follower in enumerate(fers[::-1]):
            f_name = follower['name']
            f_link = follower['link']
            f_page = requests.get( HOST + f_link )
            f_tree = html.fromstring(f_page.text.encode('utf8'))
            f_twee = f_tree.cssselect('td.stat')[0]
            f_tnum = f_twee.cssselect('div.statnum')[0].text_content()
            f_tnum = int("".join(f_tnum.split(',')))
            f_fers = f_tree.cssselect('td.stat')[2]
            f_fnum = f_fers.cssselect('div.statnum')[0].text_content()
            f_fnum = int("".join(f_fnum.split(',')))

            if 5000 > f_tnum or f_tnum > 10000 or f_fnum > 3000:
                fers.remove(follower)

            if 0 == i % 20:
                print "STAT: %s %% filtered." \
                        % str( 100 * float(i) / follower_count  )[:5]

        print "SUCC: Filter done. %s followers filtered out." % len(fers)

    print "SUCC: Crawl followers done."
    return fers

def timer(raw_time):

    # every tweet has a push time, and in twitter the push time has several
    # formats :
    # 1. only minutes:          xxm
    # 2. only hours:            xxh
    # 3. only seconds:          xxs
    # 4. now                    now
    # 5. month and day:         mmm dd
    # 6. day, month and year:   dd mmm yy
    now              = datetime.now()
    year, month, day = now.year, now.month, now.day
    today            = date(year, month, day)
    month_dict       = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 
                        'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    time_list        = raw_time.split()

    if 3 == len(time_list):
        # day, month and year : dd mmm yy
        year      = int('20' + time_list[2])
        month     = month_dict[time_list[1]]
        day       = int(time_list[0])
        push_time = date(year, month, day)
        return str(push_time)
    elif 2 == len(time_list):
        # month and day : mmm dd
        month     = month_dict[time_list[0]]
        day       = int(time_list[1])
        push_time = date(year, month, day)
        if push_time > today: push_time = date(year-1, month, day)
        return str(push_time)
    elif 1 == len(time_list):
        # only minute : xxm
        if re.match(r'\d+m', time_list[0]):
            delta = timedelta(minutes = int(filter(str.isdigit, time_list[0])))
            push_d= now - delta
            push_time = date(push_d.year, push_d.month, push_d.day)
            return str(push_time)
        # only hours : xxh
        elif re.match(r'\d+h', time_list[0]):
            delta = timedelta(hours = int(filter(str.isdigit, time_list[0])))
            push_d= now - delta
            push_time = date(push_d.year, push_d.month, push_d.day)
            return str(push_time)
        # only seconds : xxs
        elif re.match(r'\d+s', time_list[0]):
            push_d= now
            push_time = date(push_d.year, push_d.month, push_d.day)
            return str(push_time)
        # now
        elif re.match(r'now', time_list[0]):
            push_d= now
            push_time = date(push_d.year, push_d.month, push_d.day)
            return str(push_time)
        else:
            return raw_time
    else:
        return raw_time

def check_redundant(client, peer):
    username = peer['username']
    tweets   = client.mruirf.twitter_tweets

    if tweets.find_one({"username":username}):
        print "WARN: Already in database."
        return True
    else:
        print "STAT: Not in database."
        return False

def store(client, tweets_json):
    tweets = client.mruirf.twitter_tweets

    tweets.insert(tweets_json)
    print "SUCC: Stored."

def fetch_tweets(username, page_no, page_size = 20):
    client = MongoClient('mongodb://localhost:27017/')
    tweets = client.msif.twitter_tweets
    peer   = tweets.find_one({'username':username})
    page_no= int(page_no)
    texts  = peer['texts'][(page_no-1)*page_size:page_no*page_size]
    return texts

def fetch_raw_tweet(username, index):
    client = MongoClient('mongodb://localhost:27017/')
    tweets = client.msif.twitter_tweets
    peer   = tweets.find_one({'username':username})
    texts  = peer['texts']
    return texts[int(index)]

def get_default_peers():

    # the following peers have too many tweets and do not contain many important
    # infomation
    #{'name':'Hans Fangoh',  'link':'/ProfCompMod',  'username':'@ProfCompMod'},
    #{'name':'Tiffany Horan','link':'/TiffanyHoran', 'username':'@TiffanyHoran'},
    #{'name':'Danny mc',     'link':'/Danny_Mc12',   'username':'@Danny_Mc12'},
    #{'name':'Jiri Mocicka', 'link':'/givision',     'username':'@givision'},
    #{'name':'R Fouchaux',   'link':'/thefooshshow', 'username':'@thefooshshow'},
    #{'name':'Ev Williams',  'link':'/ev',           'username':'@ev'},
    #{'name':'Ryan Seacrest','link':'/RyanSeacrest', 'username':'@RyanSeacrest'},
    #{'name':'Jenna Lucas',  'link':'/JennaLucas81', 'username':'@JennaLucas81'},
    #{'name':'Adam Lofting', 'link':'/adamlofting',  'username':'@adamlofting'},
    #{'name':'Ginger Kadlec','link':'/GingerKadlec', 'username':'@GingerKadlec'},
    #{'name':'David Chan',   'link':'/chanatown',    'username':'@chanatown'}

    peers   = [
    {'name':'Amy Shearn', 'link':'/amyshearn', 'username':'@amyshearn'}
    ]

    return peers


if __name__ == '__main__':

    client = MongoClient('mongodb://localhost:27017/')
    peers  = get_default_peers()
    e_peer = []

    for peer in peers:

        try:

            print "STAT: %s users have already recorded in database." \
                    % client.mruirf.twitter_tweets.count()
            print peer['name'].encode('utf8'), "-"*50

            # get tweets
            if False == check_redundant(client, peer):
                store(client, get_tweets(peer))

            # get followers
            # corpus is built up, do not need get followers any more
            # if len(peers) < 3000:
            #     followers = get_followers(peer, True)
            #     for follower in followers:
            #         peers.append(follower)

            print
            print

            # log: 2015-04-17 get an 1000p corpus
            # log: 2015-04-23 add more 2000p
            if client.mruirf.twitter_tweets.count() > 3000 : break

        except:

            e_peer.append(peer)
