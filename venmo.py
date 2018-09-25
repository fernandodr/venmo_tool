import re
import sys
import time
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

username = sys.argv[1]
password = sys.argv[2]


#the function that gives a list of people you've had transactions with
def get_list_names(username, password):
	print(username)
	print(password)

	driver = webdriver.Firefox()
	driver.get("https://venmo.com/account/sign-in/")
	# time.sleep(1)

	elem = driver.find_element_by_name('phoneEmailUsername')
	elem.clear()
	elem.send_keys(username)

	elem = driver.find_element_by_name('password')
	elem.clear()
	elem.send_keys(password)
	time.sleep(.1)
	elem.send_keys(Keys.RETURN)
	time.sleep(1)

	elem = driver.find_element_by_css_selector('button.ladda-button.mfa-button-code-prompt')
	elem.click()

	phone_code = raw_input("Enter the texted code: ")
	elem = driver.find_element_by_name('token')
	elem.clear()
	elem.send_keys(phone_code)
	time.sleep(.1)
	elem.send_keys(Keys.RETURN)
	time.sleep(2)

	elem = driver.find_element_by_class_name('ladda-button.auth-button')
	elem.click()
	time.sleep(2)

	driver.get("https://venmo.com/?feed=mine")

	html_code = driver.page_source
	times = html_code.count("<strong>")

	html_code = html_code[html_code.find("<strong>"):]
	sep = "<div id=\"classic-feed\" style=\"display: none;\">"
	rest = html_code.split(sep, 1)[0]

	names = []

	for x in range(0, times):
		name = rest[(rest.index("<strong>")+8):rest.index("</strong>")]
		rest = rest[(rest.index("</strong>")+9):]
		names.append(name)

	true_names = [str(x) for x in names]
	real_people = [x for x in true_names if x != "Fernando Rivera"]
	woduplicates = list(set(real_people))
	return woduplicates

#the function to check if the person fed from venmo list goes to UF
def attends(first_name, last_name):
	print(first_name)
	print(last_name)

	driver = webdriver.Firefox()
	driver.get("https://directory.ufl.edu/")
	time.sleep(1)

	elem = driver.find_element_by_class_name('input-radio')
	elem.click()


	elem = driver.find_element_by_id('directory-search-first')
	elem.clear()
	elem.send_keys(first_name)

	elem = driver.find_element_by_id('directory-search-last')
	elem.clear()
	elem.send_keys(last_name)
	time.sleep(.1)
	elem.send_keys(Keys.RETURN)
	time.sleep(1)

	username = raw_input('Enter your GatorLink: ')
	password = raw_input('Enter your password: ')

	elem = driver.find_element_by_id('username')
	elem.clear()
	elem.send_keys(username)

	elem = driver.find_element_by_id('password')
	elem.clear()
	elem.send_keys(password)
	time.sleep(.1)
	elem.send_keys(Keys.RETURN)
	time.sleep(1)

	link = "https://directory.ufl.edu/private/search/?f=" + first_name + "&l=" + last_name + "&e=&a=student"

	driver.get(link)
	time.sleep(1)
	no_results = "yielded no results."

	html = driver.page_source

	if (no_results in html):
		return False
	else:
		return True




my_transactions_people = get_list_names(username, password)

uf_students_with_transactions = []

for name in my_transactions_people:
	first = name[:name.index(" ")]
	last = name[(name.index(" ")+1):]
	if (attends(first, last) == True):
		uf_students_with_transactions.append(name)

print uf_students_with_transactions





