import ast
import os
from collections import OrderedDict

import PARAMETER
import preprocess


def spimi_invert(block_path):
    '''
    store each K-term-docIDs block
    :param block_path: the path of blocks
    '''

    remaining = len(token_id_pairs)
    block_number = 0

    list_f = {}
    for pair in token_id_pairs:
        id = pair[1]
        token = pair[0]

        if token not in list_f.keys():
            list_f[token] = [[id, 1]]
        else:
            posting_tmp = list_f[token]
            flag = False
            for l in posting_tmp:
                if id == l[0]:
                    l[1] += 1
                    flag = True
            if not flag:
                list_f[token].append([id, 1])

        count = len(list_f)
        remaining -= 1
        if count == PARAMETER.BOLCK_SIZE or remaining == 0:
            print("storing Block" + str(block_number) + " ......")

            sorted_list = OrderedDict()
            for key in sorted(list_f.keys()):
                sorted_list[key] = list_f[key]

            filename = block_path + "Block" + str(block_number) + ".txt"
            f = open(filename, "a+")
            for (token, value) in sorted_list.items():
                f.write(token + ':' + str(value) + "\n")

            block_number += 1
            list_f = {}


def merge_blocks(block_path, merged_block_path):
    '''
    merges blocks into a single index
    :param block_path: the path of blocks
    :param merged_block_path: the path of merged blocks(final inverted index)
    '''
    print("\nstart merging blocks ......")

    filename = merged_block_path + PARAMETER.dictionary_file
    f = open(filename, "a+")

    blocks_dict = OrderedDict()
    block_files = OrderedDict()

    for block in os.listdir(block_path):
        block_files[block] = open(block_path + block)

    # print("len(block_files): ", len(block_files))
    count = len(block_files)

    for (block, lines) in block_files.items():
        first_line = lines.readline()
        token, postings_list = first_line.split(":", 1)
        # print(token)
        blocks_dict[block] = [token, ast.literal_eval(postings_list)]

    term_number = 0
    while count > 0:
        min_block = min(blocks_dict, key=lambda x: blocks_dict[x][0])
        min_term = blocks_dict[min_block][0]

        min_term_posting = []
        blocks_with_min_term = []
        for (key, value) in blocks_dict.items():
            if value[0] == min_term:
                blocks_with_min_term.append(key)
                min_term_posting = min_term_posting + value[1]

        position_dict = {}
        for pair in min_term_posting:
            id = pair[0]
            tf = pair[1]
            if id not in position_dict:
                position_dict[id] = tf
            else:
                position_dict[id] += tf

        posting = list(position_dict.items())
        posting.sort(key=(lambda x: x[1]), reverse=True)
        df = len(posting)
        df_posting = [df, posting]

        f.write(min_term + ":" + str(df_posting) + "\n")
        term_number += 1

        # print(blocks_with_min_term)
        for block in blocks_with_min_term:
            next_line = block_files[block].readline()
            # print(next_line)
            if next_line:
                token, postings_list = next_line.split(":", 1)
                blocks_dict[block] = [token, ast.literal_eval(postings_list)]
            else:
                del blocks_dict[block]
                count -= 1

    print("term number: ", term_number)


def start_spimi(block_path, merged_block_path):
    '''
    start spimi
    :param block_path: the path of blocks
    :param merged_block_path: the path of merged blocks(final inverted index)
    '''
    # free memory available

    global token_id_pairs
    token_id_pairs = preprocess.token_docID

    if not os.path.exists(block_path):
        os.makedirs(block_path)

    if not os.path.exists(merged_block_path):
        os.makedirs(merged_block_path)

    spimi_invert(block_path)
    merge_blocks(block_path, merged_block_path)
