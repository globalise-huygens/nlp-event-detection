import os
import ast
from collections import Counter
import csv

def get_filepath_list(root_path):
    """
    Get complete filepaths leading to all relevant training data documents in a list
    :param root_path: str
    """
    file_list = []
    for root, _, filenames in os.walk(root_path):
        for filename in filenames:
            file_list.append(os.path.join(root, filename))

    return(file_list)

def read_tokens(paths):
    """
    Reads a jsonfile and returns the corpus as a list of list with a sentence per list
    """
    tokens = []
    for path in paths:
        print(path)
        with open(path, 'r') as file:
            data = file.read()
        list_data = []
        for item in data.split('\n'):
            list_data.append(ast.literal_eval(item))

        for d in list_data:
            for i in range(len(d['words'])):
                tokens.append(d['words'][i]) #add [2:] for not including I- and B-

    return(tokens)

paths = get_filepath_list('../json_per_doc')
all_tokens = read_tokens(paths)

counted = Counter(all_tokens)
print(len(counted))
print(counted)



type_token_ratio = len(counted) / len(all_tokens)

print()
print(type_token_ratio)