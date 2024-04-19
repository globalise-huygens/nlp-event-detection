import json

import pandas
import pandas as pd

punct = ['.', ';', ',', ':', '-', '_', "'"]
funct = ['in', 'op', 'onder', 'voor', 'tuschen', 'bij', 'by', 'naest', 'door', 'met', 'ende', 'ons', 'wij', 'jullie', 'hen',
         'naast', 'en', 'maar', 'ook', 'oock', 'dit', 'de', 'het', 'soo', 'te', 'den', 'haer', 'van', 'aen', 'over',
         'ten', 't', "'t", 'tot', 'is']


def read_data(path_to_traindata):

    with open(path_to_traindata) as f:
        data = f.readlines()

    info = []
    for line in data:
        info.append(json.loads(line))

    return(info)

def label_with_lexicon(path_to_traindata, path_to_testdata, filter_interpunct = 'yes', filter_functional = 'no'):
    """
    reads trainingdata, extracts tokens with event labels and labels test data accordingly
    :param path_to_traindata: json file
    :param path_to_testdata: json file
    :return: labeled test set with predictions and gold annotations
    """

    info = read_data(path_to_traindata)
    tokens_b = []
    tokens_i = []

    punct = ['.', ';', ',', ':', '-', '_', "'"]
    funct = ['in', 'op', 'voor', 'tuschen', 'bij', 'by', 'naest', 'door', 'met', 'ende', 'ons', 'wij', 'jullie', 'hen' ,'naast', 'en', 'maar', 'ook', 'oock', 'dit', 'de', 'het', 'soo', 'te', 'den', 'haer', 'van', 'aen', 'over', 'ten', 't', "'t", 'tot', 'is']
    for dict in info:
        zipped = zip(dict['words'], dict['events'])
        for w, e in zipped:
            if filter_interpunct == 'yes' and filter_functional == 'no':
                if e == 'I-event' and w not in punct:
                    tokens_i.append(w)
                if e == 'B-event' and w not in punct:
                    tokens_b.append(w)
            if filter_interpunct == 'yes' and filter_functional == 'yes':
                if e == 'I-event' and w not in punct and w not in funct:
                    tokens_i.append(w)
                if e == 'B-event' and w not in punct and w not in funct:
                    tokens_b.append(w)
            if filter_interpunct == 'no' and filter_functional == 'yes':
                if e == 'I-event' and w not in funct:
                    tokens_i.append(w)
                if e == 'B-event'  and w not in funct:
                    tokens_b.append(w)
            if filter_interpunct == 'no' and filter_functional == 'no':
                if e == 'I-event':
                    tokens_i.append(w)
                if e == 'B-event':
                    tokens_b.append(w)

    print('Amount of annotated tokens: ', len(tokens_i) + len(tokens_b))
    print('Amount of unique annotated tokens: ', len(set(tokens_i))+len(set(tokens_b)))

    #for item in set(tokens_b):
        #if item in set(tokens_i):
            #print(item)

    test = []
    with open(path_to_testdata) as f:
        data = f.readlines()
    for line in data:
        test.append(json.loads(line))

    #print(test)
    for dict in test:
        annotated = []
        for word in dict['words']:
            if word not in set(tokens_b) and word not in set(tokens_i):
                annotated.append('O')
            elif word in set(tokens_b):
                annotated.append('B-event')
            elif word in set(tokens_i):
                annotated.append('I-event')

        dict['preds'] = annotated

    return(test)


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
                if e[i] == 'I-event' and p[i] == 'I-event':
                    tp +=1
                if e[i] == 'B-event' and p[i] == 'O':
                    fn += 1
                if e[i] == 'I-event' and p[i] == 'O':
                    fn += 1
                if e[i] == 'O' and p[i] == 'B-event':
                    fp += 1
                if e[i] == 'O' and p[i] == 'I-event':
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

def get_lexicon_with_types(path_to_traindata, only_duplicates = True):

    with open(path_to_traindata) as f:
        data = f.readlines()

    info = []
    for line in data:
        info.append(json.loads(line))

    annos = []
    for dict in info:
        zipped = zip(dict['words'], dict['events'])
        for w, e in zipped:
            if e != 'O':
                annos.append({w: e.split('-')[1]})

    #print(annos)
    #print(len(annos))

    # Create a dictionary to store the count of each dictionary
    dict_count = {}

    # Iterate through the list and count occurrences of each dictionary
    for d in annos:
        dict_str = str(d)
        dict_count[dict_str] = dict_count.get(dict_str, 0) + 1

    #print(dict_count)

    list_words = []
    list_events = []
    list_counts = []
    # Print dictionaries that appear more than once
    for dict_str, count in dict_count.items():
        if only_duplicates == True:
            if count > 1:
                print(eval(dict_str), count)
                for key, value in (eval(dict_str)).items():
                    list_words.append(key)
                    list_events.append(value)
                list_counts.append(count)
        if only_duplicates == False:
            for key, value in (eval(dict_str)).items():
                list_words.append(key)
                list_events.append(value)
            list_counts.append(count)

    df = pandas.DataFrame()
    df['token'] = list_words
    df['event'] = list_events
    df['count'] = list_counts


    return(df)



#path_to_traindata = 'data/data_only_detect/train.json'
#path_to_testdata = 'data/data_only_detect/dev.json'
#test = label_with_lexicon(path_to_traindata, path_to_testdata, filter_interpunct='yes', filter_functional='yes')

#p, r = evaluate(test, bio_or_binary='binary')
#print(p, r)

#pred_to_csv(test,'predictions/lex_base_filterboth.csv')

path_tr_types = 'data/input_for_lexicon_v2/json/classification/all.json'
df_lexicon = get_lexicon_with_types(path_tr_types, only_duplicates=True)
df_lexicon.to_csv('data/from_runningdata_annoround_april2024.csv')

# only do B- labels and not filter out any function words --> should think of a solution for strings later
annos = zip(df_lexicon['token'].tolist(), df_lexicon['event'].tolist())

filtered_annos = [(x, y) for x, y in annos if x not in funct+punct]
print(filtered_annos)

#info = read_data(path_to_traindata)

tokens = []
events = []
text = []

num=0
extended_data = []
for w, e in filtered_annos:
    #print(e)
    for line in info:
        for i in range(0, len(line['words'])):
            if line['words'][i] == w:
                #print('ok')
                #print(line['words'][i])
                #print(e)
                if line['events'][i] == 'O':
                    tokens.append(w)
                    events.append(e)
                    text.append((' ').join(line['words']))
                    print(w, e)
                    num+=1
                    print((' ').join(line['words']))
                #print(line['events'][i])
                #line['events'][i] = e
                #print(line['events'][i])

print(num)

analyse_df = pd.DataFrame()
analyse_df['token'] = tokens
analyse_df['event'] = events
analyse_df['original text'] = text

#analyse_df.to_csv('lexicon/automatic_anno_extension_train_annoround3.csv')

