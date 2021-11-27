from functools import lru_cache
import json
import logging
import requests

GENERIC_URL = "https://en.wikipedia.org/w/api.php?action=query&format=json&\
prop=links&meta=&titles={link}&pllimit=500"
STARTING_LINK = "german"  # import random random.choice(['Audi', 'german', 'Mercedes-Benz'])


"""
Those are refers to the searching function
"""
visited_wikis = set()
graph = {}


@lru_cache
def request_page(wiki_url):

    print(wiki_url)
    page = requests.get(GENERIC_URL.format(link=wiki_url))

    if page.status_code == 200:
        return page


@lru_cache
def parse_page_to_links(page):

    links = []

    page_data = json.loads(page.text)["query"]["pages"]
    page_data = page_data[list(page_data.keys())[0]]

    if "links" in list(page_data.keys()):
        page_data = page_data["links"]
        for i in page_data:
            links.append(i["title"])

    return links


@lru_cache
def get_links_from_url(wiki_url):
    page = request_page(wiki_url)
    links = parse_page_to_links(page)
    return links


def hitler_validation(links):
    return "Adolf Hitler" in links or "Hitler" in links


def search_for_hitler(visited_wikis, graph, wiki_url):

    if wiki_url not in visited_wikis:
        graph[wiki_url] = get_links_from_url(wiki_url)
        visited_wikis.add(wiki_url)
        if hitler_validation(graph[wiki_url]):
            logging.warning("Hitlerrrr")
            logging.critical(graph)
            return

        for wiki_sub_url in graph[wiki_url]:
            search_for_hitler(visited_wikis, graph, wiki_sub_url)


def main():
    search_for_hitler(visited_wikis, graph, STARTING_LINK)


if __name__ == "__main__":
    main()
