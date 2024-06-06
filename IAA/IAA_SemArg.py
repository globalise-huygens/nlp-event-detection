from process_inception_token_per_line import main
import pandas as pd
import ast
import numpy as np
import collections

#main("team_data/inception_output/NL-HaNA_1.04.02_1812_0803-0808-1.tsv",
     #"team_data/all_tokens_processed/foelie-pre.tsv", "team_data/all_tokens_processed/foelie-lines.tsv")
#main("team_data/inception_output/NL-HaNA_1.04.02_1812_0803-0808-2.tsv",
     #"team_data/all_tokens_processed/kruidnagel-pre.tsv", "team_data/all_tokens_processed/kruidnagel-lines.tsv")

main("team_data_2024/inception_output/foelie_IAA_feb_2024.tsv",
     "team_data_2024/all_tokens_processed/foelie-pre.tsv", "team_data_2024/all_tokens_processed/foelie-lines.tsv")
main("team_data_2024/inception_output/kruidnagel_IAA_feb_2024.tsv",
     "team_data_2024/all_tokens_processed/kruidnagel-pre.tsv", "team_data_2024/all_tokens_processed/kruidnagel-lines.tsv")
main("team_data_2024/inception_output/nootmuskaat_IAA_feb_2024.tsv",
     "team_data_2024/all_tokens_processed/nootmuskaat-pre.tsv", "team_data_2024/all_tokens_processed/nootmuskaat-lines.tsv")
main("team_data_2024/inception_output/kaneel_IAA_feb_2024.tsv",
     "team_data_2024/all_tokens_processed/kaneel-pre.tsv", "team_data_2024/all_tokens_processed/kaneel-lines.tsv")

list_arguments = ['Patient_offsets', 'Agent_offsets', 'Instrument_offsets', 'Location_offsets', 'Benefactive_offsets', 'Source_offsets', 'Target_offsets', 'Path_offsets']#, 'AgentPatient_offsets', 'Cargo_offsets', 'Time_offsets']

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

   # for element in original_offsets:
      #  try:
       #     convert_element(element)
       # except ValueError:
       #     print(element)
        #    print(rowname)
    new_offsets = [convert_element(element) for element in original_offsets]
    df[rowname] = new_offsets

    return(df)

def prepare_df(filepath, list_rownames):
    "creates df and filters ids from semarg offsets"
    df = pd.read_csv(filepath)
    for rowname in list_rownames:
        df = delete_ids(df, rowname)

    return(df)

#Code is not working for AgentPatient offsets in FOELIE df and Cargo offsets (not sure if both or only foelie); Time offsets are not working for Kaneel

#foelie_df = prepare_df("team_data_2024/all_tokens_processed/foelie-lines.tsv", list_arguments)
#kruid_df = prepare_df("team_data_2024/all_tokens_processed/kruidnagel-lines.tsv", list_arguments)
#nootmuskaat_df = prepare_df("team_data_2024/all_tokens_processed/nootmuskaat-lines.tsv", list_arguments)
#kaneel_df = prepare_df("team_data_2024/all_tokens_processed/kaneel-lines.tsv", list_arguments)

foelie_df = prepare_df("team_data_2024/processed/foelie-triggers-c.tsv", list_arguments)
kruid_df = prepare_df("team_data_2024/processed/kruidnagel-triggers-c.tsv", list_arguments)
nootmuskaat_df = prepare_df("team_data_2024/processed/nootmuskaat-triggers-c.tsv", list_arguments)
kaneel_df = prepare_df("team_data_2024/processed/kaneel-triggers-c.tsv", list_arguments)

foelie_df.to_csv('experimental/check_def_prep.tsv')


def count_nones(df1, df2, arg_row):
    condition1 = (df1['mention_token_id'] == df2['mention_token_id']) #for all tokens per line processed: mention_token_id should be token_id
    condition2 = (df1['eventclass_no_number'] == df2['eventclass_no_number']) & (df1['eventclass_no_number'] != '0') & (df2['eventclass_no_number'] != '0')
    condition3 = (df1[arg_row] == 'None') & (df2[arg_row] == 'None') #pd.isnull(df1[arg_row]) & pd.isnull(df2[arg_row])
    condition = condition1+condition2+condition3
    res1 = len(df1[condition])

    return(res1)


def check_offset_agreement(df1, df2, arg_row):


    # make dfs same length
    if len(df1) > len(df2):
        for i in range(len(df1)-len(df2)):
            new_row = pd.Series()
            df2 = pd.concat([df2, pd.DataFrame([new_row])], ignore_index=True)


    if len(df2) > len(df1):
        for i in range(len(df2)-len(df1)):
            new_row = pd.Series()
            df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)


    # Per line
    condition_token_id = (df1['mention_token_id'] == df2['mention_token_id'])

    #Check if 'eventclass' is not zero in both DataFrames
    #condition_event = (df1['eventclass_no_number'] != '0') & (df2['eventclass_no_number'] != '0')

    condition_event = (df1['eventclass_no_number'] == df2['eventclass_no_number']) & (df1['eventclass_no_number'] != '0') & (df2['eventclass_no_number'] != '0')


    # Check if 'agent_id' is the same in both DataFrames
    condition_semarg = (
        (df1[arg_row] == kruid_df[arg_row]) | (pd.isnull(df1[arg_row]) & pd.isnull(df2[arg_row]))
    )

    prep_condition = condition_token_id & condition_event

    # Combine conditions with logical AND
    final_condition = condition_token_id & condition_semarg & condition_event

    # Subset the original DataFrames based on the conditions
    result = df1[final_condition]

    count_offset_not_matching = len(df1[prep_condition]) - len(df1[final_condition])
    count_both_none = count_nones(df1, df2, arg_row)


    return(len(result), count_offset_not_matching, count_both_none)


#print(foelie_df['Agent_offsets'].tolist())
#print(kruid_df["Agent_offsets"].tolist())





#for arg in list_arguments:
 #   agree, disagree, none_match = check_offset_agreement(foelie_df, kruid_df, arg)
 #   print(arg, "agree: ", agree, "; disagree: ", disagree, "; agree on no arg: ", none_match)
#print()

#for arg in list_arguments:
 #   agree, disagree, none_match = check_offset_agreement(foelie_df, nootmuskaat_df, arg)
 #   print(arg, "agree: ", agree, "; disagree: ", disagree, "; agree on no arg: ", none_match)


print()
#events_f = foelie_df['eventclass_no_number'].tolist()
#events_kr = kruid_df['eventclass_no_number'].tolist()
#events_n = nootmuskaat_df['eventclass_no_number'].tolist()
#events_ka = kaneel_df['eventclass_no_number'].tolist()

#print(collections.Counter(events_f))
#print(collections.Counter(events_kr))
#print(collections.Counter(events_n))
#print(collections.Counter(events_ka))
#print()
#print("END")




def get_token_ids_per_argtype(df, arg):

    interm = []

    for item in df[arg]:
        if type(item) != float:
            for token_id in ast.literal_eval(item):
                interm.append(token_id)


    unique_arg_ids = set(interm)
    return(list(unique_arg_ids))

ids_patient_foelie = get_token_ids_per_argtype(foelie_df, 'Patient_offsets')
print(ids_patient_foelie)
ids_patient_kruid = get_token_ids_per_argtype(kruid_df, 'Patient_offsets')
print(ids_patient_kruid)

print(len(ids_patient_foelie))
print(len(ids_patient_kruid))
#print(len(ids_patient_foelie.intersection(ids_patient_kruid)))

exact_match = 0
partial_match = 0
for item in ids_patient_foelie:
    if item in ids_patient_kruid:
        exact_match+= 1
    if item.split('-')[0] + '-' + str((int(item.split('-')[1]) + 1)) in ids_patient_kruid:
        print(item.split('-')[0] + '-' + str((int(item.split('-')[1]) + 1)))
        partial_match+= 1

print(exact_match)
print(partial_match)




zipped_kr = zip(kruid_df['mention_span_ids'].tolist(), kruid_df['Patient_offsets'].tolist())
zipped_foelie = zip(foelie_df['mention_span_ids'].tolist(), foelie_df['Patient_offsets'].tolist())

zipped_mentions = zip(kruid_df['mention_span_ids'].tolist(), foelie_df['mention_span_ids'].tolist())

#compare mention span ids
#store relevant mention_span_ids (intersection of >0)
# find roles

result = []
for event1, role1 in zipped_kr:
    print('event1: ', event1)
    #print('event: ', ast.literal_eval(event), 'role: ', role)
    for event2, role2 in zipped_foelie:
        print('event2: ', event2)
        #check for span overlap in event selection
        if len(set(ast.literal_eval(event1)).intersection(set(ast.literal_eval(event2)))) > 0:
            print('overlap')
            continue
        #if len(set(ast.literal_eval(event1)).intersection(set(ast.literal_eval(event2)))) < 0:
            #print('no overlap')
            #dict['event_mention_span1'] = ast.literal_eval(event1)
            #dict['event_mention_span2'] = ast.literal_eval(event1)
            #dict['Patient_offset1'] = ast.literal_eval(role1)
            #dict['Patient_offset2'] = ast.literal_eval(role2)
        #result.append(dict)
    #print(result)

print()
print(len(kruid_df))



ex1 = ['8-230', '8-231', '8-232']
ex2 = ['8-230']
ex3 = ['8-229']

new_set = set(set(kruid_df['mention_span_ids'].tolist()).intersection(set(nootmuskaat_df['mention_span_ids'].tolist())))
print(new_set)


if len(set(ex2).intersection(set(ex1)))>0:
    print('overlap')


print()
print()


#matching_mentions = set(set(kruid_df['mention_span_ids'].tolist()).intersection(set(nootmuskaat_df['mention_span_ids'].tolist())))
#print(matching_mentions)



rel_ment1 = []
rel_ment2 = []
for ment1, ment2 in zipped_mentions:
    print(ment1)
    print(ment2)
    if len(set(ast.literal_eval(ment1)).intersection(set(ast.literal_eval(ment2)))) > 0:
        rel_ment1.append(ment1)
        rel_ment2.append(ment2)


print(len(rel_ment2))
print(len(rel_ment1))



print(rel_ment1)
print(rel_ment2)


ment_kruid = kruid_df['mention_span_ids'].tolist()
ment_foelie = foelie_df['mention_span_ids'].tolist()

overlapping_ment = []
for ment in ment_kruid:
    for ment_f in ment_foelie:
        if len(set(ast.literal_eval(ment)).intersection(set(ast.literal_eval(ment_f)))) > 0:
            overlapping_ment.append((ment, ment_f))

print()
print()
print(len(ment_kruid))
print(overlapping_ment)
print(len(overlapping_ment))
print(len(set(overlapping_ment)))


unique_overlap = list(set(overlapping_ment))
print(len(unique_overlap))

#new_df =pd.DataFrame()
#new_df['mention_span_1'] = kruid_df

only_kruid = []
only_foelie = []
patient_offsets = []
for s in unique_overlap:
    only_kruid.append(s[0])
    only_foelie.append(s[1])

print(only_kruid)

condition1 = kruid_df['mention_span_ids'].isin(only_kruid)
condition2 = foelie_df['mention_span_ids'].isin(only_foelie)

df = kruid_df[condition1]
df2 = foelie_df[condition2]

print(len(df))
print(len(df2))
print()
print()

new_df = pd.DataFrame()
new_df['mention_span1'] = only_kruid
new_df['mention_span2'] = only_foelie

print(new_df)

offsets1 = []

for index2, row2 in new_df.iterrows():
    temp = []
    for index, row in kruid_df.iterrows():
        if row['mention_span_ids'] == row2['mention_span1']:
            temp.append(row['Patient_offsets'])
    offsets1.append(temp)

print(len(offsets1))
print(offsets1)
offsets1_filtered = []
for item in offsets1:
    offsets1_filtered.append(item[0])

print(offsets1_filtered)

offsets2 = []
for index2, row2 in new_df.iterrows():
    temp = []
    for index, row in foelie_df.iterrows():
        if row['mention_span_ids'] == row2['mention_span1']:
            temp.append(row['Patient_offsets'])
    offsets2.append(temp)


offsets2_filtered = []
for item in offsets2:
    try:
        offsets2_filtered.append(item[0])
    except IndexError:
        offsets2_filtered.append(np.nan)

new_df['offsets1'] = offsets1_filtered
new_df['offsets2'] = offsets2_filtered

print()
print()

print(offsets1_filtered)


def create_window(offsets):
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
                    prefix = offset.split('-')[0]
                    suffix = offset.split('-')[1]
                    window.append(prefix + '-' + str(int(suffix) - 1))
                    window.append(offset)
                    window.append(prefix + '-' + str(int(suffix) + 1))
                    temp_window.append(window)
                list_window.append(temp_window)
        else:
            list_window.append('')
    return(list_window)

print('-----------------------------------------------')
#print(offsets1_filtered)
#print(offsets2_filtered)

window_kruid = create_window(offsets1_filtered)
window_foelie = create_window(offsets2_filtered)

new_df['window1'] = window_kruid
new_df['window2'] = window_foelie
new_df.to_csv('experimental/patients_kruid_foelie.csv')

### compare

detection_disagree = 0
detection_agree = 0
no_arg_agree = 0

# one team identified at least one arg and the other none:
for index, row in new_df.iterrows():
    if type(row['offsets1']) != type(row['offsets2']):
        detection_disagree += 1
    if type(row['offsets1']) == type(row['offsets2']) and type(row['offsets1']) != float:
        detection_agree += 1
    if type(row['offsets1']) == type(row['offsets2']) and type(row['offsets1']) == float:
        no_arg_agree += 1

perfect_match = 0
match = 0
# both one arg
for index, row in new_df.iterrows():
    if type(row['offsets1']) == type(row['offsets2']) and type(row['offsets1']) != float:
        if len(ast.literal_eval(row['offsets1'])) == 1 and len(ast.literal_eval(row['offsets2'])) == 1:
            #print(row['offsets1'], row['offsets2'])
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
for index, row in new_df.iterrows():
    if type(row['offsets1']) == type(row['offsets2']) and type(row['offsets1']) != float:
        if len(ast.literal_eval(row['offsets1'])) > 1 and len(ast.literal_eval(row['offsets2'])) > 1:
            if ast.literal_eval(row['offsets1'])[0] == ast.literal_eval(row['offsets2'])[0]:
                perfect_match += 1
                match+= 1
            if ast.literal_eval(row['offsets1'])[1] == ast.literal_eval(row['offsets2'])[1]:
                perfect_match += 1
                match+= 1
            if row['offsets1'] != row['offsets2']:
                window1 = row['window1']
                window2 = row['window2']
                if len(set(window1[0]).intersection(set(window2[0]))) > 0:
                    match += 1
                if len(set(window1[0]).intersection(set(window2[0]))) > 0:
                    match += 1


print('Scores')
print('Detection agreement (percentage of times both teams detected a Patient): ', (detection_agree / len(new_df)) * 100)
print('Agreement: both teams identified the same item as a patient: ', (match / len(new_df)) * 100)
print('Agreement: if both teams identify a patient they choose the same patient', (match / detection_agree) * 100)
print('Agreement: if both teams identify a patient they choose the same patient with the exact same token as offset', (perfect_match / detection_agree) * 100)

new_list = []
for item in window_list:
    if type(item) == list:
        for x in item:
            if type(x) == list:
                new_list.append(x)
            if type(x) == str:
                new_list.append(item)