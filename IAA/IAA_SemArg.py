from process_inception_token_per_line import main
import pandas as pd
import ast
import collections

main("team_data/inception_output/NL-HaNA_1.04.02_1812_0803-0808-1.tsv",
     "team_data/all_tokens_processed/foelie-pre.tsv", "team_data/all_tokens_processed/foelie-lines.tsv")
main("team_data/inception_output/NL-HaNA_1.04.02_1812_0803-0808-2.tsv",
     "team_data/all_tokens_processed/kruidnagel-pre.tsv", "team_data/all_tokens_processed/kruidnagel-lines.tsv")

list_arguments = ['Patient_offsets', 'Agent_offsets', 'Instrument_offsets', 'Location_offsets', 'Time_offsets', 'Benefactive_offsets', 'Source_offsets', 'Target_offsets', 'Path_offsets']

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

#Code is not working for AgentPatient offsets in FOELIE df and Cargo offsets (not sure if both or only foelie

foelie_df = prepare_df("team_data/all_tokens_processed/foelie-lines.tsv", list_arguments)
kruid_df = prepare_df("team_data/all_tokens_processed/kruidnagel-lines.tsv", list_arguments)

def count_nones(df1, df2, arg_row):
    condition1 = (df1['token_id'] == df2['token_id'])
    condition2 = (df1['eventclass_no_number'] == df2['eventclass_no_number']) & (df1['eventclass_no_number'] != '0') & (df2['eventclass_no_number'] != '0')
    condition3 = pd.isnull(df1[arg_row]) & pd.isnull(df2[arg_row])
    condition = condition1+condition2+condition3
    res1 = len(df1[condition])

    return(res1)


def check_offset_agreement(df1, df2, arg_row):
    # Per line
    condition_token_id = (df1['token_id'] == df2['token_id'])

    #Check if 'eventclass' is not zero in both DataFrames
    #condition_event = (df1['eventclass_no_number'] != '0') & (df2['eventclass_no_number'] != '0')
    condition_event = (df1['eventclass_no_number'] == df2['eventclass_no_number']) & (df1['eventclass_no_number'] != '0') & (df2['eventclass_no_number'] != '0')


    # Check if 'agent_id' is the same in both DataFrames
    condition_semarg = (
        (df1[arg_row] == kruid_df[arg_row]) | (pd.isnull(df1[arg_row]) & pd.isnull(df2[arg_row]))
    )

    prep_condition = condition_token_id & condition_event

    # Combine conditions with logical AND
    final_condition = condition_token_id & condition_event & condition_semarg

    # Subset the original DataFrames based on the conditions
    result = df1[final_condition]

    count_offset_not_matching = len(df1[prep_condition]) - len(df1[final_condition])
    count_both_none = count_nones(df1, df2, arg_row)


    return(len(result), count_offset_not_matching, count_both_none)


#print(foelie_df['Patient_offsets'].tolist())
#print(kruid_df["Patient_offsets"].tolist())

for arg in list_arguments:
    agree, disagree, none_match = check_offset_agreement(foelie_df, kruid_df, arg)
    print(arg, "agree: ", agree, "; disagree: ", disagree)#, "; agree on no arg: ", none_match)


print()
events_f = foelie_df['eventclass_no_number'].tolist()
events_k = kruid_df['eventclass_no_number'].tolist()

print(collections.Counter(events_f))
print(collections.Counter(events_k))

print()
print("END")
