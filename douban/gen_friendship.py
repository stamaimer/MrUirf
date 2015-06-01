# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

LOGIN_ENDPOINT = "https://www.douban.com/accounts/login"

def login(email, password):
	
	try:

		browser = webdriver.Chrome()

		browser.get(LOGIN_ENDPOINT)

		browser.find_element_by_id("email").send_keys(email)

		browser.find_element_by_id("password").send_keys(password)

		browser.find_element_by_name("login").send_keys(Keys.RETURN)

		#how to check if login sucess?
	
		print "login success ... "

		return browser

	except Exception, exception:

		print str(exception)

		raise exception

def start(username, depth):

	handle = login("", "")

	

