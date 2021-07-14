import ast
import os
import re
from collections import OrderedDict

import PARAMETER

block_files = OrderedDict()
blocks_dict = OrderedDict()
block_path = PARAMETER.BOLCK_PATH
for block in os.listdir(block_path):
    block_files[block] = open(block_path + block)
#
# for (block, lines) in block_files.items():
#     first_line = lines.readline()
#     print(first_line)
#     token, postings_list = first_line.split(":", 1)
#     print(postings_list)
#     print(type(postings_list))
#     blocks_dict[block] = [token, ast.literal_eval(postings_list)]
#     print(blocks_dict[block])
#     print(blocks_dict[block][0])
#     print(blocks_dict[block][1])
#     print(type(blocks_dict[block]))

from scrapy.linkextractors import IGNORED_EXTENSIONS

print(IGNORED_EXTENSIONS)
tokens = re.sub(r'[\W\s]', '', "ᐅᓵᐚᐱᐦᑯᐱᓀᐦᓯ !!!")
print(tokens)
print()

from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer(language="french")
stems = stemmer.stem("ᐅᓵᐚᐱᐦᑯᐱᓀᐦᓯ")
print(stems)

from textblob import TextBlob

b = TextBlob("bonjour")
b1 = TextBlob("œuvrait")
b2 = TextBlob("ᓇᑉᐸᑕᐅᒪᔪᖅ")
print(b.detect_language())
print(b1.detect_language())
print(b2.detect_language())

tokens = ["Ein", "œuvrait", "ᓇᑉᐸᑕᐅᒪᔪᖅ", "0"]
tokens = [token for token in tokens if len(token) >= 3 if TextBlob(token).detect_language() == 'en']
print(tokens)
tokens = [re.sub(r'[\W\s]', '', token) for token in tokens]
print(tokens)
tokens = [token for token in tokens if token != '']
print("ᓇᑉᐸᑕᐅᒪᔪᖅ".isalnum())
print(tokens)

f = open("tmp1.txt", 'w')
f.truncate()

path = "tmp/"
if os.path.exists(path):
    # os.remove(path)
    os.removedirs(path)
# if not os.path.exists(path):
#     os.makedirs(path)
