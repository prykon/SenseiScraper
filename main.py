import os
from sty import fg, bg, ef, rs

os.system('clear')
print("%s   _____                      _      _____                                %s"%(fg(20) , bg.rs))
print("%s  / ___/___  ____  ________  (_)    / ___/______________ _____  ___  _____%s"%(fg(56) , bg.rs))
print("%s  \__ \/ _ \/ __ \/ ___/ _ \/ /_____\__ \/ ___/ ___/ __ `/ __ \/ _ \/ ___/%s"%(fg(92) , bg.rs))
print("%s ___/ /  __/ / / (__  )  __/ /_____/__/ / /__/ /  / /_/ / /_/ /  __/ /    %s"%(fg(128) , bg.rs))
print("%s/____/\___/_/ /_/____/\___/_/     /____/\___/_/   \__,_/ .___/\___/_/     %s"%(fg(164) , bg.rs))
print("%s                                                      /_/                 %s"%(fg(200) , bg.rs))

print('Starting script...')
print('Loading modules...', end=" ")

domain_name = "www.example.com"

import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import keys
from selenium.webdriver.support.ui import Select
print('done.')

options = Options()
options.add_argument("--disable-javascript")
options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications" : 2})

geo = input('What destination do you wish to scrape?: ')
my_tags = input('What additional tags do you want to add to the DB for these items? (comma separated): ').split(',')

browser = webdriver.Chrome(options=options)

print('Loading page...')
main_page = 'https://%s/hoteles/'%domain_name
browser.get(main_page)
time.sleep(2)
print('Done.')
browser.find_element_by_class_name('widget_fb_close').click()
searchbox = browser.find_element_by_xpath("//input[contains(@class, 'autosuggest-desktop data-hj-whitelist')]")
searchbox.send_keys(geo)
time.sleep(2)

searchbox.send_keys(keys.Keys.ENTER)

browser.find_element_by_xpath("//button[contains(@class, 'button__button___2Yslp button__button--large___e-xBY search-button')]").click()
time.sleep(2)

listing_url = browser.current_url


time.sleep(5)
if listing_url == main_page:
	print('The website doesn\'t recognize this geo.'+fg.rs)
	browser.close()
else:
	print('Geo found! Loading page...')
	listing_url = re.sub(r"\/\d{2}-\d{2}-\d{4}\/\d{2}-\d{2}-\d{4}\/",'/{{from}}/{{to}}/', listing_url)
	#time.sleep(30)
	input('\nPress ENTER key when content finishes loading.')	
	print('Let the scraping begin!')
	print('Preparing some BeautifulSoup...')
	from bs4 import BeautifulSoup

	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(2)
	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(2)
	soup = BeautifulSoup(browser.page_source, 'lxml')

	print('Scraping items...')
	try:
		items = soup.find_all("a", {"class": re.compile("link__link___.*?")})[2:]
	except:
		print('Items where not loaded. Waiting 10 more seconds...')
		time.sleep(10)
		items = soup.find_all("a", {"class": re.compile("link__link___.*?")})[2:]

	print('%i items found.'%(len(items)/2))

	print('Loading DB...')
	#Database stuff
	import mysql.connector
	import SenseiScraper as scraper
	scraper.geo = geo

	current_page = 1

	print("Scraping page %i"%current_page)
	scraper.scrape(items, listing_url,my_tags)
	button_next = browser.find_element_by_xpath('//*[@id="__next"]/div[2]/section[2]/main/nav/div[2]/button')
	
	while button_next.is_enabled():
		button_next.click()
		time.sleep(5)
		soup = BeautifulSoup(browser.page_source, 'lxml')
		items = soup.find_all("a", {"class": re.compile("link__link___.*?")})[2:]
		print("Scraping page %i"%current_page)
		current_page = current_page + 1
		scraper.scrape(items, browser.current_url,my_tags)

	print('Done!'+fg.rs)
	browser.close()