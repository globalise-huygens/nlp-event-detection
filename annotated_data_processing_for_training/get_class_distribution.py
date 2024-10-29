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

def read_labels(paths):
    """
    Reads a jsonfile and returns the corpus as a list of list with a sentence er list
    """
    eventlabels = []
    for path in paths:
        with open(path, 'r') as file:
            data = file.read()
        list_data = []
        for item in data.split('\n'):
            list_data.append(ast.literal_eval(item))



        for d in list_data:
            for i in range(len(d['words'])):
                eventlabels.append(d['events'][i]) #add [2:] for not including I- and B-

    return(eventlabels)

root_dir = "json_per_doc_class/"
filepaths = get_filepath_list(root_dir)
print(filepaths)
labels = read_labels(filepaths)
counted = Counter(labels)

with open('labelcount-mentions.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in counted.items():
        if key.startswith("B-"):  # do not use this line if extracting token count, this is for mention count
            writer.writerow([key, value])