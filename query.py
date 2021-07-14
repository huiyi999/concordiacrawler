import ast
import json
import math
import os
import re
import nltk

import PARAMETER

term_dict = {}
frequency = {}
MESSAGE = "No result found."

f = open(PARAMETER.result_file, 'w')


def start_single_query(query):
    '''
    starts single query
    :param query_list: the query
    '''
    global f
    print("Single query: " + str(query))
    if not query_dict:
        f.write(MESSAGE + "\n")
        print(MESSAGE)
        return
    else:
        result = {}
        for l in query_dict[query]:
            doc = l[0]
            tf = l[1]
            result[doc] = tf

    sorted_doc = sorted(result, key=lambda x: result[x], reverse=True)

    f.write("Single query: " + str(len(result)) + " documents found.\n")
    print("Single query: ", len(result), " documents found.")
    print('Num   DocID   Term Frequency')
    print("---   -----   --------------")
    num = 0
    for doc in sorted_doc:
        num += 1
        print("%-6s%-8s%-5s" % (num, doc, result[doc]))
    print("===   =====   ==============\n")


def intersect(p1, p2):
    '''
    find intersect between two postings lists
    :param p1: postings list one
    :param p2: postings list two
    '''
    docs_list = []
    pointer1 = 0
    pointer2 = 0
    while pointer1 < len(p1) and pointer2 < len(p2):
        if p1[pointer1] == p2[pointer2][0]:
            docs_list.append(p1[pointer1])
            pointer1 += 1
            pointer2 += 1
        elif p1[pointer1] > p2[pointer2][0]:
            pointer2 += 1
        else:
            pointer1 += 1
    return docs_list


def and_query(query_list):
    '''
    do and query
    :param query_list: the list of query keywords
    :return: the result of and query
    '''

    docs_list = []
    for index in query_dict[query_list[0]]:
        docs_list.append(index[0])

    not_found = []
    found = []
    found.append(query_list[0])
    for query in query_list[1:]:
        if query in query_dict:
            found.append(query)
            docs_list = intersect(docs_list, query_dict[query])
        else:
            not_found.append(query)

    global f
    print("========== Result of Multiple Keywords AND Query: ")
    f.write("========== Result of Multiple Keywords AND Query: \n")
    if len(docs_list) == 0:
        f.write("No result found for AND Query.\n")
        print("No result found for AND Query.")

    else:
        start_ranking(docs_list, query_list)



def union(p1, p2):
    '''
    find union of two postings lists
    :param p1: postings list one
    :param p2: postings list two
    '''
    global frequency

    docs_list = []
    pointer1 = 0
    pointer2 = 0
    while pointer1 < len(p1) and pointer2 < len(p2):
        if p1[pointer1] == p2[pointer2][0]:

            if p1[pointer1] in frequency:
                tmp = frequency[p1[pointer1]]
                frequency[p1[pointer1]] = tmp + 1
            else:
                frequency[p1[pointer1]] = 2

            docs_list.append(p1[pointer1])
            pointer1 += 1
            pointer2 += 1
        elif p1[pointer1] > p2[pointer2][0]:
            docs_list.append(p2[pointer2][0])
            frequency[p2[pointer2][0]] = 1
            pointer2 += 1

        else:
            docs_list.append(p1[pointer1])
            frequency[p1[pointer1]] = 1
            pointer1 += 1

    if pointer1 < len(p1):
        for p in p1[pointer1:]:
            docs_list.append(p)
            frequency[p] = 1
    elif pointer2 < len(p2):
        for p in p2[pointer2:]:
            docs_list.append(p[0])
            frequency[p[0]] = 1

    return docs_list


def or_query(query_list):
    '''
    do or query
    :param query_list: the list of query keywords
    :return: the result of or query
    '''
    global frequency,f
    frequency = {}
    docs_list = []

    print("========== Result of Multiple Keywords OR Query: ")
    f.write("\n========== Result of Multiple Keywords OR Query: \n")

    for index in query_dict[query_list[0]]:
        docs_list.append(index[0])

    for query in query_list[1:]:
        if query in query_dict:
            docs_list = union(docs_list, query_dict[query])

    start_ranking(docs_list, query_list)


def read_file():
    '''
    read the inverted index from the file
    '''
    path = PARAMETER.MERGED_BOLCK_PATH + PARAMETER.dictionary_file

    if not os.path.exists(path) or os.path.getsize(path) == 0:
        print("The dictionary file doesn't exist or it is empty.")
        os._exit(0)

    lines = open(path).readlines()
    global term_dict, N, docs_dict, dft_dict
    term_dict = {}
    dft_dict = {}

    for line in lines:
        posting_list = []
        term, posting = line.split(":", 1)
        str_list = ast.literal_eval(posting.strip())
        dft_dict[term] = str_list[0]
        for pair in str_list[1]:
            posting_list.append([int(pair[0]), int(pair[1])])
        sorted_posting_list = sorted(posting_list)
        term_dict[term] = sorted_posting_list

        # term, posting = line.split(":", 1)
        # posting_list = ast.literal_eval(posting.strip())
        # term_dict[term] = posting_list

    docs_file = PARAMETER.docID_file
    if not os.path.exists(docs_file) or os.path.getsize(docs_file) == 0:
        print("The file doesn't exist or it is empty.")
        os._exit(0)
    json_file = open(docs_file)

    docs_dict = {}
    data = json.load(json_file)
    for (key, value) in data.items():
        docs_dict[int(key)] = value
    N = len(docs_dict)
    # print("N: ", N)


def compute_score(docID, query_list):
    '''
    compute rsv_d, and tf_idf_weighting, and vsm_score for the query
    :param docID: docID
    :param query_list: the list of query keywords
    :return: rsv_d, tf_idf_weighting, vsm_score
    '''
    # print("docID: ",docID)
    l_total = 0
    for value in docs_dict.values():
        l_total += value[1]
    # print("l total: ", l_total)
    l_ave = l_total / N
    l_d = docs_dict[docID][1]

    rsv_d = 0
    tf_idf_weighting = 0
    vsm_score = 0

    tf_q_raw = {}  # raw tf in query
    tf_q_wt = {}  # weighted tf in query
    df_q = {}  # df
    idf_q = {}
    weight_tq = {}  # tf-idf weighting
    normalize_q = {}  # normalized tf-idf weighting

    tf_d_raw = {}  # raw tf in document
    tf_d_wt = {}  # weighted tf in document
    weight_td = {}
    normalize_d = {}  # normalized weighted tf in document

    for term in query_list:

        # tf raw in query
        if term in tf_q_raw.keys():
            tf_q_raw[term] += 1
        else:
            tf_q_raw[term] = 1

        # tf raw in document
        tf_d_raw[term] = 0
        tf_d_wt[term] = 0
        df_q[term] = 0
        idf_q[term] = 0
        if term not in query_dict.keys():
            print("not found in dictionary: ", term)
            continue

        postings_list = query_dict[term]
        for index in postings_list:
            if index[0] == docID:
                tf_d_raw[term] = index[1]

        # print(term, " tf_d_raw[term]: ", tf_d_raw[term])
        if tf_d_raw[term] > 0:
            tf_d_wt[term] = 1 + math.log(tf_d_raw[term], 10)
        df_q[term] = dft_dict[term]
        idf_q[term] = math.log(N / df_q[term], 10)

        rsv_d += idf_q[term] * ((PARAMETER.k1 + 1) * tf_d_raw[term]) / (
                PARAMETER.k1 * ((1 - PARAMETER.b) + PARAMETER.b * (l_d / l_ave)) + tf_d_raw[term])

        # print("tftd: ", tf_d_raw[term], " dft: ", df_q[term], " idf: ", idf_q[term])

        tf_idf_weighting += tf_d_wt[term] * idf_q[term]
        # print("tf_idf_weighting: ", tf_idf_weighting)

    total_q = 0
    for (key, value) in tf_q_raw.items():
        tf_q_wt[key] = 1 + math.log(value, 10)
        weight_tq[key] = tf_q_wt[key] * idf_q[key]
        total_q += weight_tq[key] * weight_tq[key]

    total_d = 0
    for (key, value) in tf_d_wt.items():
        weight_td[key] = tf_d_wt[key]
        total_d += weight_td[key] * weight_td[key]

    for (key, value) in tf_q_raw.items():
        normalize_q[key] = weight_tq[key] / math.sqrt(total_q)

    for (key, value) in tf_d_raw.items():
        normalize_d[key] = weight_td[key] / math.sqrt(total_d)

    for (key, value) in tf_q_raw.items():
        vsm_score += normalize_q[key] * normalize_d[key]

    # print("url: ", docs_dict[docID][0])
    # print(
    #     "==========   ==========  =========  ====  ======  ======  ===========  =========  ======  ===========  ========")
    # print(
    #     '   term       tf_q_raw    tf_q_wt    df    idf     w_tq    normalize    tf_d_raw   w_td    normalize    product ')
    # print(
    #     "==========   ==========  =========  ====  ======  ======  ===========  =========  ======  ===========  ========")
    # for term in query_list:
    #     print("%-17s%-11s%-9s%-6s%-8s%-10s%-14s%-8s%-10s%-12s%-8s" % (
    #         term, tf_q_raw[term], round(tf_q_wt[term], 2), round(df_q[term], 2), round(idf_q[term], 2),
    #         round(weight_tq[term], 2), round(normalize_q[term], 2),
    #         tf_d_raw[term], round(weight_td[term], 2), round(normalize_d[term], 2),
    #         round(normalize_q[term] * normalize_d[term], 2)))
    #     print(
    #         "==========   ==========  =========  ====  ======  ======  ===========  =========  ======  ===========  ========")
    # print()

    return rsv_d, tf_idf_weighting, vsm_score


def search_queries(query_list):
    '''
    search the result for each keywords
    :param query_list: the list of query keywords
    '''
    global query_dict
    query_dict = {}

    for query in query_list:
        for (key, value) in term_dict.items():
            if query == key:
                query_dict[query] = term_dict[key]
    # for key in query_dict.keys():
    #     print(key, ": ", len(query_dict[key]), " : ", query_dict[key])
    # print("len(query_dict): ", len(query_dict))


def start_ranking(docs_list, query_list):
    '''
    start compute bm25 and tf_idf_weighting
    :param query_list: the list of query keywords
    :param docs_list: the list of docID
    '''

    # print("start_ranking")
    global f

    print(len(docs_list), " results found.")
    f.write(str(len(docs_list)) + " results found.\n")

    rsv_d = {}
    tf_idf_weighting = {}
    vsm_score = {}

    for doc in docs_list:
        rsv_d[doc], tf_idf_weighting[doc], vsm_score[doc] = compute_score(doc, query_list)

    print("========== RSV_D ranking ==========")
    f.write("========== RSV_D ranking ==========\n")
    print_result(rsv_d)
    print("========== tf-idf weighting ranking ==========")
    f.write("\n========== tf-idf weighting ranking ==========\n")
    print_result(tf_idf_weighting)
    print("========== vsm score ranking ==========")
    f.write("\n========== vsm score ranking ==========\n")
    print_result(vsm_score)


def print_result(score_dict):
    sorted_score = sorted(score_dict.items(), key=lambda d: d[1], reverse=True)
    global f
    print("===   ===============   =================================")
    f.write("===   ===============   =================================\n")
    print('Num   Relevance Score          Url         ')
    f.write('Num   Relevance Score          Url         \n')
    print("---   ---------------   ---------------------------------")
    f.write("---   ---------------   ---------------------------------\n")
    num = 0

    for (docID, score) in sorted_score:
        num += 1
        print("%-6s%-18s%-20s" % (num, round(score, 10), docs_dict[docID][0]))
        f.write("%-6s%-18s%-20s\n" % (num, round(score, 10), docs_dict[docID][0]))
        if num == 15:
            break
    print("===   ===============   =================================\n")
    f.write("===   ===============   =================================\n")


def sort_query_list(query_list):
    sorted_query = sorted(query_dict, key=lambda i: len(query_dict[i]), reverse=True)
    # print(sorted_query)
    sorted_query_list = []
    for query in sorted_query:
        sorted_query_list.append(query)

    for query in query_list:
        if query not in sorted_query_list:
            sorted_query_list.append(query)

    return sorted_query_list


def probabilistic_search_engine(query):
    '''
    start probabilistic search engine
    :param query: query keywords
    '''

    global f

    print("query: ", query)

    tokens = query.split(" ")
    tokens = [re.sub(r'[\W\s]', '', token) for token in tokens]
    tokens_list = [token for token in tokens if token != '']
    query_list = []
    porter = nltk.PorterStemmer()
    for token in tokens_list:
        token_stemming = porter.stem(token.lower())
        query_list.append(token_stemming)

    f.write("\nquery: " + query + "\n")
    f.write("tokens: " + str(query_list) + "\n")

    # print("len(query_list): ", len(query_list))
    read_file()
    search_queries(query_list)

    # print(query_list)
    # print("len(query_dict): ", len(query_dict))

    query_list = sort_query_list(query_list)

    if query_dict:

        if len(query_list) == 1:
            start_single_query(query_list[0])

        else:
            print("\n========== AND query ==========")
            and_query(query_list)
            print("\n========== OR query ==========")
            or_query(query_list)
    else:
        print("No term found in dictionary.")
        f.write("No term found in dictionary.\n")
