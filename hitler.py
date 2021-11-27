from functools import lru_cache
import requests
import random
import json
import re


GENERIC_URL = 'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=links&meta=&titles=$LINK$&pllimit=500'
STARTING_LINK = 'german' # random.choice(['Audi', 'german', 'Mercedes-Benz'])


@lru_cache
def request_page(wiki_url):
	try:
		print(wiki_url)
		page = requests.get(GENERIC_URL.replace('$LINK$', wiki_url))
	except Exception as e:
		print(e)
		return

	if page.status_code == 200:
		return page
		

@lru_cache
def parse_page_to_links(page):
	links = []

	page_data = json.loads(page.text)['query']['pages']
	page_data = page_data[list(page_data.keys())[0]]
	
	if 'links' in list(page_data.keys()):
		page_data = page_data['links']
		[links.append(i['title']) for i in page_data]

	return links


@lru_cache
def get_links_from_url(wiki_url):
	page = request_page(wiki_url)
	links = parse_page_to_links(page)
	return links


def hitler_validation(links):
	return 'Hitler' in links or 'Adolf Hitler' in links


visited_wikis = set()
graph = {}

def dfs(visited_wikis, graph, wiki_url):

	if wiki_url not in visited_wikis:
		graph[wiki_url] = get_links_from_url(wiki_url)
		visited_wikis.add(wiki_url)

		if hitler_validation(graph[wiki_url]):
			print("Hitlerrrr"); print(graph)
			return  

		for wiki_sub_url in graph[wiki_url]:
			dfs(visited_wikis, graph, wiki_sub_url)


def main():
	dfs(visited_wikis, graph, STARTING_LINK)
	print(graph)


if __name__ == '__main__':
	main()	
