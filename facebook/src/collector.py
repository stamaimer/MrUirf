# -*- coding: utf-8 -*-

import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

start_url = "http://m.facebook.com"
user_email= "wendyfrank@126.com"
user_pass = "wendyfrank"
year_links= []

def login(driver):
    driver.get(start_url)
    email = driver.find_element_by_name('email')
    passwd = driver.find_element_by_name('pass')
    email.send_keys(user_email)
    passwd.send_keys(user_pass)
    driver.find_element_by_name('login').click()

driver = webdriver.Firefox()
login(driver)

# visit obama
driver.get("http:m.facebook.com/barackobama?refid=46&sld=eyJzZWFyY2hfc2lkIjoiNGZmZWUxMmQ3NTQ3MzJlMDQwNjlkOWE3ZTczZTUzMTgiLCJxdWVyeSI6Im9iYW1hIiwic2VhcmNoX3R5cGUiOiJTZWFyY2giLCJzZXF1ZW5jZV9pZCI6NDU0NzY1NjE0LCJwYWdlX251bWJlciI6MSwiZmlsdGVyX3R5cGUiOiJTZWFyY2giLCJlbnRfaWQiOjY4MTU4NDE3NDgsInBvc2l0aW9uIjowLCJyZXN1bHRfdHlwZSI6Mjc0fQ%3D%3D")

# open 'homepage'
# driver.find_element_by_xpath('/html/body/div/div/div[1]/div/div/a[3]').click()

year_start  = 2005
year_now    = datetime.now().year
year_list   = range(year_start, year_now+1)
button_contain  = driver.find_element_by_id('u_0_0')
print button_contain
a_contains      = button_contain.find_elements_by_class_name('i')

print year_list

print a_contains
for a_contain in a_contains:
    a = a_contain.find_elements_by_tag_name('a')
    digit = filter(str.isdigit, a.get_attribute('innerHTML')) 
    print digit
    if int(digit) in year_list:
        year_links.append({"year":digit, "link":a.get_attribute('href')})

print year_links

def exec_year(driver, year_page_link):
    driver.get(year_page_link["link"])

    while True:
        status_contains = driver.find_elements_by_class_name("bz")
        for contain in status_contains:
            contain = contain.find_element_by_tag_name('span')
            status  = contain.get_attribute('innerHTML')
            t_filter= re.compile('<[^>]+>')
            status  = t_filter.sub("", status)
            print status
            print
        button_contain  = driver.find_element_by_id('u_0_0')
        a_contain       = button_contain.find_elements_by_class_name('i')
        first_a         = a_contain[0].find_element_by_tag_name('a')
        inner           = first_a.get_attribute(innerHTML)
        if inner == "展开":
            first_a.click()
        else:
            break

for year_page_link in year_links:
    exec_year(driver, year_page_link['link'])




