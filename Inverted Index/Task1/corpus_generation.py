import os

import shutil
import urllib2

import re
from bs4 import BeautifulSoup

BASE_URL = "https://en.wikipedia.org"
WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/"
SEED_URL = "https://en.wikipedia.org/wiki/Tropical_cyclone"
DOWNLOADED_HTML_DIR = "Downloaded HTML"
GENERATED_CORPUS_DIR = "Corpus"
FILENAME_LIST = []
CASE_FOLDING = 1 # initially we do case_folding
PUNCTUATION_HANDLING = 1 # initially we handle punctuations


def generate_corpus():
    global FILENAME_LIST
    for file_name in FILENAME_LIST:
        file_content = cleanup_file(file_name)
        content = generating_file(file_content)
        write_content_to_disk(file_name, content)


def generating_file(file_content):
    soup = BeautifulSoup(file_content, "html.parser")
    soup.prettify().encode("UTF-8") # to make sure that we accommodate other languages

    # we need only the title of the page and its corresponding body
    title = soup.find('title').get_text().encode("UTF-8")
    body = "" # initially nothing is in the body
    divs = soup.findAll('div', {"id": "bodyContent"})
    for div in divs:
        body += div.get_text().encode("UTF-8")
    total_content = title + body
    return process_file(total_content)

# remove additional spaces, remove unwanted punctuations
def process_file(file_content):
    global CASE_FOLDING, PUNCTUATION_HANDLING
    '''
        This pattern removes the following:
        1. Additional Spaces (not single spaces)
        2. "()", "{}", "[]", "<>"  brackets
        3. ":" and ";" from content
        4. Mathematical equations such as "+", "*", "/", "="
        5. Currency symbols "$"
    '''
    pattern_to_remove = re.compile(r'[_!@\s#$%=+~^?&*:;(){}<>[\]\\/|"\']')
    file_content = pattern_to_remove.sub(' ',file_content)
    content_as_array = []

    if (CASE_FOLDING == 1):
        file_content = file_content.lower()
        for each_word in file_content.split():
            content_as_array.append(each_word)

    if (PUNCTUATION_HANDLING == 1):
        temp_array = []
        # we need to remove trailing and pre-fixed "," , "." and "-" from the words
        for each_word in file_content.split():
            length = len(each_word)
            # removing trailing punctuations
            if (each_word[(length - 1) : length] == "-") or (each_word[(length - 1) : length] == ",") or (each_word[(length - 1) : length] == "."):
                each_word = each_word[:(length-1)] # removing the punctuation
            # removing pre-fixed punctuations
            each_word = handle_prefixed_punctuations(each_word)
            temp_array.append(each_word)
        content_as_array = temp_array


    if (CASE_FOLDING == 0 and PUNCTUATION_HANDLING == 0):
        print "in hee"
        for each_word in file_content.split():
            content_as_array.append(each_word)

    content_as_array = [word for word in content_as_array if word != ""]
    content_as_array = " ".join(content_as_array)

    return content_as_array

# handling punctuations before a word, such as -1.0 shouldnt be removed while: ".hello" should be removed
def handle_prefixed_punctuations(word):
    # dont remove punctuations in a negative and positive, decimal or float number
    if (re.match(r'^[\-]?[0-9]*\.?[0-9]+$', word)):
        return word
    elif (word[:1] == "-") or (word[:1] == ",") or (word[:1] == "."):
        return word[1:]
    else:
        return word

# cleans up a wikipedia page. removes navigation, see also and references
def cleanup_file(file):
    file_content = read_file(file)

    # to remove the URL in the top of the file, I have stored as part of HW1-Task1
    first_line = (file_content.splitlines()[0])
    first_line_len = first_line.count('')
    file_content = file_content[first_line_len:] # remove the first line

    # type of divs to remove
    navigation = '<div id="mw-navigation">'
    toc = '<div class="toc" id="toc">'
    see_also = '<span class="mw-headline" id="See_also">'
    references = '<span class="mw-headline" id="References">'
    notes_and_references = '<span class="mw-headline" id="Notes_and_references">'

    # remove the navigation and logo present on top of the page
    if (file_content.find(navigation) != -1):
        file_content = file_content[: file_content.index(navigation)]
    if (file_content.find(toc) != -1):
        file_content = remove_toc(file_content)

    # now removing all the contents from "See also", "References" and "Notes and References"
    if (file_content.find(see_also) != -1):
        file_content = file_content[: file_content.index(see_also)]
    elif (file_content.find(references) != -1):
        file_content = file_content[: file_content.index(references)]
    elif (file_content.find(notes_and_references) != -1):
        file_content = file_content[: file_content.index(notes_and_references)]

    return file_content


# toc is a wikipedia generated navigation for the article
def remove_toc(file_content):
    starting = file_content.index('<div class="toc" id="toc">')  # starting of the tag
    ending_toctitle = file_content.find('</div>', starting)  # first of the "</div>", this closes the toctitle
    ending = file_content.find('</div>', ending_toctitle + 1)  # closes the "#toc"
    # now we need to get all the content other than the content in-between starting to ending
    begining_to_toc = file_content[:starting]
    toc_end_to_ending = file_content[ending:]
    return (begining_to_toc + toc_end_to_ending)


# Traverse the DOWNLOADED_HTML_DIR directory and get all file names, store it in a global variable.
def traverse_directory():
    global FILENAME_LIST
    file_names = os.listdir(DOWNLOADED_HTML_DIR)
    file_names = sorted(file_names, key=lambda x: int(os.path.splitext(x.split('_')[0])[0])) # to sort based on file name
    FILENAME_LIST = file_names


def get_file_as_url(filename):
    return "file://"+os.path.abspath(DOWNLOADED_HTML_DIR+"/"+filename)

# read the contents of a file
def read_file(file):
    file_content = open(DOWNLOADED_HTML_DIR + '/' + file, "r")
    return file_content.read()

# write contents on to a disk
def write_content_to_disk(filename, content):
    file_to_write = open(GENERATED_CORPUS_DIR + '/' + filename, "w")
    file_to_write.write(content)

# Deletes all files and Folders as the program starts
def delete_files():
    if os.path.exists(GENERATED_CORPUS_DIR):
        shutil.rmtree(GENERATED_CORPUS_DIR)
    os.mkdir(GENERATED_CORPUS_DIR)


# main function, used to kick start the corpus generation
def start():
    global CASE_FOLDING, PUNCTUATION_HANDLING, DOWNLOADED_HTML_DIR
    input_d = raw_input("Please Enter the Folder name where the HTML is present (skip to use default) : \n")
    if input_d:
        DOWNLOADED_HTML_DIR = input_d
    input_c = raw_input("Do you want Case-folding? (Yes: 1, No: 0) : \n")
    if input_c:
        CASE_FOLDING = int(input_c)
    input_p = raw_input("Do you want handle Punctuations? (Yes: 1, No: 0) : \n")
    if input_p:
        PUNCTUATION_HANDLING = int(input_p)

    delete_files()
    traverse_directory() # create an array of filenames and save it in a global variable "FILENAME_LIST"
    print "Generating Corpus and placing it in folder 'Corpus'"
    generate_corpus()

start()