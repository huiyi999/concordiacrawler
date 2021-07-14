import json
import os
import nltk
import re
import PARAMETER
from textblob import TextBlob

token_docID = []
documents = {}


def read_file(file):
    '''
    read json file
    :param path: the name of json file
    '''

    if not os.path.exists(file) or os.path.getsize(file) == 0:
        print("The file doesn't exist or it is empty.")
        os._exit(0)
    content = json.load(open(file))

    global N, docID_dict
    N = len(content)
    print("N: ", N)

    content_dict = {}
    docID_dict = {}
    docID = 1
    for txt in content:
        docID_dict[docID] = [txt["url"]]
        content_dict[docID] = txt["content"]
        docID += 1

    tokenize(content_dict)


def tokenize(contents):
    """
    tokenize the content
    """
    tokens_number = 0
    porter = nltk.PorterStemmer()
    global documents
    for (docID, article) in contents.items():

        tokens = nltk.word_tokenize(str(article))

        tokens = [re.sub(r'[^0-9a-zA-Z]', '', token) for token in tokens]
        tokens = [token for token in tokens if token != '']
        for token in tokens:
            token_stemming = porter.stem(token.lower())
            token_docID.append([token_stemming, docID])
        # print(tokens)
        documents[docID] = tokens
        tokens_number = tokens_number + len(tokens)
    print("Number of tokens: " + str(tokens_number))

    write_to_file()
    calculate_doc_len()


def write_to_file():
    fo = open(PARAMETER.TOKENS_PATH, "a+")
    for (key, value) in documents.items():
        fo.write(str(key) + ":" + str(value) + "\n")


def calculate_doc_len():
    global docID_dict
    for (key, value) in documents.items():
        # print(id, ": ", value)
        docID_dict[key].append(len(value))
    json.dump(docID_dict, open(PARAMETER.docID_file, "w", encoding="utf−8"), indent=3)
