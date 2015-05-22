# -*- coding: utf-8 -*-

'''
    MEMO
    2015-05-06
    Facebook is really a mean guy, grasping all of its data and never sharing.
So it makes status auto collection much harder, and finally we have to use web
auto test tool selenium to collect status. This way we could detour a few trival
things, such as login and collecting status without authorizing by every user.
However, this method has a huge disadvantage: cost great deal of time, because
using selenium to collect data is the same as people visiting website, the only
difference is that program can execute(ex. click) quicker than human beings.
That means we will waste lots of time to wait webpage loading.
    So unlike twitter, we could not collect huge data from facebook.
'''

import re
import json
from pymongo  import MongoClient
from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

HOST = "http://m.facebook.com"

def login(driver):

    with file('facebook.account', 'r') as f:
        account_data = json.load(f)
    user_email = account_data['email']
    user_pass  = account_data['pass']

    driver.get(HOST)
    driver.find_element_by_name('email').send_keys(user_email)
    driver.find_element_by_name('pass').send_keys(user_pass)
    driver.find_element_by_name('login').click()

    print "Logged in."

def get_expand_button(driver):
    a_list = []

    con_contain = driver.find_element_by_id('structured_composer_async_container')
    con_divs    = con_contain.find_elements_by_tag_name('div')
    for a_contain in [d for d in con_divs if d.get_attribute('class') == 'i']:
        a_list.append(a_contain.find_element_by_tag_name('a'))

    return a_list

def exec_year(driver, year_page_link):
    status_list   =[]
    content_xpath ='/html/body/div/div/div[2]/div/div/div/div[2]/div[2]/div/div'

    print "crawl status in %s." % year_page_link['year']
    driver.get(year_page_link["link"])

    while True:

        # get status in current page
        content = driver.find_elements_by_xpath(content_xpath)
        if len(content) == 0: break
        for contain in content:
            try:
                status  = contain.find_element_by_xpath('./div[1]').find_element_by_tag_name('span').get_attribute('innerHTML')
                raw_time= contain.find_element_by_xpath('./div[2]/div[1]/abbr').get_attribute('innerHTML')
                time    = timer(raw_time)
                t_filter= re.compile('<[^>]+>')
                status  = t_filter.sub("", status)
                print status
                status_list.append({'content':status,'time':time,'flag':'00000'})
                # the flag means refer to twitter/collector_by_web.py explanation
            except:
                pass

        # get more status
        link    = get_expand_button(driver)[0]
        label   = link.get_attribute('innerHTML').encode('utf8')
        more    = ['展开', '更多']
        if label in more:   link.click()
        else:               break

    return status_list

def scan_name_and_status(peer):
    username = peer['username']
    link     = peer['link']
    status      = []
    year_links  = []
    print "  ".join([username, "-"*30])

    # visit peer's homepage
    driver = webdriver.Firefox()
    login(driver)
    driver.get(link)

    # get name
    name = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/span[1]/strong').get_attribute('innerHTML')

    # visit peer's timeline
    driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div[1]/div[4]/a[1]').click()

    # get the year page links. 'year 2015', 'year 2014', ...
    for a in get_expand_button(driver):
        a_inner = a.get_attribute('innerHTML').encode('utf8')
        inner_d = filter(str.isdigit, a_inner) 
        if inner_d != '' and int(inner_d) in range(2005, datetime.now().year+1):
            year_links.append({"year":inner_d, "link":a.get_attribute('href')})

    # start peer executing
    for year_page_link in year_links:
        status += exec_year(driver, year_page_link)

    driver.close()
    print "finished."
    return name, status

def timer(raw_time):

    # every status has a push time, and in facebook the push time has several
    # formats :
    # 1. only hour                  hh 小时
    # 2. year and month             yyyy年mm月
    # 3. year, month and day        yyyy年mm月dd日
    # 4. month, day and time        mm月dd日上午 xx:xx
    # 5. year, month, day and time  yyyy年mm月dd日上午 xx:xx
    # sample = [
    #     u'15 小时', u'2013年4月', u'2014年9月22日', u'1月10日上午 4:12',
    #     u'2013年4月19日上午 9:28'
    # ]
    now              = datetime.now()
    year, month, day = now.year, now.month, now.day
    time_list        = [d for d in re.split('\D+', raw_time) if d != '']

    if 5 == len(time_list):
        # year, month, day and time  yyyy年mm月dd日上午 xx:xx
        year      = int(time_list[0])
        month     = int(time_list[1])
        day       = int(time_list[2])
        push_time = date(year, month, day)
        return str(push_time)
    elif 4 == len(time_list):
        # month, day and time        mm月dd日上午 xx:xx
        month     = int(time_list[0])
        day       = int(time_list[1])
        push_time = date(year, month, day)
        return str(push_time)
    elif 3 == len(time_list):
        # year, month and day        yyyy年mm月dd日
        year      = int(time_list[0])
        month     = int(time_list[1])
        day       = int(time_list[2])
        push_time = date(year, month, day)
        return str(push_time)
    elif 2 == len(time_list):
        # year and month             yyyy年mm月
        year      = int(time_list[0])
        month     = int(time_list[1])
        push_time = date(year, month, 1)
        return str(push_time)
    elif 1 == len(time_list):
        # only hour                  hh 小时
        hour      = int(time_list[0])
        delta     = timedelta(hours = hour)
        push_d    = now - delta
        push_time = date(push_d.year, push_d.month, push_d.day)
        return str(push_time)
    else:
        return raw_time

def fetch_status(username, page_no, page_size = 20):
    client = MongoClient('mongodb://localhost:27017/')
    status = client.msif.facebook_status
    peer   = status.find_one({'username':username})
    page_no= int(page_no)
    texts  = peer['texts'][(page_no-1)*page_size:page_no*page_size]
    return texts

def fetch_raw_status(username, index):
    client = MongoClient('mongodb://localhost:27017/')
    status = client.msif.facebook_status
    peer   = status.find_one({'username':username})
    texts  = peer['texts']
    return texts[int(index)]

def get_peer():

    with file('facebook.account', 'r+') as f:
        account_data = json.load(f)
    link = account_data['default_peer_link']
    username = re.split(r'facebook.com/', link)[1].split('?')[0]
    link = "%s/%s" % (HOST, username)
    return [{'link':link, 'username':'@'+username}]

if __name__ == '__main__':

    peer = get_peer()
    f_status = []
    for p in peer:
        # p['username'] get
        # p['link'] get
        now = datetime.now()
        now_date   = date(now.year, now.month, now.day)
        p['time']  = str(now_date)
        name,status= scan_name_and_status(p)
        p['name']  = name
        p['texts'] = status
        f_status.append(p)

    f = file('status.json', 'w+')
    json.dump(f_status, f)
    f.close()

