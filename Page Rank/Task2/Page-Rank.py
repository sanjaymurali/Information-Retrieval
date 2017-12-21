import os
import math

INLINK_DICTIONARY = dict()  # contains a list of URLs and its corresponding in-links
OUTLINK_DICTIONARY = dict()  # contains a list of URLs and corresponding links it points to (out-links)
PAGE_RANK = dict()  # contains a list of URLs and their corresponding page rank values
TOTAL_PAGE_LIST = []  # Contains all URLs that are parsed in HW1-Task1

d = 0.85  # Given, its the dampening factor
SINK_LIST = []  # set of URLs that have no out-links

# file list
INPUT_GRAPH = "graph-1.txt"
OUTPUT_PERPLEXITY = "G1-Perplexity.txt"
OUTPUT_TOP50 = "G1-Top50.txt"


# calculate the Page rank given a Graph of DOC_IDs and their in-links
# This function, first reads the graph, creates the dictionary for in-links and out-links and then starts calculating the Page-Rank
def calculate_page_rank():
    create_inlink(INPUT_GRAPH)  # create In-links from the file and store them in INLINK_DICTIONARY
    create_outlink()  # create out-links from the INLINK_DICTIONARY

    page_rank_initial()  # generate initial value of Page rank for every page
    TOTAL_LENGTH = len(TOTAL_PAGE_LIST)  # total number of URLs obtained

    iteration_count = 1  # Number of iterations that Page-Rank has been running
    counter = 0  # Used for checking for convergence
    perplexity = 0  # initial value of perplexity for the first iteration

    # if for 4 consecutive iterations the Page Rank converges, break the loop
    while counter <= 4:
        newPR = dict()  # create a new Page Rank dictionary to store temporarily calculated Page Rank values
        totalSinkPageRank = calculate_sink_page_rank()  # calculate the total Page Rank value of all Sinks

        # Calculate Page Rank for Every Page
        for page in TOTAL_PAGE_LIST:
            # Code from HW2 Task2 used here.
            newPR[page] = (float) (1-d)/(float)(TOTAL_LENGTH)  # teleportation
            newPR[page] += d*(float)(totalSinkPageRank)/(float)(TOTAL_LENGTH)  # spread remaining PR evenly
            # "INLINK_DICTIONARY[page]" is an array of urls, which point to "page"
            for out_page in INLINK_DICTIONARY[page]:
                outlink_length = len(OUTLINK_DICTIONARY[out_page])  # length of unique out-links from a given out_page
                # add share of Page Rank from in-links
                newPR[page] += d*((float)(PAGE_RANK[out_page])/(float)(outlink_length))
        # set the newly calculated page ranks to the PAGE_RANK global dictionary
        for page in TOTAL_PAGE_LIST:
            PAGE_RANK[page] = newPR[page]

        # this decides the convergence of the Page Rank
        perplexity_new = calculate_perplexity()

        # Print the Perplexity and Iteration info to a file for record
        print_perplexity(perplexity_new, iteration_count)

        # check if new value and old value have a difference of 1, if yes then add 1 to counter else reset the counter
        if abs(perplexity_new - perplexity) < 1:
            counter += 1
        else:
            counter = 0

        perplexity = perplexity_new  # The new value of the perplexity after current iteration
        iteration_count += 1


# calculate the total Page Rank for all the Sinks
def calculate_sink_page_rank():
    sink = 0
    for url in SINK_LIST:
        sink += PAGE_RANK[url]
    return sink


# Set initial Page Rank to every page in the Page list. its is (1 / total number of pages in graph)
def page_rank_initial():
    total_length = len(TOTAL_PAGE_LIST)
    for url in TOTAL_PAGE_LIST:
        PAGE_RANK[url] = (float)(1) / (float) (total_length)


# used to calculate the shannon entropy of the Page Rank distribution
def calculate_entropy():
    shannon = 0.0
    for url in TOTAL_PAGE_LIST:
        shannon += (PAGE_RANK[url])*(math.log((float) (PAGE_RANK[url]), 2))
    return -(shannon)


'''
    used to calculate perplexity which acts as test for convergence. if for 4 consecutive iterations the change of
    perplexity value is less than 1, then the we consider the PR distribution to have converged
'''
def calculate_perplexity():
    return 2 ** calculate_entropy()


# Used to populate the INLINK_DICTIONARY dictionary with DOC_IDs from the Graph
def create_inlink(input):
    try:
        document_to_inlink = open(input, "r")
        # Ex : D1 D2 D3, means D2 and D3 are in-links to page D1
        for line in document_to_inlink:
            line = line.strip("\n")
            temp = line.split(' ')
            TOTAL_PAGE_LIST.insert(0, temp[0])
            INLINK_DICTIONARY[temp[0]] = temp[1:]
    except:
        print "Please enter Correct File name"


# Used to populate the OUTLINK_DICTIONARY dictionary with DOC_IDs from the Graph
def create_outlink():
    if INLINK_DICTIONARY:
        for key,values in INLINK_DICTIONARY.iteritems():
            for value in values:
                if value not in OUTLINK_DICTIONARY.keys():
                    OUTLINK_DICTIONARY[value] = []
                if key not in OUTLINK_DICTIONARY[value]:
                    OUTLINK_DICTIONARY[value].append(key)
        check_outlink() # used to create the SINK_LIST
    else:
        print "Please run create_inlink() first"


# Used to check how many DOC_IDs dont have in-links (Sources)
def check_inlink():
    inlink_count = 0
    for key in INLINK_DICTIONARY.keys():
        if not (INLINK_DICTIONARY[key]):
            inlink_count += 1
    return inlink_count


# Used to check how many DOC_IDs dont have out-links (Sinks)
def check_outlink():
    outlink_count = 0
    for url in TOTAL_PAGE_LIST:
        if not OUTLINK_DICTIONARY.has_key(url):
            SINK_LIST.append(url)
            outlink_count += 1
    return outlink_count

'''
    Helper Functions for Printing Page Ranks to file, Printing Perplexity value to file and sorting page rank
'''


# returns the PAGE_RANK in sorted format interms of the PR value in descending order
def sort_page_rank():
    return sorted(PAGE_RANK.iteritems(), key=lambda (k, v): (v, k), reverse=-1)


# returns Top 50 Page Rank
def return_top50():
    return sort_page_rank()[:50]


def return_top10_inlink():
    temp_dict = dict()
    for key,values in INLINK_DICTIONARY.iteritems():
        temp_dict[key] = len(values)
    return sorted(temp_dict.iteritems(), key=lambda (k, v): (v, k), reverse=-1)[:10]


# print the Top 50 PR to a file
def print_top50():
    top50_file = open(OUTPUT_TOP50, "a")
    top50 = return_top50()
    for rank in top50:
        rank = str(rank)
        temp = rank.split(", ")
        temp[0] = temp[0].strip("(")
        temp[1] = temp[1].strip(")")
        top50_file.write("Rank of page " + temp[0] + " is " + temp[1] + "\n")


# print perplexity and iteration info to a file
def print_perplexity(perplexity, iteration):
    print "Perplexity: ", perplexity, " Iteration: ", iteration
    perplexity_file = open(OUTPUT_PERPLEXITY, "a")
    perplexity_file.write("Iteration: " + str(iteration) + " Perplexity: " + str(perplexity) + "\n")


# used to clean up and delete files before starting the process
def delete_files():
    if os.path.exists(OUTPUT_PERPLEXITY):
        os.remove(OUTPUT_PERPLEXITY)
    if os.path.exists(OUTPUT_TOP50):
        os.remove(OUTPUT_TOP50)


def start():
    global INPUT_GRAPH, OUTPUT_TOP50, OUTPUT_PERPLEXITY
    input_g = raw_input("Please Enter the File name for the Input Graph: \n")
    if input_g:
        INPUT_GRAPH = input_g
    input_p = raw_input("Please Enter the File name to Output Perplexity Info: \n")
    if input_p:
        OUTPUT_PERPLEXITY = input_p
    input_50 = raw_input("Please Enter the File name to Output Top 50 Page Rank Info: \n")
    if input_50:
        OUTPUT_TOP50 = input_50
    delete_files()

    calculate_page_rank()  # initialize the Page Rank function
    print_top50()  # Print Top-50 Pages to a file of your choice
    print return_top10_inlink()  # Print Top 10 Pages with highest in-link counts
    print "No in-links (Sources): ", check_inlink()  # Number of Sources
    print "No out-links (Sinks): ", check_outlink()  # Number of Sinks

start()