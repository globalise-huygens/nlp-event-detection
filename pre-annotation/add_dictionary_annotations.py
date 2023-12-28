### 1. directory of csv's to json
### 2. enrich train json with lexicon json

import glob
import csv, json
import pandas as pd
import os

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

def label_with_lexicon_and_types(testdata, anno_dict):

    list_of_keys = []
    for key, value in anno_dict.items():
        list_of_keys.append(key)

    for dict in testdata:
        annotated = []
        for word in dict['words']:
            if word not in list_of_keys:
                annotated.append('O')
            elif word in list_of_keys:
                annotated.append('B-' + anno_dict[word][1])

        dict['preds'] = annotated

    return(testdata)


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


def parse_lexicon_old(csv_file, jsonfilepath):
    data = {}
    with open(csv_file) as csvfile:
            csvReader = csv.DictReader(csvfile)
            for rows in csvReader:
                print(rows)
                id = rows['token']
                data[id] = rows

    with open(jsonfilepath, 'w') as jsonfile:
        jsonfile.write(json.dumps(data))

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

#def add_lexicon(df):

df = pd.read_csv('lexicon/lexicon_v1.csv')
print(df)
tokens = df['tokens'].tolist()
labels = df['label'].tolist()
relationtypes = df['relationtype'].tolist()

zipped_ref = zip(tokens, labels, relationtypes)

zipped = zip(tokens, labels)
#for t, l in zipped:
    #if ';' in t:
        #print(t)

#d = {}
#for t, l in zipped:
   # d[t] = l

d = dict(zipped)
print(d)

#d_ref = dict(zipped_ref)

new_dict = {}
for t, l, r in zipped_ref:
    print(t, l)
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

old_dict = {}

for t, l in d.items():
    print(t, l)
    if ';' in t:
        old_dict[t.split('; ')[0]]= l
        old_dict[t.split('; ')[1]] = l
        for i in range(2, 20):
            try:
                old_dict[t.split('; ')[i]] = l
            except IndexError:
                x = 0
    else:
        old_dict[t] = l

print(len(new_dict))
print(new_dict)

to_annotate = []
for t, lr in new_dict.items():
    to_annotate.append(t)


#doc_names = os.listdir(os.path.join('data/to_annotate_2024/'))
#for doc in doc_names:
#    print(doc)
#    testdata = read_data(doc)
#    labeled = label_with_lexicon(testdata, new_dict)

#    with open("predictions/to_annotate_2024/pre_annotate-"+ doc, "w") as outfile:
#        # json.dump(labeled, outfile)
#        for sentence in labeled:
#            json.dump(sentence, outfile)
#            outfile.write("\n")

#testdata = read_data('data/dev.json')
#testdata = read_data('data/to_annotate_2024/NL-HaNA_1.04.02_11012_0229-0251.json')
#labeled = label_with_lexicon(testdata, to_annotate)
#labeled = label_with_lexicon_and_types(testdata, new_dict)

filenames = ['NL-HaNA_1-8.json','NL-HaNA_1-9.json', 'NL-HaNA_1-10.json', 'NL-HaNA_1.04.02_3598_0797-0809.json', 'NL-HaNA_1.04.02_11012_0229-0251.json']

print(new_dict)

for file in filenames:
    data = read_data('data/to_annotate_2024/'+file)
    labeled = label_with_lexicon_and_types(data, new_dict)

    with open("predictions/to_annotate_2024/type-pre_annotate-"+file, "w") as outfile:
        #json.dump(labeled, outfile)
        for sentence in labeled:
            json.dump(sentence, outfile)
            outfile.write("\n")

#print(labeled)
#p, r = evaluate(labeled, bio_or_binary='binary')
#print(p, r)

#print(labeled)


#for dict in labeled:
  #  print(dict['words'])
  #  print(dict['events'])
  #  print(dict['preds'])

#pred_to_csv(labeled, 'lexicon/lexicon_v1_types_check.csv')