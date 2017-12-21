Lucene and BM25 - Assignment 4 - Information Retrieval - CS 6200
================================================================

The goal of the assignment is Introduction to Lucene. Retrieval and scoring using BM25.

Task 1:

This task involves performing searching of the queries provided using lucene. We first have to setup lucene in our project
and then read the "QueryList.txt" file to read each query and return the results
------------------------------------------------------------------------------------------------------------------------

Task 2:

This task involves Implementing the BM25 ranking algorithm, and then read the "QueryList.txt" file to read each query
and return the results
------------------------------------------------------------------------------------------------------------------------

INSTALLATION INSTRUCTIONS:

Task 1:

1. Java needs to be installed.
2. Download Java 1.8 from http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html
3. We need to setup the environment variables so that we can run ".java" file "javac" command.
4. To set environment variables: https://docs.oracle.com/cd/E19182-01/820-7851/inst_cli_jdk_javahome_t/
5. The program uses lucene to perform search and retrieval process, to download lucene: https://archive.apache.org/dist/lucene/java/4.7.2/
6. Once	you download Lucene add the following three jars into your project’s list of referenced libraries:
   1) lucene-core-VERSION.jar
   2) lucene-queryparser-VERSION.jar
   3) lucene-analyzers-common-VERSION.jar.
   I have provided these JAR files in a folder called "JAR Files"
7. You could also import the project I'm providing into your favorite code editor like eclipse and add the external jar
   files

Task 2:

1. The program is written in Python 2.7, so we need to install Python 2.7 locally to be able to run it.
2. Download Python 2.7 from https://www.python.org/download/releases/2.7/
3. We need to setup the environment variables so that we can run the ".py" file with "python" command.
4. The program uses BeautifulSoup4 for downloading HTML files from the internet, we can install it by:
   pip install beautifulsoup4
------------------------------------------------------------------------------------------------------------------------

RUNNING THE PROGRAM:

Task 1:

1. Run the java program "HW4.java"
2. Enter the absolute paths to "Corpus" folder (I Have provided a zip file)
3. The program would then ask series of questions, follow the instructions
4. Press "q" when it asks "Enter the FULL path to add into the index" again

Task 2:

1. Running the program involves traversing to the directory where the ".py" program file is located.
2. Start the crawler by typing the command "python <file_name>.py" in the command line/Terminal.
------------------------------------------------------------------------------------------------------------------------

Files:

QueryList.txt file:

Mapping between professor's given input and my input:

1 hurricane isabel damage => hurricane isabel damage
2 forecast models => forecast models
3 green energy canada => green energy canada
4 heavy rains => heavy rains
5 hurricane music lyrics => hurricane music lyrics
6 accumulated snow => accumulated snow
7 snow accumulation => snow accumulation
8 massive blizzards blizzard => massive blizzards blizzard
9 new york city subway => new york city subway

Task 1:

The Task 1 is part of a project folder called "Lucene", You can import the project and add external jars to run the lucene
present in src/HW4.java

1. HW4.java which is the source for lucene
2. A folder called "DOC List Rank Lucene" which would be created by running the program contains the 9 tables for each
   query ranked by score
3. Files inside "DOC List Rank Lucene" are of the from "Q<Query_id>.txt", each text file containing the DOC_IDS ranked by
   score. There would be 9 files from Q1 - Q9
4. "QueryList.txt" file which contains all the queries provided by professor
5. Output is of the form :
	query_id Q0 fileName docId rank score Lucene

Task 2:

1. BM25.py which is the source code
2. "QueryList.txt" file which contains all the queries provided by professor
3. A folder containing the cleaned documents (Corpus), available in "HW3-Task2" folder. The folder called "Corpus" contains
   the corpus
4. A folder called "BM25 Scores" which would be created by running the program contains the 9 tables for each
   query ranked by score
5. Files inside "BM25 Scores" are of the from "Q<Query_id>.txt", each text file containing the DOC_IDS ranked by
   score. There would be 9 files from Q1 - Q9
6. Output is of the form :
	query_id Q0 fileName/docId rank score BM25
------------------------------------------------------------------------------------------------------------------------

CITATIONS:

1. BeautifulSoup - For downloading and crawling the webpages (https://www.crummy.com/software/BeautifulSoup/)
2. BM25 Formula - Information Retrieval in Practice (CMS) textbook
3. Lucene Documentation - https://lucene.apache.org/core/4_7_2/index.html