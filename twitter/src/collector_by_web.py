import json
import requests
from lxml import html
from lxml import cssselect

host    = "https://mobile.twitter.com"
# tweets json format
# {name : [{'tweet': tw1, 'time': ti1}, {'tweet': tw2, 'time': ti2}]}
tweets  = {}
peers   = [{'name':'stamaimer', 'link':'https://mobile.twitter.com/stamaimer?p=s'},
           {'name':'Fenng',     'link':'https://mobile.twitter.com/Fenng?p=s'}]

def get_tweets(peer):
    name = peer['name']
    link = peer['link']
    t_cons_xpath = '//*[@id="main_content"]/div[2]/table'
    tweets = {name: []}
    page_count = 1

    web_page = requests.get(link)
    print name, "-"*30

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
            web_page = requests.get(host + link)
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
