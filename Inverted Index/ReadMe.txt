Text processing and corpus statistics - Assignment 3 - Information Retrieval - CS 6200
==========================================================================================

The goal of this assignment is : Implementing your own inverted indexer. Text processing and corpus statistics

INSTALLATION INSTRUCTIONS:

1. The program is written in Python 2.7, so we need to install Python 2.7 locally to be able to run it.
2. Download Python 2.7 from https://www.python.org/download/releases/2.7/
3. We need to setup the environment variables so that we can run the ".py" file with "python" command.
4. The program uses BeautifulSoup4 for downloading HTML files from the internet, we can install it by:
   pip install beautifulsoup4
------------------------------------------------------------------------------------------------------------------------

RUNNING THE PROGRAM:

1. Running the program involves traversing to the directory where the ".py" program file is located.
2. Start the Corpus generation by typing the command "python <file_name>.py" in the command line/Terminal.
3. To run the inverted-index on the corpus, place the Corpus in a folder and use the path to this folder while running
   the program in the command line/Terminal.
------------------------------------------------------------------------------------------------------------------------

Comments:

1. Task1

A. The "Downloaded HTML" folder contains the wikipedia articles downloaded as plain text and stored in a text file.
B. This folder could be created by running "web-crawler.py" from HW1-Task1

2. Task2

A. I make use of the "Corpus" generated as part of the Task1 in Task2. This could be changed by giving your own corpus
   folder location while running the program
B. To use the Corpus folder I generated, unzip the "Corpus.zip" file

3. Task3

A. The code for generating the Term Frequency Table and Document Frequency Table and the code for creating a file for
   Term Frequency Table and Document Frequency Table has been written as part of Task2. This is a design decision I chose
   so as to gain easy access to the Corpus and inverted index that has been created as part of Task2
------------------------------------------------------------------------------------------------------------------------

Files:

Task1:

1. Source code for Downloading the wikipedia articles "web-crawler.py", The Downloaded HTML would be available in a folder
   called "Downloaded HTML" in the same directory
2. Source code for creating the corpus out of the downloaded articles "corpus_generation.py"
3. The folder "Corpus" contains the output of the "corpus_generation.py" program. This is the corpus generated out of the
   downloaded wikipedia articles
4. I have compressed the "Corpus" folder as "Corpus.zip" to save space while submitting in Blackboard


Task2:

1. Source code for creating the inverted index for the corpus in "inverted-indexer.py"
2. The Corpus which is the input for the inverted indexer is present in a folder called "Corpus" generated out of a
   compressed file called "Corpus.zip"
3. Please run "inverted-indexer.py" to generate the files for Unigram, Bigram and trigram their respective term and
   document frequency
4. Inverted index for unigrams in file: "Inverted Index for Unigram.txt"
5. Inverted index for bigrams in file: "Inverted Index for Bigram.txt"
6. Inverted index for trigrams in file: "Inverted Index for Trigram.txt"


Task3:

0. Please run "inverted-indexer.py" in Task2 to generate the files for Unigram, Bigram and trigram their respective term and
   document frequency
1. For inverted index in the case of unigrams : "Term Frequency for Unigram.txt" and "Document Frequency for Unigram.txt"
   files which contain the Term frequency and Document Frequency information
2. For inverted index in the case of bigrams : "Term Frequency for Bigram.txt" and "Document Frequency for Bigram.txt"
   files which contain the Term frequency and Document Frequency information
3. For inverted index in the case of trigrams : "Term Frequency for Trigram.txt" and "Document Frequency for Trigram.txt"
   files which contain the Term frequency and Document Frequency information
4. "DOC_ID Mappings.txt" which contains the mapping between the DOC_IDs I have used in the inverted indexer and the
   article name of the wikipedia article.
5. stopwords which contains details on the stoplist


NOTE:

The files: "Term Frequency for Unigram.txt", "Document Frequency for Unigram.txt", "Term Frequency for Bigram.txt",
           "Document Frequency for Bigram.txt", "Term Frequency for Trigram.txt", "Document Frequency for Trigram.txt"
           "Inverted Index for Unigram.txt", "Inverted Index for Bigram.txt" and "Inverted Index for Trigram.txt"
are all very large in size, 30MB and above thus they cant be submitted part of the assignment. Hence to create them you
need to run the "inverted-indexer.py" program in Task2.
------------------------------------------------------------------------------------------------------------------------

Design Choices:

Task1:

In Task1, we need to create a corpus given a list of documents from wikipedia.

1. I decided to programmatically remove all useless "divs" from the document given. The approach I took was as follows:
   A. Remove the logo and the navigation around it
   B. Remove "See also" tab on bottom of the articles
   C. Remove "References" and "Notes and References" on bottom of the articles
   D. Remove the "in-article navigation"
   E. Disgard all the HTML tags

2. The generated Corpus is stored in the from of text file, where every document is named as follows:
   <Number>_<Article Title>.txt
3. This approach gives unique file names to each article

Task2:

In Task2, we need to create an inverted indexer for unigrams, bigrams and trigrams.

1. The inverted indexer stores the Document ID (Article name) where the "term" was found, instead of using the article
   name as the DOC_ID, I used the "File name" without extension as the DOC_ID.
   Ex: Instead of using "Tropical Cyclone" as a DOC_ID, I would have used "1_Tropical-Cyclone"
   Please Note that a mapping between DOC_ID and its corresponding article name has been provided in "DOC_ID Mappings.txt"

2. Task2 contains the code for Generating and Writing: Term and Document Frequency Table which is part of Task3, this is
   done inorder to gain easy access to the Corpus and inverted index that has been created as part of Task2
------------------------------------------------------------------------------------------------------------------------

CITATIONS:

1. BeautifulSoup - For downloading and crawling the webpages (https://www.crummy.com/software/BeautifulSoup/)
2. https://regex101.com/ - Regular expressions online evaluator to make it easy for checking regular expressions