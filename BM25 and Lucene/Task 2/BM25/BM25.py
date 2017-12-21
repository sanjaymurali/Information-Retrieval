import os
import math
import operator
import shutil

CORPUS_DIR = "HW3-TASK2/Corpus"
QUERY_FILE = "QueryList.txt"
BM25_SCORE_DIR = "BM25 Scores"

# for creating inverted index
FILENAMES_IN_CORPUS = []
INVERTED_INDEX = dict()

# part of calculating BM25 score
LENGTH_OF_DOC = dict() # contains the length of each document in the corpus
AVERAGE_LENGTH_OF_DOC = 0 # average length of a document in the corpus "AVDL"

# read the query file, calculate BM25 score for each query and write them on to disk
def BM25():
    queries = open(QUERY_FILE, "r")
    query = queries.readline()
    query_id = 1
    while query != "":
        score = calculate_BM25(query.split())
        write_score(score, query_id)
        query_id += 1
        query = queries.readline()

# The actual BM25 formula.
def BM25_Formula(n, qf, f, dl):
    N = len(LENGTH_OF_DOC) # total number of documents
    k1 = 1.2
    k2 = 100
    b = 0.75
    R = 0.0
    r = 0.0 # since we have to calculate BM25 score for every document
    K = k1*((1-b) + b*(float(dl)/float(AVERAGE_LENGTH_OF_DOC)))
    first_part = math.log(((r + 0.5)/(R - r + 0.5))/((n - r + 0.5)/(N - n - R + r + 0.5)))
    second_part = ((k1 + 1)*f)/(K + f)
    third_part = ((k2 + 1) * qf)/(k2 + qf)
    total = first_part*second_part*third_part
    return total

# given a array of Strings, it calculates the BM25 score for the given query
def calculate_BM25(query_words):
    doc_score = dict()
    query_term_frequency = dict()
    # term frequencies for each word in the given query
    for word in query_words:
        if not query_term_frequency.has_key(word):
            query_term_frequency.update({word: 1})
        else:
            query_term_frequency[word] += 1

    # building inverted index with only terms in the query
    query_inverted_index = dict()
    for term in query_term_frequency:
        if not INVERTED_INDEX.has_key(term):
            query_inverted_index.update({term: {}})
        else:
            query_inverted_index.update({term: INVERTED_INDEX[term]})

    for term in query_inverted_index:
        n = len(INVERTED_INDEX[term]) # number of documents containing the term
        qf = query_term_frequency[term] # query frequency
        for doc_id in query_inverted_index[term]:
            f = INVERTED_INDEX[term][doc_id] # frequency of the term in the given document
            if LENGTH_OF_DOC.has_key(doc_id):
                dl = LENGTH_OF_DOC[doc_id] # length of the document, given the docid
            score = BM25_Formula(n, qf, f, dl) # the actual BM25 score for the given term
            if doc_id in doc_score:
                total_score = doc_score[doc_id] + score # query consists of several words, so total needs to be found
                doc_score.update({doc_id: total_score})
            else:
                doc_score.update({doc_id: score})

    doc_score = sorted(doc_score.items(), key=operator.itemgetter(1), reverse=True) # sort them in descending order of score
    print str(query_words) + " " + str(len(doc_score))
    doc_score = doc_score[0:100] # the assignment asks only top 100
    return doc_score

# Used in inverted index creation. Create inverted index from corpus
def process_corpus():
    global N_GRAM, INVERTED_INDEX
    retrieve_corpus()
    inverted_index = dict()
    for file_name in FILENAMES_IN_CORPUS:
        file_content = open(CORPUS_DIR + '/' + file_name, "r").read()
        inverted_index = generate_inverted_index_unigram(file_name, file_content, inverted_index)

    INVERTED_INDEX = inverted_index


# Used in inverted index creation. Generate the inverted index for unigram
def generate_inverted_index_unigram(docid, file_content, inverted_index):
    # split the document into each word separately
    global LENGTH_OF_DOC
    words = file_content.split()
    LENGTH_OF_DOC[docid] = len(words)
    for word in words:
        inverted_index = create_inverted_index(word, docid, inverted_index)
    return inverted_index


# Used in inverted index creation. create the inverted index
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


# Used in inverted index creation. Gets all the file names in the given corpus
def retrieve_corpus():
    global FILENAMES_IN_CORPUS
    if os.path.exists(CORPUS_DIR):
        file_names = os.listdir(CORPUS_DIR)
        file_names = sorted(file_names, key=lambda x: int(os.path.splitext(x.split('_')[0])[0]))  # to sort based on file name
        FILENAMES_IN_CORPUS = file_names

# to get the average document length in the corpus
def get_average_length_of_doc():
    global AVERAGE_LENGTH_OF_DOC
    sum = 0
    for lengths in LENGTH_OF_DOC.values():
        sum += lengths
    avg = float(sum)/float(len(LENGTH_OF_DOC))
    AVERAGE_LENGTH_OF_DOC = avg

# write scores to files
def write_score(score, query_id):
    score_file = open(BM25_SCORE_DIR+"/Q" + str(query_id) +".txt", "w")
    builder = ""
    rank = 1 # from top to bottom
    for docid, score in score:
        builder += str(query_id) + "\tQ0\t" + docid + "\t" + str(rank) + "\t" + str(score) + "\tBM25\n"
        rank += 1
    builder = builder[0: len(builder)-1] # delete the trailing "\n"
    score_file.write(builder)

def delete_files():
    if os.path.exists(BM25_SCORE_DIR):
        shutil.rmtree(BM25_SCORE_DIR)
    os.mkdir(BM25_SCORE_DIR)

# starter program
def start():
    global CORPUS_DIR, QUERY_FILE

    input_corpus = raw_input("Enter path to the Corpus directory generated from HW3-Task1 (Skip for Default): ")
    if input_corpus:
        CORPUS_DIR = input_corpus

    input_query = raw_input("Enter path to the query file (Skip for Default): ")
    if input_query:
        QUERY_FILE = input_query

    delete_files()
    process_corpus() # this function generates the inverted index for unigram for the given corpus
    get_average_length_of_doc() # this function helps in calculating "AVDL", average document length in the corpus
    BM25()

start()