from process_inception_token_per_line import main
import pandas as pd
import ast
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