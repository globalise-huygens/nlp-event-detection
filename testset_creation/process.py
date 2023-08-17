'''
This code takes WebAnno output from INCEpTION and puts event annotation in a CONLL-like data format that can be used for IAA analysis and other post-processing steps.
@author StellaVerkijk
'''

import pandas as pd
import csv
from shutil import move

# define list of semantic roles
list_of_args = ['Patient', 'Agent', 'Location', 'Time', 'AgentPatient', 'Benefactive', 'Cargo', 'Source', 'Target', 'Path', 'Instrument']

def clean(path_to_export, path_out):
    """
    Reads an export from Inception (WebAnno tsv v3.3) and cleans description lines,
    empty lines and lines that represent the whole text region in tokens (#Text). Basically, all lines that consist of less than 11 rows.
    :param path_to_export: str path to inception export
    :param path_out: str path to where you want the cleaned tsv
    :return: tsv
    """

    with open(path_to_export) as tsvfile, open(path_out, "w") as t:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        temp = csv.writer(t, delimiter="\t")
        for row in tsvreader:
            if len(row) == 11:
                temp.writerow(row)
    move(t.name, path_out)


def make_base_dict(path):
    # open cleaned tsv file, already converted from webannotsv to normal tsv, blank lines taken out etcetera
    with open(path) as tsvfile:
        #gather rows of newly organized tsv in all_mentions
        all_mentions = []
        #loop over rows in cleaned file
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        for row in tsvreader:
            #if for a token there is an event annotation
            if row[8] != '_':
                #begin a new dictionary and add the mention, the ids and the event label
                eventdict = {}
                eventdict['mention'] = row[2]
                eventdict['anchor_type'] = row[9].split('[')[0]
                eventdict['mention_token_id'] = row[0]
                eventdict['mention_character_id'] = row[1]
                eventdict['eventclass'] = row[8] #.split('[')[0]
                # for all the possible semantic roles
                for arg in list_of_args:
                    # if the semantic role is not mentioned in the row add None to the dict
                    if arg not in row[6].split(';'):
                        eventdict[arg+'_offsets'] = 'None'
                    #if the role is mentioned, save the id of the first token
                    try:
                        arg_ids = []
                        for i in range(0, 20):
                            if arg in row[6].split(';')[i]:
                                arg_ids.append(row[7].split(';')[i])
                                eventdict[arg+'_offsets'] = arg_ids
                    except IndexError:
                        continue
                all_mentions.append(eventdict)

    return(all_mentions)

def store_original_dict(path):
    with open(path) as tsvfile:
        data = tsvfile.readlines()
        data_list = [i.split('\t') for i in data]

    return(data_list)

def check_spans(df, i):
    try:
    #check if the event class at i is the same as event class at i+1
        if df.at[i, 'eventclass'] == df.at[i+1, 'eventclass']:
            #check if the event class at i is not the same as the event class at i-1
            if df.at[i, 'eventclass'] != df.at[i-1, 'eventclass']:
                #check if the token_id of the second token within the instance of the event class at i is +1 the token_id of the first token within the instance of the event class
                try:
                    if int(df.at[i, 'mention_token_id'].split('-')[1])+1 == int(df.at[i+1, 'mention_token_id'].split('-')[1]):
                        for i2 in range (1,20):
                            try:
                                if df.at[i, 'eventclass'] != df.at[i+i2, 'eventclass']:
                                    return(int(i2))
                            except KeyError:
                                return(len(df)-i)
                except ValueError: #code throws value error when tokens have been partially annotated, like in "'t[Schip]". Since we will be annotating on token level instead of character level in the future these annotations are not relevant.
                    return(None)
    except KeyError:
        return(None)


def get_mention_spans(dicts, df):
    new_mentions = []
    i=-1
    for dict in dicts:
        i += 1
        #for row in df.iterrows():
        if type(check_spans(df, i)) != int:
            dict['mention_span'] = dict['mention']
            dict['mention_span_ids'] = [df.at[i, 'mention_token_id']]
        else:
            mentions = []
            ids = []
            for i2 in range (i, i+check_spans(df, i)):
                mentions.append(df.at[i2, 'mention'])
                ids.append(df.at[i2, 'mention_token_id'])
            mentionspan = (' ').join(mentions)
            dict['mention_span'] = mentionspan
            dict['mention_span_ids'] = ids
        new_mentions.append(dict)
    return(new_mentions)


def get_context(df, i, data_list):
    context = []
    i2 = 0
    for l in data_list:
        i2+=1
        if l[0] == df.at[i, 'mention_token_id'].split('.')[0]:
            if df.at[i, 'mention_span'] == 'None':
                for i3 in range(-20, -1):
                    context.append(data_list[i2+i3][2])
                context.append('[')
                context.append(df.at[i, 'mention'])
                context.append(']')
                for i4 in range(-1, 20):
                    context.append(data_list[i2+i4][2])
            else:
                len_span = len(df.at[i, 'mention_span'].split(' '))
                for i3 in range(-20, -1):
                    context.append(data_list[i2+i3][2])
                context.append('[')
                context.append(df.at[i, 'mention_span'])
                context.append(']')
                try:
                    for i4 in range(-1+len_span, 20):
                        context.append(data_list[i2+i4][2])
                except IndexError:
                    for i4 in range(-1+len_span, 10):
                        context.append(data_list[i2+i4][2])
    return(' '.join(context))



def insert_context_and_span(df, dicts, original):
    context_mentions = []
    i=-1
    for dict in dicts:
        i += 1
        dict['mention_in_context'] = get_context(df, i, original)
        context_mentions.append(dict)

    df = pd.DataFrame(context_mentions)

    for i in range(0, len(df)):
        if df.at[i, 'mention_span'] != 'None':
            len_span = len(df.at[i, 'mention_span'].split(' '))
            try:
                for i2 in range(0, len_span):
                    if df.at[i+i2, 'mention'] in df.at[i, 'mention_span'].split(' '):
                        df.at[i+i2, 'mention_span'] = df.at[i, 'mention_span']
                        df.at[i+i2, 'mention_in_context'] = df.at[i, 'mention_in_context']
                        df.at[i + i2, 'mention_span_ids'] = df.at[i, 'mention_span_ids']
            except KeyError:
                continue
    return(df)


def post_process(df, list_of_args):
    '''
    :param df: dataframe ready for post-processing
    :return: df with eventclasses without identifiers; zero values if there are no annotations for an argument; last token id's of a mention span
    '''
    # post-processing: taking off numbered labels from mention span of longer than one token
    eventclass_no_number = []
    for index, row in df.iterrows():
        eventclass_no_number.append(df.at[index, 'eventclass'].split('[')[0])

    df['eventclass_no_number'] = eventclass_no_number

    last_token_id = []
    for index, row in df.iterrows():
        if type(row['mention_span_ids']) == list:
            last_token_id.append(row['mention_span_ids'][-1])
        else:
            last_token_id.append('No Span')

    df['last_token_id'] = last_token_id
    return(df)

def main(input_path, output_path1, output_path2, output_path3):
    clean(input_path, output_path1)
    all_mentions = make_base_dict(output_path1)
    df = pd.DataFrame(all_mentions)
    original = store_original_dict(output_path1)
    with_mention_spans = get_mention_spans(all_mentions, df)
    df = pd.DataFrame(with_mention_spans)
    with_context = insert_context_and_span(df, with_mention_spans, original)
    post_processed = post_process(with_context, list_of_args)

    post_processed.to_csv(output_path2)
    post_processed.to_json(output_path3)
