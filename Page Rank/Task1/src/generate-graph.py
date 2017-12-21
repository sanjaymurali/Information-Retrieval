"""
    Author: Sanjay Murali
    Course: CS 6200 - Information Retrieval
    Task: Generating Graph
"""

from bs4 import BeautifulSoup
import urllib2
import re
import os


BASE_URL = "https://en.wikipedia.org"
URL_LIST = "url_list_dfs.txt"
GRAPH_NAME = "graph-2.txt"
CRAWLED_URL = []
DICTIONARY = dict()


# create inlinks for a given URL. Its basically re-crawling.
def create_inlink():
    wiki_pattern = re.compile("^/wiki/")
    for seed_url in DICTIONARY:
        html_text = urllib2.urlopen(seed_url)
        html_content = BeautifulSoup(html_text, "html.parser")
        url_data = html_content.find('div', {"id": "bodyContent"}).findAll('a', href=wiki_pattern)
        for url in url_data:
            href = url.get('href')
            current_url = BASE_URL + href
            if ':' in href:
                continue
            if '#' in current_url:
                current_url = current_url[:current_url.index('#')]
            current_url = current_url.encode("UTF-8")
            if current_url in DICTIONARY.keys() and seed_url not in DICTIONARY[current_url] and seed_url != current_url:
                DICTIONARY[current_url].append(seed_url)


# Read the URL List file
def read_url(url):
    url_to_dic = open(url, "r")
    for line in url_to_dic:
        line1 = re.sub("[0-9]*.\t", "", line) # removing Serial Number from line
        line1 = line1.strip(" \n")
        CRAWLED_URL.append(line1)
        DICTIONARY[line1] = []


# Create the Graph file containing the Inlinks
def create_graph():
    dic_to_url = open(GRAPH_NAME, "a")
    for url, inlinks in DICTIONARY.iteritems():
        string = ""
        for inlink in inlinks:
            string += strip_url(inlink)
            string += " "

        string = string.rstrip()
        dic_to_url.write(strip_url(url) + " " + string + "\n")


# Delete Files
def delete_files():
    if os.path.exists(GRAPH_NAME):
        os.remove(GRAPH_NAME)


# Make sure that only page title exists in the graph as DOC_ID
def strip_url(url):
    url = re.sub(".*/wiki/", "", url)
    return url


# main function, used to kick start
def start():
    delete_files()
    print "Processing..."
    read_url(URL_LIST)
    print "Creating Inlinks..."
    create_inlink()
    print "Creating Graph..."
    create_graph()

start()