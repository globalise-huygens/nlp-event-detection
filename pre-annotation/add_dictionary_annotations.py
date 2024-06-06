### 2. enrich train json with lexicon in csv

import csv, json
import pandas as pd


def read_data(path_to_traindata):

    with open(path_to_traindata) as f:
        data = f.readlines()

    info = []
    for line in data:
        info.append(json.loads(line))

    return(info)

def label_with_lexicon(testdata, tokens):
    """
    reads trainingdata, extracts tokens with event labels and labels test data accordingly
    :param path_to_traindata: json file
    :param path_to_testdata: json file
    :return: labeled test set with predictions and gold annotations
    """

    #print(test)
    for dict in testdata:
        annotated = []
        for word in dict['words']:
            if word not in tokens:
                annotated.append('O')
            elif word in tokens:
                annotated.append('B-event')

        dict['preds'] = annotated

    return(testdata)

def label_with_lexicon_and_types(data, anno_dict):

    list_of_keys = []
    for key, value in anno_dict.items():
        list_of_keys.append(key)

    for dict in data:
        annotated = []
        for word in dict['words']:
            if word.lower() not in list_of_keys:
                annotated.append('O')
            elif word.lower() in list_of_keys:
                annotated.append('B-' + anno_dict[word.lower()][1] + '-' + str(anno_dict[word.lower()][0]))

        dict['events'] = annotated

    return(data)


def label_with_lexicon_and_types_new(data, anno_dict):

    list_of_keys = []
    for key, value in anno_dict.items():
        list_of_keys.append(key)

    for dict in data:
        annotated = []
        for word in dict['words']:
            for key in list_of_keys:
                if word.lower() != key:
                    annotated.append('O')
                elif word.lower() == key:
                    annotated.append('B-' + anno_dict[word.lower()][1] + '-' + str(anno_dict[word.lower()][0]))

        dict['preds'] = annotated

    return(data)

def extend_annos(testdata, tokens):

    for dict in testdata:
        annotated = []
        for word in dict['words']:
            if 'event' in dict['events']:
                annotated.append(dict['events']) #NO REVISE
            if word not in tokens and 'event' not in dict['events']:
                annotated.append('O')
            if word in tokens and 'event' not in dict['events']:
                annotated.append('B-event')

        dict['preds'] = annotated

    return(testdata)


def evaluate(test, bio_or_binary = 'bio'):

    ## evaluation
    list_of_gold = []
    list_of_preds = []
    for d in test:
        list_of_gold.append(d['events'])
        list_of_preds.append(d['preds'])

    compare = zip(list_of_gold, list_of_preds)

    tp = 0
    fp = 0
    fn = 0

    for e, p in compare:
        for i in range(0, len(e)):
            if bio_or_binary == 'bio':
                if e[i] == 'B-event' and p[i] == 'B-event':
                    tp +=1
                if e[i] == 'B-event' and p[i] == 'O':
                    fn += 1
                if e[i] == 'O' and p[i] == 'B-event':
                    fp += 1
            if bio_or_binary == 'binary':
                if 'event' in e[i] and 'event' in p[i]:
                    tp +=1
                if 'event' in e[i] and 'event' not in p[i]:
                    fn+=1
                if 'event' not in e[i] and 'event' in p[i]:
                    fp+=1


    precision = tp / (tp + fp)
    recall = tp / (tp + fn)

    return(precision, recall)

def pred_to_csv(test, outfile):
    all_words = []
    all_preds = []
    all_gold = []

    for d in test:
        all_words.extend(d['words'])
        all_gold.extend(d['events'])
        all_preds.extend(d['preds'])

    df = pd.DataFrame()
    df['tokens'] = all_words
    df['preds'] = all_preds
    df['gold'] = all_gold

    df.to_csv(outfile)

# parse lexicon
df = pd.read_csv('lexicon_v2.csv')
tokens = df['tokens'].tolist()
labels = df['label'].tolist()
relationtypes = df['relationtype'].tolist()
zipped_ref = zip(tokens, labels, relationtypes)

# create dictionary of lexicon
new_dict = {}
for t, l, r in zipped_ref:
    if ';' in t:
        new_dict[t.split('; ')[0]]= [r, l]
        new_dict[t.split('; ')[1]] = [r, l]
        for i in range(2, 20):
            try:
                new_dict[t.split('; ')[i]] = [r, l]
            except IndexError:
                x = 0
    else:
        new_dict[t] = [r, l]

print(new_dict)



# list files that you want to pre-annotate

filenames_readme = ['NL-HaNA_1-8.json','NL-HaNA_1-9.json', 'NL-HaNA_1-10.json', 'NL-HaNA_1.04.02_3598_0797-0809.json', 'NL-HaNA_1.04.02_11012_0229-0251.json']

filenames_june2024 = ['NL-HaNA_1.04.02_8596_0761-0766.json']

# loop over files and create new jsonfiles with labels for any words that overlap with lexicon
for file in filenames_june2024:
    data = read_data('data/globalise-xmi-2024-05-31-ner/globalise-xmi-2024-06-03-ner-events/'+file)
    labeled = label_with_lexicon_and_types(data, new_dict)

    with open("preannotated-"+file, "w") as outfile:
        #json.dump(labeled, outfile)
        for sentence in labeled:
            json.dump(sentence, outfile)
            outfile.write("\n")

