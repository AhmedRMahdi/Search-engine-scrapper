import re
import sys
import requests
from bs4 import BeautifulSoup

sys.append(os.getenv('UT_PATH'))
from headers import random_desktop_header


SEARCH_ENGINE = {
    'google': 'https://www.google.co.uk/search?q={0}&start={1}',
    'bing': 'https://www.bing.com/search?q={0}&first={1}'
}


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
                raise ValueError, 'pages start from 1. Please re-enter a number greater than or equal to 1'
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


def clean_urls_g(alist, soupobj, aclass):
    # for google
    start_letter, start_number, stop_char = 'h', 0, '&'

    for d in soupobj.select('div.{0}'.format(aclass)):
        link = d.select_one('a')
        if link is not None:
            tp = link['href']
            new = ''
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


def clean_urls_b(alist, soupobj, aclass):
    # for bing
    for d in soupobj.select('li.{0}'.format(aclass)):
        link = d.select_one('a')
        alist.append(link['href'])
    return alist


def get_links(url, aclass):
    soup_obj = make_soup_obj(get_url(url))
    url_list = []
    if aclass == 'BING_CLASS':
        return clean_urls_b(url_list, soup_obj, aclass)
    else:
        return clean_urls_g(url_list, soup_obj, aclass)


# x = query('bing', 'c programming')
# print get_links(x, BING_CLASS)
# print x


# returns -- 'https://www.google.co.uk/search?q=c+programming'
# x = query(SEARCH_ENGINE['google'], 'c programming')

# print get_links(x, GOOGLE_CLASS)


# go through pages in google: start=0 is page 1, start=10 is page 2, start=20 is page 3 etc.
# e.g. https://www.google.co.uk/search?q=c+programming&start=20  <-- is page 3 of 'c programming' search


# further research: https://github.com/NikolaiT/GoogleScraper
# https://www.google.co.uk/search?q=c+to+speed+up+web+scraping
