import re
import json
import requests
from pymongo    import MongoClient
from datetime   import date, datetime, timedelta
from lxml       import html
from lxml       import cssselect

host    = "https://mobile.twitter.com"
peers   = [
    {'name':'Hans Fangoh',  'link':'/ProfCompMod?p=s',  'role':'professor'},
    {'name':'Tiffany Horan','link':'/TiffanyHoran?p=i', 'role':'artist'},
    {'name':'Darius H',     'link':'/ComethTheNerd?p=s','role':'ms engineer'},
    {'name':'Danny mc',     'link':'/Danny_Mc12?p=s',   'role':'c# coder'},
    {'name':'Jiri Mocicka', 'link':'/givision?p=s',     'role':'DesignDirector'},
    {'name':'R Fouchaux',   'link':'/thefooshshow?p=s', 'role':'web teacher'},
    {'name':'Ev Williams',  'link':'/ev?p=s',           'role':'ios app owner'},
    {'name':'Ryan Seacrest','link':'/RyanSeacrest?p=s', 'role':'famous host'},
    {'name':'Jenna Lucas',  'link':'/JennaLucas81?p=s', 'role':'primary tcher'},
    {'name':'Adam Lofting', 'link':'/adamlofting?p=s',  'role':'a mozilla lead'}
]


# tweets json format:
# {
#   "name"      :   name,
#   "time"      :   time,
#   "tweets"    :   [{'tweet': tw1, 'time': ti1}, 
#                    {'tweet': tw2, 'time': ti2}]
# }
def get_tweets(peer):
    name = peer['name']
    link = peer['link']
    role = peer['role']
    time = str(date.today())
    t_cons_xpath = '//*[@id="main_content"]/div[2]/table'
    tweets = {"name":name, "time":time, "tweets": []}
    page_count = 1

    web_page = requests.get( host + link )
    print "STAT: Crawl start."

    while True:
        print "STAT: Start page %d tweets crawl. link : %s" % (page_count, link)
        tree     = html.fromstring(web_page.text.encode('utf8'))
        timeline = tree.cssselect('div.timeline')
        t_cons   = timeline[0].cssselect('table.tweet')
        for con in t_cons:
            tweet   = con.cssselect('div.tweet-text')[0].text_content()
            raw_time= con.cssselect('td.timestamp a')[0].text_content()
            time    = timer(raw_time)
            tweets["tweets"].append({'content':tweet, 'time':time})
        try:
            # refresh link
            link     = timeline[0].cssselect('div.w-button-more a')[0].get("href")
            # refresh web_page
            web_page = requests.get( host + link )
            page_count += 1
        except:
            break

    print "SUCC: Crawl done."
    return tweets

def timer(raw_time):

    # every tweet has a push time, and in twitter the push time has several
    # formats :
    # 1. only minutes:          xxm
    # 2. only hours:            xxh
    # 3. month and day:         mmm dd
    # 4. day, month and year:   dd mmm yy
    now              = datetime.now()
    year, month, day = now.year, now.month, now.day
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
        return str(push_time)
    elif 1 == len(time_list):
        # only minute : xxm
        if re.match(r'\d+m', time_list[0]):
            delta = timedelta(minutes = int(filter(str.isdigit, time_list[0])))
            push_d= now - delta
            push_time = date(push_d.year, push_d.month, push_d.day)
            print str(push_time)
        # only hours : xxh
        elif re.match(r'\d+h', time_list[0]):
            delta = timedelta(hours = int(filter(str.isdigit, time_list[0])))
            push_d= now - delta
            push_time = date(push_d.year, push_d.month, push_d.day)
            return str(push_time)
        else:
            return raw_time
    else:
        return raw_time

def check_redundant(client, peer):
    name = peer['name']
    tweets = client.mruirf.twitter_tweets

    if tweets.find_one({"name":name}):
        print "WARN: Already in database."
        return True
    else:
        print "STAT: Not in database."
        return False

def store(client, tweets_json):
    tweets = client.mruirf.twitter_tweets

    tweets.insert(tweets_json)
    print "SUCC: Stored."

if __name__ == '__main__':

    client = MongoClient('mongodb://localhost:27017/')

    tweets = client.mruirf.twitter_tweets

    for peer in peers:
        print peer['name'], "-"*50

        if False == check_redundant(client, peer):
            store(client, get_tweets(peer))

        print
