# -*- coding: utf-8 -*-

import re
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

start_url = "http://m.facebook.com"
user_email= "curmium@gmail.com"
user_pass = "zhanhui"

def login(driver):

    driver.get(start_url)
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
    status_list     =[]
    content_xpath   ='/html/body/div/div/div[2]/div/div/div/div[1]/div[2]/div/div'

    print "crawl status in %s." % year_page_link['year']
    driver.get(year_page_link["link"])

    while True:

        # get status in current page
        content = driver.find_elements_by_xpath(content_xpath)
        if len(content) == 0: break
        for contain in content:
            try:
                status  = contain.find_element_by_xpath('./div[1]').find_element_by_tag_name('span').get_attribute('innerHTML')
                time    = contain.find_element_by_xpath('./div[2]/div[1]/abbr').get_attribute('innerHTML')
                t_filter= re.compile('<[^>]+>')
                status  = t_filter.sub("", status)
                status_list.append({'status':status, 'time':time})
            except:
                pass

        # get more status
        link    = get_expand_button(driver)[0]
        label   = link.get_attribute('innerHTML').encode('utf8')
        more    = ['展开', '更多']
        if label in more:   link.click()
        else:               break

    return status_list

def scan_status(peel):
    status      = []
    year_links  = []
    print "  ".join([peel['name'], "-"*30])

    # visit peel's timeline
    driver = webdriver.Firefox()
    login(driver)
    driver.get(peel['link'])
    driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div[1]/div[4]/a[1]').click()

    # get the year page links. 'year 2015', 'year 2014', ...
    for a in get_expand_button(driver):
        a_inner = a.get_attribute('innerHTML').encode('utf8')
        inner_d = filter(str.isdigit, a_inner) 
        if inner_d != '' and int(inner_d) in range(2005, datetime.now().year+1):
            year_links.append({"year":inner_d, "link":a.get_attribute('href')})

    # start peel executing
    for year_page_link in year_links:
        status += exec_year(driver, year_page_link)

    driver.close()
    print "finished."
    return status

def default_peel():
    return {'name':'Mark Hatlestad', 'link':
            'https://m.facebook.com/mark.hatlestad?fref=fr_tab'}

if __name__ == '__main__':

    peel = default_peel()
    f_status = {peel['name'] :scan_status(peel = default_peel())}

    f = file('status.json', 'w+')
    json.dump(f_status, f)
    f.close()
