"""
    Author: Sanjay Murali
    Course: CS 6200 - Information Retrieval
    Task: Web Crawler with Depth First Traversal
"""

from bs4 import BeautifulSoup
import urllib2
import re
import os
import shutil # For deleting an entire directory (multiple files at once)
import traceback
import time

BASE_URL = "https://en.wikipedia.org"
SEED_URL = "https://en.wikipedia.org/wiki/Tropical_cyclone"
DOWNLOADED_HTML_DIR = "Downloaded HTML DFS"
VISITED_PAGES = []
FILES_CREATED = []
URL_COUNTER = 0
MAX_DEPTH = 6
MAX_URL = 1000
DEPTH_REACHED = 1


# Takes URL as argument which is the seed URL and crawls.
def crawler(url, depth, visited):
    global DEPTH_REACHED

    # Depth First implementation for crawling
    if len(visited) < MAX_URL and depth <= MAX_DEPTH:
        if url not in visited:
            visited.append(url)
        # time.sleep(1)
        urls = parse_all_urls(url)
        for one_url in urls:
            if one_url not in visited:
                newdepth = depth + 1
                union(visited, crawler(one_url, newdepth, visited))
            else:
                break
    DEPTH_REACHED = depth
    return visited

def dfs_crawler(url):
    crawler(url, 1, [])

# This function makes sure that the "nextlist" array is a SET of URLs.
def union(nextlist, currentlist):
    for url in currentlist:
        if url not in nextlist:
            nextlist.insert(0,url)


# Takes URL as argument and creates/downloads the contents of the URL on to disk
def crawl_url(url):
    global URL_COUNTER
    global VISITED_PAGES

    html_file = urllib2.urlopen(url)
    soup = BeautifulSoup(html_file,"html.parser")
    # Takes care of redirection so that we dont visit the same page twice
    html_title = soup.title.string
    if html_title in VISITED_PAGES:
        return -1
    else:
        VISITED_PAGES.append(html_title)
        # to make sure that only 1000 URLs are being crawled
        URL_COUNTER += 1
        #write_html_disk(url, soup)
        record_url(url)
        return soup


# Takes a URL as arguments and returns all possible outgoing links from the HTML of that URL
def parse_all_urls(url):
    wiki_pattern = re.compile("^/wiki/")
    url_list = []
    try:
        html_content = crawl_url(url)
        if html_content != -1:
            url_data = html_content.find('div', {"id": "bodyContent"}).findAll('a', href=wiki_pattern)
            for url in url_data:
                href = url.get('href')
                current_url = BASE_URL + href
                if ':' in href:
                    continue
                if '#' in current_url:
                    current_url = current_url[:current_url.index('#')]
                url_list.append(current_url.encode("UTF-8"))
        else:
            return []
    except:
        print "Error Parsing URL!"
        print traceback.format_exc()
    return url_list


# Takes a URL and HTML page as argument, writes them on to disk into their corresponding files
def write_html_disk(url, html):
    # This is the Name of the file for the downloaded html
    html_title = html.title.string
    html_title = re.sub(' - .*', '', html_title)  # remove: "- WikiPedia" from the title
    html_title = re.sub(' ', '-', html_title)
    file_name = DOWNLOADED_HTML_DIR + "/" + str(URL_COUNTER) + "_" + html_title + ".txt"
    FILES_CREATED.append(file_name)

    html_to_disk = open(file_name, "w")
    html_to_disk.write(url.encode("UTF-8") + "\n" + html.encode("UTF-8"))
    html_to_disk.close()


# Records URL visited on to a file called "url_list.txt"
def record_url(url):
    url_to_disk = open('url_list_dfs.txt', "a")
    url_to_disk.write(str(URL_COUNTER) + ".\t" + url.encode("UTF-8") + "\n")


# Deletes all files and Folders as the program starts
def delete_files():
    if os.path.exists(DOWNLOADED_HTML_DIR):
        shutil.rmtree(DOWNLOADED_HTML_DIR)
    if os.path.exists("url_list_dfs.txt"):
        os.remove("url_list_dfs.txt")
    os.mkdir(DOWNLOADED_HTML_DIR)


# main function, used to kick start the crawler
def start():
    delete_files()
    print("The Crawler is starting with Seed URL: " + SEED_URL)
    print("Visited pages is recorded in url_list_dfs.txt")
    print("Running...")
    dfs_crawler(SEED_URL)
    print("Depth Reached: " , DEPTH_REACHED)
    print("URL Counter: ", URL_COUNTER)


start()