import re
import sys
import requests
from bs4 import BeautifulSoup

from user_agents import random_desktop_headers


SEARCH_ENGINE = {
	'google': 'https://www.google.co.uk/search?q={0}&start={1}',
	'bing': 'https://www.bing.com/search?q={0}&first={1}'
}

GOOGLE_CLASS = 'g'

def get_engine(engine_name):
	return SEARCH_ENGINE.get(engine_name, SEARCH_ENGINE['google'])


def query(engine, *queries, **page):
	"""turns params into search engine recognised query"""

	if engine == 'bing':
		return bing_query(get_engine('bing'), *queries, **page)
	else:
		return google_query(get_engine('google'), *queries, **page)


def google_query(engine, *queries, **page):
	"""turns params into a google recognised query"""

	if page:
		if not len(page) > 1:
			if not page.values()[0] < 1:
				link_start_number = (page.values()[0] - 1) * 10
			else:
				return 'pages start from 1. Please re-enter a number greater than or equal to 1'
		else:
			return 'there can only be 1 kwarg maximum'
	else:
		link_start_number = 0 

	return engine.format(' '.join(queries).replace(' ', '+'), link_start_number)


def bing_query(engine, *queries, **page):
	"""turns params into a bing recognised query"""
	if page:
		if not len(page) > 1:
			if not page.values()[0] < 1:
				link_start_number = (page.values()[0] * 10) - 9 
			else:
				return 'pages start from 1. Please re-enter a number greater than or equal to 1'
		else:
			return 'there can only be 1 kwarg maximum'
	else:
		link_start_number = 0 

	return engine.format(' '.join(queries).replace(' ', '+'), link_start_number)


def get_url(url):
	return requests.get(url, headers=random_desktop_headers(), timeout=1)


def make_soup_obj(opened_link):
	data = opened_link.text.encode('utf-8')
	return BeautifulSoup(data, 'html.parser')



def clean_urls(alist, soupobj, aclass):

	for d in soupobj.select('div.{0}'.format(aclass)):
		link = d.select_one('a')
		if not link is None:
			tp = link['href']
			new =''
			start_letter = 'h'
			start_number = 0
			stop_char = '&'
			for char in tp:
				if char == stop_char:
					break
				else:
					if char == start_letter or start_number > 0:
						new += char
						start_number += 1
					else:
						pass 
			alist.append(new)
	return alist


def get_links(url, aclass):
	soup_obj = make_soup_obj(get_url(url))
	url_list = []
	return clean_urls(url_list, soup_obj, aclass)


# returns -- 'https://www.google.co.uk/search?q=c+programming'
x = query(SEARCH_ENGINE['google'], 'c programming')

# print get_links(x, GOOGLE_CLASS)




# go through pages in google: start=0 is page 1, start=10 is page 2, start=20 is page 3 etc.
# e.g. https://www.google.co.uk/search?q=c+programming&start=20  <-- is page 3 of 'c programming' search


# further research: https://github.com/NikolaiT/GoogleScraper
# https://www.google.co.uk/search?q=c+to+speed+up+web+scraping












