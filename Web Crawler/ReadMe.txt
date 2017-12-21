Web Crawler - Assignment 1 - Information Retrieval - CS 6200
=============================================================

The goal of this assignment is to implement our own web crawler and Performing focused crawling.

Task 1:

This task involves crawling a URL from wikipedia: https://en.wikipedia.org/wiki/Tropical_cyclone
We start from the Seed URL given to us and crawl the documents using Breadth first tree traversal technique.
We crawl the documents till we get 1000 unique URLs or we reach a maximum depth of 6 whichever occurs first.
------------------------------------------------------------------------------------------------------------------------

Task 2:

This task involves crawling a URL from wikipedia: https://en.wikipedia.org/wiki/Tropical_cyclone with a given keyword.
The keyword given to us this time is "rain". The keyword is to be matched against anchor text or text within a URL.
We crawl the documents till we get 1000 unique URLs or we reach a maximum depth of 6 whichever occurs first.
------------------------------------------------------------------------------------------------------------------------

INSTALLATION INSTRUCTIONS:

1. The program is written in Python 2.7, so we need to install Python 2.7 locally to be able to run it.
2. Download Python 2.7 from https://www.python.org/download/releases/2.7/
3. We need to setup the environment variables so that we can run the ".py" file with "python" command.
4. The program uses BeautifulSoup4 for downloading HTML files from the internet, we can install it by:
   pip install beautifulsoup4
------------------------------------------------------------------------------------------------------------------------

RUNNING THE PROGRAM:

1. Running the program involves traversing to the directory where the ".py" program file is located.
2. Start the crawler by typing the command "python <file_name>.py" in the command line/Terminal.
------------------------------------------------------------------------------------------------------------------------

RESULT OF THE CRAWLER:

1. The result of the crawler is  text file "url_list" which contains all the unique URLs that have been crawled by the
   web crawler.
2. a Folder named "Downloaded HTML" is created containing all the HTML pages as clear text in their respective file
   names. The URL for the downloaded HTML is also appended on the top of the file.
------------------------------------------------------------------------------------------------------------------------

DEPTH REACHED:

1. Task 1: Maximum Depth reached is 3
2. Task 2: Maximum Depth reached is 4
------------------------------------------------------------------------------------------------------------------------
CITATIONS:

1. BeautifulSoup - For downloading and crawling the webpages (https://www.crummy.com/software/BeautifulSoup/)
2. Python regular expression Editor for trying out the regular expression used in Task 2 (https://pythex.org/)

