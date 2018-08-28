import sys
import argparse
from time import time
import random

from se_scraper import query, get_links

from proxies.csvsaver import SaveToCSV



def get_parser():
    parser = argparse.ArgumentParser(
        description='Search engine scraping via the command line')
    parser.add_argument('query', metavar='QUERY', type=str,
                        help='The query you want to scrape, '
                        'this can be like any normal text you would enter into a search engine. '
                        'Note: put query into quotations')
    parser.add_argument('--engine', help='What search engine you want to scrape. '
                        '<options>: google (default), bing', 
                        type=str, required=False, default='google')
    parser.add_argument('--pages', help='<optional>: The number of pages to scrape, starting at 1',
                        default=1, type=int, required=False)

    return parser


def clr():
    parser = get_parser()
    args = parser.parse_args()

    q = args.query
    s_engine = args.engine
    pages = args.pages

    return q, s_engine, pages

def main():
    css_classes = {
        'GOOGLE': 'g',
        'BING': 'b_algo'
    }
    q, s_engine, pages = clr()

    if pages == 1:
        query_url = query(s_engine, q, pages=pages)
        links = get_links(query_url, css_classes.get(s_engine.upper()))
    else:
        for i in xrange(1, pages+1):
            time.sleep(randome.choice(xrange(5, 60)))
            query_url = query(s_engine, q, pages=i)
            links = get_links(query_url, css_classes.get(s_engine.upper()))

    output_file = q.replace(' ', '_') + '.csv'
    SaveToCSV(output_file, links)


if __name__ == '__main__':
    main()
