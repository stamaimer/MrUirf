# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

LOGIN_ENDPOINT = "https://www.douban.com/accounts/login"

def login():
	
	browser = webdriver.Chrome()

	browser.get(LOGIN_ENDPOINT)

	browser.find_element_by_id("email").send_keys(EMAIL)

	browser.find_element_by_id("password").send_keys(PASSWORD)

	browser.find_element_by_name("login").send_keys(Keys.RETURN)
	



