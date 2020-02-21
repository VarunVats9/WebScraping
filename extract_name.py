# import dependencies
from bs4 import BeautifulSoup
import requests
import re
import operator
import sys
from tabulate import tabulate
from stop_words import get_stop_words
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")

# path to chrome driver
chrome_driver_path = "/home/vvats/Downloads/chromedriver"
driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver_path)
#driver = webdriver.Chrome(chrome_driver_path)

# get name from site
name_link = "https://www.babynamesdirect.com/baby-names/sanskrit/girl/meaning/goddes"

if len(sys.argv) == 0:
	print("Enter python extract_name.py")
	exit()

# get page number
start = sys.argv[1]
end = sys.argv[2]

def callPagesWithinRange():
	full_list = []
	for page in range(int(start), int(end)):
		url = name_link + '/' + str(page)

		# open name site
		#print(url)
		driver.get(url)
		links = driver.find_elements_by_xpath(".//a")
		girl_links = []

		for link in links:
			girl_name_link = link.get_attribute('href')
			#print(girl_name_link)
			if "https://www.babynamesdirect.com/girl" in girl_name_link:
				girl_links.append(girl_name_link)

		print(url + " has total names : " + str(len(girl_links)))
		final_list = []
		for girl_link in girl_links:
			time.sleep(10)
			girl_name = girl_link.split("/")[-1]
			#print(girl_link)
			driver.get(girl_link)
			try:
				meaning = driver.find_element_by_xpath("//div[@class='sdata1']")
				point = driver.find_element_by_xpath("//s[@class='v']")
				final_list.append([int(point.text), girl_name, meaning.text])
				print('.', end='')
			except:
				print("Unable to fetch the page : " + girl_link)

		full_list.append(final_list)
		print_headers = ['Points', 'Name', 'Meaning']

		# reverse sort based on the points
		sorted(final_list, key=lambda x: x[0], reverse=True)

		# print the table with tabulate
		#print(tabulate(final_list, headers=print_headers, tablefmt='pipe'))

		# write to a file
		f = open(str(page) + ".txt", "w+")
		f.write(tabulate(final_list, headers=print_headers, tablefmt='fancy_grid'))
		f.close()

	# reverse sort based on the points
	sorted(full_list, key=lambda x: x[0], reverse=True)

	# print the table with tabulate
	#print(tabulate(final_list, headers=print_headers, tablefmt='fancy_grid'))

	# write to a file
	f = open("full_list.txt", "w+")
	f.write(tabulate(final_list, headers=print_headers, tablefmt='fancy_grid'))
	f.close()

try:
	callPagesWithinRange()
# throw an exception in case it breaks
except requests.exceptions.Timeout:
	print("The server didn't respond. Please, try again later.")

