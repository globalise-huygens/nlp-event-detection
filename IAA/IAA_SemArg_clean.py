from process_inception_token_per_line import main
import pandas as pd
import ast
import numpy as np
import itertools

#main("team_data/inception_output/NL-HaNA_1.04.02_1812_0803-0808-1.tsv",
     #"team_data/all_tokens_processed/foelie-pre.tsv", "team_data/all_tokens_processed/foelie-lines.tsv")
#main("team_data/inception_output/NL-HaNA_1.04.02_1812_0803-0808-2.tsv",
     #"team_data/all_tokens_processed/kruidnagel-pre.tsv", "team_data/all_tokens_processed/kruidnagel-lines.tsv")

#main("team_data_2024/inception_output/foelie_IAA_feb_2024.tsv",
  #   "team_data_2024/all_tokens_processed/foelie-pre.tsv", "team_data_2024/all_tokens_processed/foelie-lines.tsv")
#main("team_data_2024/inception_output/kruidnagel_IAA_feb_2024.tsv",
     #"team_data_2024/all_tokens_processed/kruidnagel-pre.tsv", "team_data_2024/all_tokens_processed/kruidnagel-lines.tsv")
#main("team_data_2024/inception_output/nootmuskaat_IAA_feb_2024.tsv",
    # "team_data_2024/all_tokens_processed/nootmuskaat-pre.tsv", "team_data_2024/all_tokens_processed/nootmuskaat-lines.tsv")
#main("team_data_2024/inception_output/kaneel_IAA_feb_2024.tsv",
    # "team_data_2024/all_tokens_processed/kaneel-pre.tsv", "team_data_2024/all_tokens_processed/kaneel-lines.tsv")

list_arguments = ['Patient_offsets', 'Agent_offsets', 'Instrument_offsets', 'Location_offsets', 'Benefactive_offsets', 'Source_offsets', 'Target_offsets', 'Path_offsets', 'AgentPatient_offsets', 'Cargo_offsets', 'Time_offsets']

def convert_element(element):
    if pd.notna(element):
        # Safely evaluate the string representation of lists using ast.literal_eval
        element_list = ast.literal_eval(element)

        # If the element is a list, apply the transformation to each item in the list
        if isinstance(element_list, list):
            element_list = [item.split('[')[0] for item in element_list]

            return str(element_list)

    return element

def delete_ids(df, rowname):
    "takes out identifiers of semarg offsets"
    original_offsets = df[rowname].tolist()

    new_offsets = [convert_element(element) for element in original_offsets]
    df[rowname] = new_offsets

    return(df)

def prepare_df(filepath, list_rownames):
    "creates df and filters ids from semarg offsets"
    df = pd.read_csv(filepath)
    for rowname in list_rownames:
        df = delete_ids(df, rowname)

    return(df)



#foelie_df = prepare_df("team_data_2024/all_tokens_processed/foelie-lines.tsv", list_arguments)
#kruid_df = prepare_df("team_data_2024/all_tokens_processed/kruidnagel-lines.tsv", list_arguments)
#nootmuskaat_df = prepare_df("team_data_2024/all_tokens_processed/nootmuskaat-lines.tsv", list_arguments)
#kaneel_df = prepare_df("team_data_2024/all_tokens_processed/kaneel-lines.tsv", list_arguments)




#nootmuskaat_df.to_csv('experimental/apr26/nootmuskaat_check_def_prep.ts


def create_window_new(offsets):

    list_window = []
    for item in offsets:
        if type(item) == str:
            item = ast.literal_eval(item)
            if len(item)== 1:
                for offset in item:
                    window = []
                    prefix = offset.split('-')[0]
                    suffix = offset.split('-')[1]
                    window.append(prefix + '-' + str(int(suffix)-1))
                    window.append(offset)
                    window.append(prefix + '-' + str(int(suffix)+1))
                    list_window.append(window)
            if len(item) > 1:
                temp_window = []
                for offset in item:
                    window = []
                    try:
                        prefix = offset.split('-')[0]
                        suffix = offset.split('-')[1]
                        window.append(prefix + '-' + str(int(suffix) - 1))
                        window.append(offset)
                        window.append(prefix + '-' + str(int(suffix) + 1))
                    except ValueError:
                        prefix = offset.split('-')[0]
                        suffix = offset.split('-')[1][:-2]
                        window.append(prefix + '-' + str(int(suffix) - 1))
                        window.append(offset)
                        window.append(prefix + '-' + str(int(suffix) + 1))
                    temp_window.append(window)
                list_window.append(temp_window)
        else:
            list_window.append('')
    return(list_window)

def get_arg_offsets(df1, df2, arg):
    """
    extracts offsets of a certain argument type for event mentions with overlapping spans between two annotator teams
    """

    ment1 = df1['mention_span_ids'].tolist()
    ment2 = df2['mention_span_ids'].tolist()

    #### dit lijkt te kloppen
    overlapping_ment = []
    for ment in ment1:
        for ment_f in ment2:
            if len(set(ast.literal_eval(ment)).intersection(set(ast.literal_eval(ment_f)))) > 0 :
                overlapping_ment.append((ment, ment_f))

    unique_overlap = list(set(overlapping_ment))

    only_kruid = []
    only_foelie = []
    for s in unique_overlap:
        only_kruid.append(s[0])
        only_foelie.append(s[1])

    new_df = pd.DataFrame()
    new_df['mention_span1'] = only_kruid
    new_df['mention_span2'] = only_foelie

    print(new_df)

    offsets1 = []
    for index2, row2 in new_df.iterrows():
        temp = []
        for index, row in df1.iterrows():
            if row['mention_span_ids'] == row2['mention_span1']:
                temp.append(row[arg+'_offsets'])
        offsets1.append(temp)

    print(len(offsets1))
    print(offsets1)
    offsets1_filtered = []
    for item in offsets1:
        try:
            offsets1_filtered.append(item[0])
        except IndexError:
            offsets1_filtered.append(np.nan)

    print(len(offsets1))
    print(len(offsets1_filtered))
    print(offsets1_filtered)

    offsets2 = []
    for index2, row2 in new_df.iterrows():
        temp = []
        for index, row in df2.iterrows():
            if row['mention_span_ids'] == row2['mention_span2']:
                temp.append(row[arg+'_offsets'])
        offsets2.append(temp)


    offsets2_filtered = []
    for item in offsets2:
        try:
            offsets2_filtered.append(item[0])
        except IndexError:
            offsets2_filtered.append(np.nan)

    print("check offsets2")
    print(offsets2)
    print(offsets2_filtered)

    zipped = zip(offsets2, offsets2_filtered)
    for item1, item2 in zipped:
        print(item1, item2)

    new_df['offsets1'] = offsets1_filtered
    new_df['offsets2'] = offsets2_filtered

    window1 = create_window_new(offsets1_filtered)
    window2 = create_window_new(offsets2_filtered)

    new_df['window1'] = window1
    new_df['window2'] = window2

    return(new_df)




print('-----------------------------------------------')


def eval(df):

    detection_disagree = 0
    detection_agree = 0 # add agreeing on not detecting
    no_arg_agree = 0

    total_arg_count = 0 # total amount of arguments annotated
    total_event_count = 0 # total amount of events for which both teams annotated at least 1 arg of certain type
    arg_count = 0 # total amount of arguments annotated for events for which both teams annotated at last 1 arg of a certain type

    extra_detection_disagree = 0
    extra_detection_agree = 0

    # one team identified at least one arg and the other none:
    for index, row in df.iterrows():
        if type(row['offsets1']) != type(row['offsets2']):
            detection_disagree += 1
            total_arg_count += 1
        if type(row['offsets1']) == type(row['offsets2']) and type(row['offsets1']) != float:
            detection_agree += 1
            total_arg_count += 2
            total_event_count += 1
        if type(row['offsets1']) == type(row['offsets2']) and type(row['offsets1']) == float:
            no_arg_agree += 1

    perfect_match = 0
    match = 0
    print('check')
    print(total_arg_count)
    print(extra_detection_agree)

    # both one arg
    for index, row in df.iterrows():
        if type(row['offsets1']) == type(row['offsets2']) and type(row['offsets1']) != float:
            if len(ast.literal_eval(row['offsets1'])) == 1 and len(ast.literal_eval(row['offsets2'])) == 1:
                #print(row['offsets1'], row['offsets2'])
                arg_count += 2
                if row['offsets1'] == row['offsets2']:
                    perfect_match += 1
                    match+= 1
                else:
                    window1 = row['window1']
                    window2 = row['window2']
                    if len(set(window1).intersection(set(window2))) > 0:
                        print(window1, window2)
                        match +=1

    # both two args
    for index, row in df.iterrows():
        if type(row['offsets1']) == type(row['offsets2']) and type(row['offsets1']) != float:
            if len(ast.literal_eval(row['offsets1'])) == 2 and len(ast.literal_eval(row['offsets2'])) == 2:
                arg_count += 4
                total_arg_count += 2
                extra_detection_agree += 1
                if ast.literal_eval(row['offsets1'])[0] == ast.literal_eval(row['offsets2'])[0]:
                    perfect_match += 1
                    match+= 1
                if ast.literal_eval(row['offsets1'])[1] == ast.literal_eval(row['offsets2'])[1]:
                    perfect_match += 1
                    match+= 1
                if ast.literal_eval(row['offsets1'])[0] == ast.literal_eval(row['offsets2'])[1]:
                    perfect_match += 1
                    match += 1
                if ast.literal_eval(row['offsets1'])[1] == ast.literal_eval(row['offsets2'])[0]:
                    perfect_match += 1
                    match += 1
                if row['offsets1'] != row['offsets2']:
                    window1 = row['window1']
                    window2 = row['window2']
                    if len(set(window1[0]).intersection(set(window2[0]))) > 0:
                        match += 1
                    elif len(set(window1[1]).intersection(set(window2[1]))) > 0:
                        match += 1
                    elif len(set(window1[0]).intersection(set(window2[1]))) > 0:
                        match += 1
                    elif len(set(window1[1]).intersection(set(window2[0]))) > 0:
                        match += 1

    # 1x one arg, 1x two args
    for index, row in df.iterrows():
        if type(row['offsets1']) == type(row['offsets2']) and type(row['offsets1']) != float:
            if len(ast.literal_eval(row['offsets1'])) == 1 and len(ast.literal_eval(row['offsets2'])) == 2:
                arg_count += 3
                total_arg_count += 1
                extra_detection_disagree += 1
                local_agree = 0
                if ast.literal_eval(row['offsets1'])[0] == ast.literal_eval(row['offsets2'])[0]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[0] == ast.literal_eval(row['offsets2'])[1]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if local_agree < 1:
                    if len(set(row['window1']).intersection(set(row['window2'][0]))) > 0:
                        match += 1
                    elif len(set(row['window1']).intersection(set(row['window2'][1]))) > 0:
                        match += 1

    #hier

    print(match, perfect_match)
    for index, row in df.iterrows():
        if type(row['offsets1']) == type(row['offsets2']) and type(row['offsets1']) != float:
            if len(ast.literal_eval(row['offsets1'])) == 2 and len(ast.literal_eval(row['offsets2'])) == 1:
                arg_count += 3
                local_agree=0
                total_arg_count += 1
                extra_detection_disagree += 1
                if ast.literal_eval(row['offsets1'])[0] == ast.literal_eval(row['offsets2'])[0]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[1] == ast.literal_eval(row['offsets2'])[0]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if local_agree < 1:
                    if len(set(row['window1'][0]).intersection(set(row['window2']))) > 0:
                        match += 1
                    elif len(set(row['window1'][1]).intersection(set(row['window2']))) > 0:
                        match += 1

    print()
    print(match, perfect_match)


    # need to evaluate: if one of two teams identifies an argument, how often do they both do it

    # more than two args
    for index, row in df.iterrows():
        if type(row['offsets1']) == type(row['offsets2']) and type(row['offsets1']) != float:
            if len(ast.literal_eval(row['offsets1'])) == 3 and len(ast.literal_eval(row['offsets2'])) == 1:
                arg_count += 4
                total_arg_count += 2
                extra_detection_disagree += 2
                local_agree = 0
                if ast.literal_eval(row['offsets1'])[0] == ast.literal_eval(row['offsets2'])[0]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[1] == ast.literal_eval(row['offsets2'])[0]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[2] == ast.literal_eval(row['offsets2'])[0]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if local_agree < 1:
                    if len(set(row['window1'][0]).intersection(set(row['window2']))) > 0:
                        match += 1
                    elif len(set(row['window1'][1]).intersection(set(row['window2']))) > 0:
                        match += 1
                    elif len(set(row['window1'][2]).intersection(set(row['window2']))) > 0:
                        #print('fourth is true', row['offsets2'])
                        match += 1

    print(match, perfect_match)

    for index, row in df.iterrows():
        if type(row['offsets1']) == type(row['offsets2']) and type(row['offsets1']) != float:
            if len(ast.literal_eval(row['offsets1'])) == 1 and len(ast.literal_eval(row['offsets2'])) == 3:
                arg_count += 4
                total_arg_count += 2
                extra_detection_disagree += 2
                local_agree = 0
                if ast.literal_eval(row['offsets1'])[0] == ast.literal_eval(row['offsets2'])[0]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[0] == ast.literal_eval(row['offsets2'])[1]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[0] == ast.literal_eval(row['offsets2'])[2]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if local_agree < 1:
                    if len(set(row['window1']).intersection(set(row['window2'][0]))) > 0:
                        match += 1
                    elif len(set(row['window1']).intersection(set(row['window2'][1]))) > 0:
                        match += 1
                    elif len(set(row['window1']).intersection(set(row['window2'][2]))) > 0:
                        match += 1

    print(match, perfect_match)

    for index, row in df.iterrows():
        if type(row['offsets1']) == type(row['offsets2']) and type(row['offsets1']) != float:
            if len(ast.literal_eval(row['offsets1'])) == 3 and len(ast.literal_eval(row['offsets2'])) == 2:
                arg_count += 5
                total_arg_count += 3
                extra_detection_disagree += 1
                extra_detection_agree += 1
                local_agree = 0
                if ast.literal_eval(row['offsets1'])[0] == ast.literal_eval(row['offsets2'])[0]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[1] == ast.literal_eval(row['offsets2'])[0]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[2] == ast.literal_eval(row['offsets2'])[0]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[0] == ast.literal_eval(row['offsets2'])[1]:
                    perfect_match += 1
                    match += 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[1] == ast.literal_eval(row['offsets2'])[1]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[2] == ast.literal_eval(row['offsets2'])[1]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if local_agree < 2:
                    if len(set(row['window1'][0]).intersection(set(row['window2'][0]))) > 0:
                        match += 1
                    elif len(set(row['window1'][1]).intersection(set(row['window2'][0]))) > 0:
                        match += 1
                    elif len(set(row['window1'][2]).intersection(set(row['window2'][0]))) > 0:
                        match += 1
                    elif len(set(row['window1'][0]).intersection(set(row['window2'][1]))) > 0:
                        match += 1
                    elif len(set(row['window1'][1]).intersection(set(row['window2'][1]))) > 0:
                        match += 1
                    elif len(set(row['window1'][2]).intersection(set(row['window2'][1]))) > 0:
                        match += 1


    print(match, perfect_match)


    for index, row in df.iterrows():
        if type(row['offsets1']) == type(row['offsets2']) and type(row['offsets1']) != float:
            if len(ast.literal_eval(row['offsets1'])) == 2 and len(ast.literal_eval(row['offsets2'])) == 3:
                arg_count += 5
                total_arg_count += 3
                extra_detection_agree += 1
                extra_detection_disagree += 1
                local_agree = 0
                if ast.literal_eval(row['offsets1'])[0] == ast.literal_eval(row['offsets2'])[0]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[0] == ast.literal_eval(row['offsets2'])[1]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[0] == ast.literal_eval(row['offsets2'])[2]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[1] == ast.literal_eval(row['offsets2'])[0]:
                    perfect_match += 1
                    match += 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[1] == ast.literal_eval(row['offsets2'])[1]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[1] == ast.literal_eval(row['offsets2'])[2]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if local_agree > 2:
                    if len(set(row['window1'][0]).intersection(set(row['window2'][0]))) > 0:
                        match += 1
                    elif len(set(row['window1'][0]).intersection(set(row['window2'][1]))) > 0:
                        match += 1
                    elif len(set(row['window1'][0]).intersection(set(row['window2'][2]))) > 0:
                        match += 1
                    elif len(set(row['window1'][1]).intersection(set(row['window2'][0]))) > 0:
                        match += 1
                    elif len(set(row['window1'][1]).intersection(set(row['window2'][1]))) > 0:
                        match += 1
                    elif len(set(row['window1'][1]).intersection(set(row['window2'][2]))) > 0:
                        match += 1

    print(match, perfect_match)


    for index, row in df.iterrows():
        if type(row['offsets1']) == type(row['offsets2']) and type(row['offsets1']) != float:
            if len(ast.literal_eval(row['offsets1'])) == 3 and len(ast.literal_eval(row['offsets2'])) == 3:
                arg_count += 6
                total_arg_count += 4
                extra_detection_agree += 2
                local_agree = 0
                if ast.literal_eval(row['offsets1'])[0] == ast.literal_eval(row['offsets2'])[0]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[1] == ast.literal_eval(row['offsets2'])[0]:
                    perfect_match += 1
                    match += 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[0] == ast.literal_eval(row['offsets2'])[1]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[0] == ast.literal_eval(row['offsets2'])[2]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[1] == ast.literal_eval(row['offsets2'])[1]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[1] == ast.literal_eval(row['offsets2'])[2]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[2] == ast.literal_eval(row['offsets2'])[0]:
                    perfect_match += 1
                    match += 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[2] == ast.literal_eval(row['offsets2'])[1]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if ast.literal_eval(row['offsets1'])[2] == ast.literal_eval(row['offsets2'])[2]:
                    perfect_match += 1
                    match+= 1
                    local_agree += 1
                if local_agree < 3:
                    if len(set(row['window1'][0]).intersection(set(row['window2'][0]))) > 0:
                        match += 1
                    elif len(set(row['window1'][0]).intersection(set(row['window2'][1]))) > 0:
                        match += 1
                    elif len(set(row['window1'][0]).intersection(set(row['window2'][2]))) > 0:
                        match += 1
                    elif len(set(row['window1'][1]).intersection(set(row['window2'][0]))) > 0:
                        match += 1
                    elif len(set(row['window1'][1]).intersection(set(row['window2'][1]))) > 0:
                        match += 1
                    elif len(set(row['window1'][1]).intersection(set(row['window2'][2]))) > 0:
                        match += 1
                    elif len(set(row['window1'][2]).intersection(set(row['window2'][0]))) > 0:
                        match += 1
                    elif len(set(row['window1'][2]).intersection(set(row['window2'][1]))) > 0:
                        match += 1
                    elif len(set(row['window1'][2]).intersection(set(row['window2'][2]))) > 0:
                        match += 1




        #return(match, perfect_match)
    print(match, perfect_match)

    print(extra_detection_agree)
    print('total amount of locations annotated: ', total_arg_count)
    print('total amount of events with a location annotated by both teams: ', total_event_count, detection_agree)
    print(detection_agree + extra_detection_agree)
    print('no arg agree: ', no_arg_agree)
    print('detection disagree: ', detection_disagree)



    print()
    print()
    print()
    print('Scores')
    #print('Detection agreement per arg mention (percentage of times both teams detected a Patient or both decided there was not any, i.e. total amount of detection+non-detection agreement/total amount of events for which a location could be annotated): ', ((detection_agree + extra_detection_agree+ no_arg_agree) / (len(new_df) + (total_arg_count-detection_agree))) * 100)
    #print('Positive detection agreement per arg mention (total amount of detection agreement / total amount of args annotated): ', ( (detection_agree + extra_detection_agree) / total_arg_count) *100) #( (len(new_df)+extra_detection_disagree) - no_arg_agree)*100))
    print('Detection agreement per event mention (percentage of times both teams detected a Patient or both decided there was not any, i.e. amount both teams decided there was a patient or both decided there was not a patient / total amount of events for which a patient could be annotated): ', ((detection_agree + no_arg_agree) / len(df)) * 100)
    print('Positive detection agreement per event mention: ', (detection_agree / (len(df) - no_arg_agree)*100))
    #print('Agreement: both teams identified the same item as a patient: ', (match / (len(new_df)+extra_arg_count-no_arg_agree)) * 100) # not correct?
    print('Agreement per arg mention: if both teams identify at least one arg they choose the same arg(s)', (match / arg_count) * 100) #divided per total of arg mention annotated --> max score = 50
    print('Agreement per arg mention: if both teams identify at least one arg they choose the same arg(s) with the exact same token as offset', (perfect_match / arg_count) * 100) # divided per total of arg mention annotated --> max score is 50
    print('Agreement per event mention: if both teams identify at least one arg they choose the same arg(s)', (match / total_event_count) * 100) #divided per total of event mention annotated
    print('Agreement per event mention: if both teams identify at least one arg they choose the same arg(s) with the exact same token as offset', (perfect_match / total_event_count) * 100) # divided per total of event mention annotated
    # should also create a score without taking into account the extra_arg_count
    # Sanity check


def collect_offset_triples(window_list):

    new_list = []
    for item in window_list:
        if type(item) == list:
            if len(item) == 3 and type(item[0]) == str:
                new_list.append(item)
            if type(item[0]) == list:
                for x in item:
                    new_list.append(x)
    return(new_list)

def eval2(df):
    windows1 = df['window1'].tolist()
    windows2 = df['window2'].tolist()

    offsets1 = set(df['offsets1'].tolist())
    offsets2 = set(df['offsets2'].tolist())

    new_list1 = collect_offset_triples(windows1)
    new_list2 = collect_offset_triples(windows2)

    #print(len(new_list1))
    #print(len(new_list2))

    new_list1.sort()
    new_list1 = list(new_list1 for new_list1, _ in itertools.groupby(new_list1))

    new_list2.sort()
    new_list2 = list(new_list2 for new_list2, _ in itertools.groupby(new_list2))

    #print(len(new_list1))
    #print(len(new_list2))


    agreement = 0
    for item1 in new_list1:
        for item2 in new_list2:
            if len(set(item1).intersection(set(item2))) > 0:
                #print(item1, item2)
                agreement += 1

    #print(agreement)
    accuracy = ((agreement / len(new_list1) ) + (agreement / len(new_list2)) ) / 2
    print(accuracy)


foelie_df = prepare_df("team_data_2024/processed/foelie-triggers-c.tsv", list_arguments)
kruid_df = prepare_df("team_data_2024/processed/kruidnagel-triggers-c.tsv", list_arguments)
noot_df = prepare_df("team_data_2024/processed/nootmuskaat-triggers-c.tsv", list_arguments)
kaneel_df = prepare_df("team_data_2024/processed/kaneel-triggers-c.tsv", list_arguments)

df_nk_location = get_arg_offsets(noot_df, kruid_df, 'Location')
df_nf_location = get_arg_offsets(noot_df, foelie_df, 'Location')
df_fk_location = get_arg_offsets(foelie_df, kruid_df, 'Location')
print()
df_nk_agent = get_arg_offsets(noot_df, kruid_df, 'Agent')
df_nf_agent = get_arg_offsets(noot_df, foelie_df, 'Agent')
df_fk_agent = get_arg_offsets(foelie_df, kruid_df, 'Agent')
print()
df_nk_patient = get_arg_offsets(noot_df, kruid_df, 'Patient')
df_nf_patient = get_arg_offsets(noot_df, foelie_df, 'Patient')
df_fk_patient = get_arg_offsets(foelie_df, kruid_df, 'Patient')
print()
df_nk_time = get_arg_offsets(noot_df, kruid_df, 'Time')
df_nf_time = get_arg_offsets(noot_df, foelie_df, 'Time')
df_fk_time = get_arg_offsets(foelie_df, kruid_df, 'Time')


df_fk_location.to_csv('experimental/foelie-kruidnagel-location-may7.csv')

#eval(df_nf_agent)

#iets klopt hier niet

print()
print()
print('new eval....')
eval2(df_nk_location)
eval2(df_nf_location)
eval2(df_fk_location)
print()
eval2(df_nk_agent)
eval2(df_nf_agent)
eval2(df_fk_agent)
print()
eval2(df_nk_patient)
eval2(df_nf_patient)
eval2(df_fk_patient)
print()
eval2(df_nk_time)
eval2(df_nf_time)
eval2(df_fk_time)
