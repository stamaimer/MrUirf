import json
import requests
from lxml import html
from lxml import cssselect

host    = "https://mobile.twitter.com"
# tweets json format
# {name : [{'tweet': tw1, 'time': ti1}, {'tweet': tw2, 'time': ti2}]}
tweets  = {}
peers   = [
    {'name':'Hans Fangoh',  'link':'/ProfCompMod?p=s',  'role':'professor'},
    {'name':'Tiffany Horan','link':'/TiffanyHoran?p=i', 'role':'artist'},
    {'name':'Darius H',     'link':'/ComethTheNerd?p=s','role':'ms engineer'},
    {'name':'Danny mc',     'link':'/Danny_Mc12?p=s',   'role':'c# coder'},
    {'name':'Jiri Mocicka', 'link':'/givision?p=s',     'role':'DesignDirector'},
    {'name':'R. Fouchaux',  'link':'/thefooshshow?p=s', 'role':'web teacher'},
    {'name':'Ev Williams',  'link':'/ev?p=s',           'role':'ios app owner'},
    {'name':'Ryan Seacrest','link':'/RyanSeacrest?p=s', 'role':'famous host'},
    {'name':'Jenna Lucas',  'link':'/JennaLucas81?p=s', 'role':'primary tcher'},
    {'name':'Adam Lofting', 'link':'/adamlofting?p=s',  'role':'a mozilla lead'}
]

def get_tweets(peer):
    name = peer['name']
    link = peer['link']
    role = peer['role']
    t_cons_xpath = '//*[@id="main_content"]/div[2]/table'
    tweets = {name: []}
    page_count = 1

    web_page = requests.get( host + link )
    print name, '|', role, "-"*15

    while True:
        print "start page %d tweets crawl. link : %s" % (page_count, link)
        tree     = html.fromstring(web_page.text.encode('utf8'))
        timeline = tree.cssselect('div.timeline')
        t_cons   = timeline[0].cssselect('table.tweet')
        for con in t_cons:
            tweet = con.cssselect('div.tweet-text')[0].text_content()
            time  = con.cssselect('td.timestamp a')[0].text_content()
            tweets[name].append({'tweet':tweet, 'time':time})
        try:
            # refresh link
            link     = timeline[0].cssselect('div.w-button-more a')[0].get("href")
            # refresh web_page
            web_page = requests.get( host + link )
            page_count += 1
        except:
            break

    print "finished."
    return tweets


if __name__ == '__main__':

    tweets = []

    for peer in peers:
        tweets.append(get_tweets(peer))

    f = file('tweets.json', 'w+')
    json.dump(tweets, f)
    f.close()
