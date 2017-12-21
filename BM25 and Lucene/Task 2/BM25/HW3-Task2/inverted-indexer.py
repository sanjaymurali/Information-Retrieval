import operator
import os
import re


BASE_URL = "https://en.wikipedia.org"
WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/"
SEED_URL = "https://en.wikipedia.org/wiki/Tropical_cyclone"
FILENAMES_IN_CORPUS = []
DOCID_MAPPINGS = []

DOCID_MAPPINGS_FILE = "DOC_ID Mappings.txt"
CORPUS_DIR = "Corpus"

N_GRAM = 1 # initially set to generate inverted index for unigrams


# The function which acts as kick starter for processing the corpus and create inverted-index
def process_corpus():
    global N_GRAM
    inverted_index = dict()
    for file_name in FILENAMES_IN_CORPUS:
        inverted_index = process_document(file_name, inverted_index)

    generate_term_frequency(inverted_index, N_GRAM) # Generate the Term Frequency for the inverted index
    generate_document_frequency(inverted_index, N_GRAM)
    write_inverted_index(inverted_index, N_GRAM)


# Processes single documents of the corpus by tokenizing them and inserting word by word into the inverted index
def process_document(filename, inverted_index):
    global N_GRAM

    TOKENS_IN_DOC = dict()
    file_content = retrieve_content(filename) # retrieve contents of a file

    # generate inverted index for unigram
    if (N_GRAM == 1):
        # count the number of tokens in the document
        TOKENS_IN_DOC[filename] = number_of_tokens_for_doc(file_content, 1) #Store the number of tokens in each document
        inverted_index = generate_inverted_index_unigram(filename, file_content, inverted_index)
    # generate inverted index for bigram
    elif (N_GRAM == 2):
        TOKENS_IN_DOC[filename] = number_of_tokens_for_doc(file_content, 2) #Store the number of tokens in each document
        inverted_index = generate_inverted_index_bigram(filename, file_content, inverted_index)
    # generate inverted index for trigram
    elif (N_GRAM == 3):
        TOKENS_IN_DOC[filename] = number_of_tokens_for_doc(file_content, 3) #Store the number of tokens in each document
        inverted_index = generate_inverted_index_trigram(filename, file_content, inverted_index)

    return inverted_index


# Generate Inverted index for unigram
def generate_inverted_index_unigram(docid, file_content, inverted_index):
    # split the document into each word separately
    for word in file_content.split():
        inverted_index = create_inverted_index(word, docid, inverted_index)
    return inverted_index


# Generate Inverted index for Bigram
def generate_inverted_index_bigram(docid, file_content, inverted_index):
    file_content = file_content.split() # split document into words
    # Loop through all the words
    for index in range(len(file_content) - 1):
        # since its  bigram, we need two words as a term, ex: "The Wikipedia" is a bigram
        word = file_content[index] + " " + file_content[index+1] # forming the bigram term
        inverted_index = create_inverted_index(word, docid, inverted_index)
    return inverted_index


# Generate Inverted index for Trigram
def generate_inverted_index_trigram(docid, file_content, inverted_index):
    file_content = file_content.split() # split document into words
    # Loop through all the words
    for index in range(len(file_content) - 2):
        # since its  tri-gram, we need three words as a term, ex: "The Wikipedia is" is a trigram
        word = file_content[index] + " " + file_content[index+1] + " " + file_content[index+2] # forming the trigram term
        inverted_index = create_inverted_index(word, docid, inverted_index)
    return inverted_index


# create the inverted index dictionary for the corpus
def create_inverted_index(word, docid, inverted_index):
    # if the word doesnt exists, add it to the inverted index
    if not inverted_index.has_key(word):
        inverted_index[word] = {docid: 1}  # initial (docid, tf) format
    elif inverted_index[word].has_key(docid):
        # if the word and the docid exists, plus 1 to the term freq. for that docid
        doc_dict = inverted_index[word]
        term_freq_value = doc_dict.get(docid)
        term_freq_value = term_freq_value + 1
        doc_dict[docid] = term_freq_value
    else:
        # if word exists but the docid doesnt, append the current "docid" with initially term freq. of 1 to that word
        inverted_index[word].update({docid: 1})
    return inverted_index

# Generating and Writing: Term and Document Frequency is part of Task3.

# Generate the Term Frequency Table for the Corpus
def generate_term_frequency(inverted_index, ngram):
    term_frequency_table = dict()
    # Iterate through the inverted index and find the frequency of a term
    for (key, values) in inverted_index.iteritems():
        term_frequency_table[key] = 0 # initially frequency is 0
        for (value) in values.values():
            # the values.values() returns "tf" from (docid, tf) pair
            term_frequency_table[key] += value # add it to the current frequency
    # Sort the Term Frequency dictionary based on the frequency in descending order
    term_frequency_table = sorted(term_frequency_table.items(), key = operator.itemgetter(1), reverse=True)
    print "Term Frequency is being written on to disk"
    write_term_frequency(term_frequency_table, ngram) # write the Term Frequency table onto disk


# Write the Term Frequency table onto a file
def write_term_frequency(term_frequency, ngram):
    # find the type of ngram
    type_ngram = ""
    if (ngram == 1):
        type_ngram = "Unigram"
    elif (ngram == 2):
        type_ngram = "Bigram"
    elif (ngram == 3):
        type_ngram = "Trigram"
    # determine the file name
    file_name = "Term Frequency for " + type_ngram + ".txt"
    builder = ""

    for each_term in term_frequency:
        builder += str(each_term[0]) + " " + str(each_term[1]) + "\n"

    file_to_write = open(file_name, "w")
    file_to_write.write(builder)


# Generate the Document Frequency Table for the Corpus
def generate_document_frequency(inverted_index, ngram):
    document_frequency_table = dict()
    # Iterate through the inverted index and collect all the document IDs where the term is present
    for (key, values) in inverted_index.iteritems():
        docids = []
        for docid in values.keys():
            docids.append(docid)
        document_frequency_table[key] = docids
    # Sort the document frequency lexographically based on the term in ascending order
    document_frequency_table = sorted(document_frequency_table.items(), key = operator.itemgetter(0))
    print "Document Frequency is being written on to disk"
    write_document_frequency(document_frequency_table, ngram) # write the document frequency onto disk


# Write the Document Frequency table onto a file
def write_document_frequency(document_frequency, ngram):
    # find the type of ngram
    type_ngram = ""
    if (ngram == 1):
        type_ngram = "Unigram"
    elif (ngram == 2):
        type_ngram = "Bigram"
    elif (ngram == 3):
        type_ngram = "Trigram"
    # determine the file name
    file_name = "Document Frequency for " + type_ngram + ".txt"
    builder = ""

    for each_entry in document_frequency:
        builder += str(each_entry[0]) + " " + str(each_entry[1]) + " " + str(len(each_entry[1])) +"\n"

    file_to_write = open(file_name, "w")
    file_to_write.write(builder)


# counts number of token given a document and the word n-gram
def number_of_tokens_for_doc(file_content, ngram):
    return len(file_content.split()) - (ngram-1)


# retrieves the contents of a file
def retrieve_content(filename):
    file_content = open(CORPUS_DIR + '/' + filename, "r")
    return file_content.read()


# gets all the file names in the given corpus
def retrieve_corpus():
    global FILENAMES_IN_CORPUS
    if os.path.exists(CORPUS_DIR):
        file_names = os.listdir(CORPUS_DIR)
        file_names = sorted(file_names, key=lambda x: int(os.path.splitext(x.split('_')[0])[0]))  # to sort based on file name
        FILENAMES_IN_CORPUS = file_names


# this function helps me create the mapping between DOC_IDs I have used and article name
def docid_to_article_name():
    pattern = '[0-9]*_'
    builder = ""
    for name in FILENAMES_IN_CORPUS:
        builder += (name + " => ")
        name = re.split(pattern, name)
        name[1] = name[1].strip('.txt')
        builder += (name[1] + "\n")
        DOCID_MAPPINGS.append(name[1])
    file_to_write = open(DOCID_MAPPINGS_FILE, "w")
    file_to_write.write(builder)

# write inverted index on to a disk
def write_inverted_index(inverted_index, ngram):
    # find the type of ngram
    type_ngram = ""
    if (ngram == 1):
        type_ngram = "Unigram"
    elif (ngram == 2):
        type_ngram = "Bigram"
    elif (ngram == 3):
        type_ngram = "Trigram"
    # determine the file name
    file_name = "Inverted Index for " + type_ngram + ".txt"
    builder = ""

    for (key, values) in inverted_index.iteritems():
        builder += key + " => " + str(values) + "\n"

    file_to_write = open(file_name, "w")
    file_to_write.write(builder)


# Deletes all files and Folders as the program starts
def delete_files():
    if os.path.exists(DOCID_MAPPINGS_FILE):
        os.remove(DOCID_MAPPINGS_FILE)


# main function, used to kick start the inverted index creation
def start():
    global CORPUS_DIR, N_GRAM
    delete_files()
    input_corpus = raw_input("Corpus Directory: ")
    if input_corpus:
        CORPUS_DIR = input_corpus

    input_ngram = raw_input("Please Enter a n-gram to begin: {Unigram: 1, Bigram: 2, Trigram: 3}: ")
    N_GRAM = int(input_ngram)

    if (N_GRAM == 1 or N_GRAM == 2 or N_GRAM == 3):
        retrieve_corpus()  # creates an array with file names from the corpus directory
        print "Generating..."
        process_corpus()  # creates the ngrams and writes the
        docid_to_article_name()
    else:
        print "Please enter the correct n-gram value!"


start()