import sys
import argparse


def get_parser():
	parser = argparse.ArgumentParser(description='Search engine scraping via the command line')
	parser.add_argument('query', metavar='QUERY', type=str,
	                    help='query you want to scrape ')
	parser.add_argument('engine', type=str, 
	                    help='what search engine you want to scrape ')
	parser.add_argument('pages', help='number of pages to scrape', default=1, type=int)

	return parser

def clr():
	parser = get_parser()
	args = vars(parser.parse_args())
	# args = parser.parse_args()

	query = args['query']
	s_engine = args['engine']
	pages = args['pages']


if __name__ == '__main__':
	clr()