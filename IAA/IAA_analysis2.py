'''
This code prints an IAA report and writes unresolved disagreements to tsv files.
IAA is calculated taking coverage agreement into account and resolving non-problematic disagreements
For more information on how scores were calculated, see the Event annotation IAA August 2023 report for GLOBALISE
@author StellaVerkijk
'''

import pandas as pd
from process_inception_output import main
import sys, os
from collections import defaultdict
import ast

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def post_clean(jsonfile, print_param):

    if print_param == 'no_print':
        blockPrint()

    df = pd.read_json(jsonfile)
    mention_ids = []
    for index, row in df.iterrows():
        if type(df.at[index, 'mention_span_ids']) != list:
            mention_ids.append([df.at[index, 'mention_token_id']])
        else:
            mention_ids.append(df.at[index, 'mention_span_ids'])
    df['mention_ids'] = mention_ids

    #gather indices of double rows
    indices = []
    for i in range(0, len(df)-1):
        if df.at[i, 'mention_span'] == df.at[i+1, 'mention_span']:
            indices.append(i+1)
    #drop those rows
    new_df = df.drop(indices)

    cleaned_df = new_df[['mention_span', 'eventclass_no_number', 'anchor_type', 'mention_in_context', 'mention_span_ids', 'mention_token_id', 'mention_ids']]
    return(cleaned_df)


main("data2/NL-HaNA_1.04.02_1812_0803-0808-1.tsv", "data2/foelie.tsv", "data2/foelie-triggers-c.tsv", "data2/foelie-triggers-conll.json")
main("data2/NL-HaNA_1.04.02_1812_0803-0808-2.tsv", "data2/kruidnagel.tsv", "data2/kruidnagel-triggers-c.tsv", "data2/kruidnagel-triggers-conll.json")
main("data2/NL-HaNA_1.04.02_1812_0803-0808-3.tsv", "data2/nootmuskaat.tsv", "data2/nootmuskaat-triggers-c.tsv", "data2/nootmuskaat-triggers-conll.json")


df_foelie = post_clean("data2/foelie-triggers-conll.json", 'print')
df_kruidnagel = post_clean("data2/kruidnagel-triggers-conll.json", 'print')
df_nootmuskaat = post_clean("data2/nootmuskaat-triggers-conll.json", 'print')


print('Total amount of annotations Foelie: ', len(df_foelie))
print('Total amount of annotations Kruidnagel:', len(df_kruidnagel))
print('Total amount of annotations Nootmuskaat:', len(df_nootmuskaat))


#EXACT MATCHES ALL ANNOTATORS

def make_dict(df):
    l = []
    for index, row in df.iterrows():
        l.append({'mention_token_id': row['mention_token_id']})
    return(l)

def general_statistics(df1, df2):
    foelie = make_dict(df_foelie)
    kruidnagel = make_dict(df_kruidnagel)
    nootmuskaat = make_dict(df_nootmuskaat)


    print('Total amount of annotations Foelie: ', len(df_foelie))
    print('Total amount of annotations Kruidnagel:', len(df_kruidnagel))
    print('Total amount of annotations Nootmsuskaat:', len(df_nootmuskaat))

    all_annos = [x for x in foelie + kruidnagel + nootmuskaat]
    agreements = [x for x in foelie + kruidnagel + nootmuskaat if x in foelie and x in kruidnagel and x in nootmuskaat]

    print('Number of total annotations: ', len(all_annos))

    print('Number of first token ids of an event mention span that received a label from all annotators (mention detection): ', len(agreements))
    #print(agreements)

    print('Percentage of mention detection agreement: ', (len(agreements)/len(all_annos))*100)

    print()
    print('Average amount of annotations is: ' , ((len(foelie)+len(kruidnagel)+len(nootmuskaat))/3))
    #print('Average amount of annotations per scan is: ' , ((len(Brecht)+len(Lodewijk)+len(Manjusha)+len(Kay))/4) / 5)


def merge_dfs(df1, df2):

    indces = []
    for index, row in df2.iterrows():
        if row['Should this mention be annotated as an event?'] != 'yes':
            indces.append(index)


    df2 = df2.drop(indces)

    mention_ids = df1['mention_ids'].tolist() + df2['mention_ids'].tolist()
    eventclass = df1['eventclass_no_number'].tolist() + df2['If so, which event class should the mention be annotated with?'].tolist()
    mention_in_context = df1['mention_in_context'].tolist() + df2['mention_in_context'].tolist()
    mention_token_id = df1['mention_token_id'].tolist() + df2['mention_token_id'].tolist()
    mention_span = df1['mention_span'].tolist() + df2['mention_span'].tolist()

    result_df = pd.DataFrame()
    result_df['mention_span'] = mention_span
    result_df['mention_ids'] = mention_ids
    result_df['eventclass_no_number'] = eventclass
    result_df['mention_in_context'] = mention_in_context
    result_df['mention_token_id'] = mention_token_id


    return(result_df)

def append_checked_annotations(df_original, df_check):


    try:
    #make sure mention_ids are list types
        mention_ids_l = []
        for item in df_check['mention_ids']:
            l2= []
            l = item.split(',')
            for item in l:
                l2.append(item.strip("['").strip("']").strip(" ").strip('"').strip("'"))
            mention_ids_l.append(l2)

        df_check['mention_ids'] = mention_ids_l

    except AttributeError:
        x = 0

    complete = merge_dfs(df_original, df_check)

    return(complete)

def append_checked_annotations2(df_original, df_check1, df_check2, df_check3):


    try:
    #make sure mention_ids are list types
        mention_ids_l = []
        for item in df_check1['mention_ids']:
            l2= []
            l = item.split(',')
            for item in l:
                l2.append(item.strip("['").strip("']").strip(" ").strip('"').strip("'"))
            mention_ids_l.append(l2)

        df_check1['mention_ids'] = mention_ids_l

        mention_ids_l = []
        for item in df_check2['mention_ids']:
            l2= []
            l = item.split(',')
            for item in l:
                l2.append(item.strip("['").strip("']").strip(" ").strip('"').strip("'"))
            mention_ids_l.append(l2)

        df_check2['mention_ids'] = mention_ids_l

        mention_ids_l = []
        for item in df_check3['mention_ids']:
            l2= []
            l = item.split(',')
            for item in l:
                l2.append(item.strip("['").strip("']").strip(" ").strip('"').strip("'"))
            mention_ids_l.append(l2)

        df_check3['mention_ids'] = mention_ids_l
    except AttributeError:
        x = 0

    merge1 = merge_dfs(df_original, df_check1)
    merge2 = merge_dfs(merge1, df_check2)
    complete = merge_dfs(merge2, df_check3)

    return(complete)

def analyse_annotator_pair(df1, df2, annotator1, annotator2):


    print('ANALYSIS ANNOTATOR PAIR ' +annotator1+" & "+annotator2+ " before secondary check-annotation task")

    misc = []
    for index, row in df1.iterrows():
        if row['eventclass_no_number'] == 'Miscellaneous':
            misc.append(index)

    df1 = df1.drop(misc)

    misc = []
    for index, row in df2.iterrows():
        if row['eventclass_no_number'] == 'Miscellaneous':
            misc.append(index)

    df2 = df2.drop(misc)


    #EXACT MATCHES
    examples_exact=[]
    for index_1, row_1 in df1.iterrows():
        for index_2, row_2 in df2.iterrows():
            if row_1['mention_ids'] == row_2['mention_ids'] and row_1['eventclass_no_number'] == row_2['eventclass_no_number']: #if row_l['mention_span'] == row_2['mention_span'] and
                    examples_exact.append(row_2['mention_in_context'])

    print()
    print("# exact span matches with the same label: ", len(examples_exact))

    #for item in examples:
    #    print(item)

    #EXACT SPAN MATCHES DIFFERENT LABEL
    examples_exact_different=[]
    for index_1, row_1 in df1.iterrows():
        for index_2, row_2 in df2.iterrows():
            if row_1['mention_ids'] == row_2['mention_ids'] and row_1['eventclass_no_number'] != row_2['eventclass_no_number']: #if row_l['mention_span'] == row_2['mention_span'] and
                    examples_exact_different.append(((row_1['mention_in_context'], row_1['eventclass_no_number']), (row_2['mention_in_context'], row_2['eventclass_no_number'])))

    print("# exact span matches with a different label: ", len(examples_exact_different))

    #for item in examples_exact_different[:5]:
    #    print(item)

    #PARTIAL SPAN MATCHES

    examples_partial=[]
    for index_1, row_1 in df1.iterrows():
        for index_2, row_2 in df2.iterrows():
            if len(set(row_1['mention_ids']).intersection(set(row_2['mention_ids'])))>0 and row_1['eventclass_no_number'] == row_2['eventclass_no_number']:
                examples_partial.append(((row_1['mention_in_context'], row_1['eventclass_no_number']), (row_2['mention_in_context'], row_2['eventclass_no_number'])))

    print("# partial span matches with the same label: ", len(examples_partial))

    #for item in examples_partial[:5]:
    #    print(item)


    ### PARTIAL SPAN MATCHES DIFFERENT LABEL seeing which spans are annotated with a different label

    examples_partial_different = []
    #pre_output_disagreement = []

    for index_1, row_1 in df1.iterrows():
        for index_2, row_2 in df2.iterrows():
            if len(set(row_1['mention_ids']).intersection(set(row_2['mention_ids'])))>0 and row_1['eventclass_no_number'] != row_2['eventclass_no_number']:
                examples_partial_different.append(((row_1['mention_in_context'], row_1['eventclass_no_number'], row_1['mention_ids']), (row_2['mention_in_context'], row_2['eventclass_no_number'], row_2['mention_ids'])))
                #pre_output_disagreement.append(((row_1['mention_in_context'], row_1['eventclass_no_number'], row_1['mention_ids']), (row_2['mention_in_context'], row_2['eventclass_no_number'], row_2['mention_ids'])))

    print("# partial span matches different label: ", len(examples_partial_different))

    translocation_events = ['TransLocation', 'Transportation', 'Leaving', 'Arriving', 'Voyage', 'Translocation']
    possession_events = ['Buying', 'Selling', 'Getting', 'Giving', 'LosingPossession', 'FinancialTransaction', 'Trade',
                         'ChangeOfPossession']
    violentcontest_events = ['ViolentContest', 'Attacking', 'Besieging', 'Invasion', 'Killing']
    social_interact_conflict_events = ['StartingAWar', 'EndingAWar', 'EndingAConflict', 'StartingAConflict']
    unrest_events = ['Mutiny', 'Riot', 'PoliticalRevolution', 'Uprising']
    relationship_events = ['BeginningARelationship', 'RelationshipChange', 'AlteringARelationship',
                           'EndingARelationship']
    scalar_events = ['ScalarChange', 'Decreasing', 'Increasing', 'QuantityChange']
    spelling1 = ['HavingInternalState', 'HavingInternalState-']
    spelling2 = ['TakingUnderControl', 'TakingSomeoneUnderControl']
    stateplus_events = ['Repairing', 'Healing']
    statemin_events = ['Damaging', 'FallingIll']

    translocation_static = ['BeingAtAPlace']
    possession_static = ['HavingInPossession']
    conflict_static = ['BeingInConflict', 'War']
    unrest_static = ['Unrest']
    relationship_static = ['BeingInARelationship']
    internalmin_static = ['HavingInternalState-', 'HavingInternalState']
    internalplus_static = ['HavingInternalState+']

    real_disagreements = []
    disagreement_dicts = []
    process_disagreements = []

    # def count_confusion_types(event_type)
    i_stat_dyn = 0
    i_transloc = 0
    i_possess = 0
    i_violentcontest = 0
    i_unrest = 0
    i_relationship = 0
    i_scalar = 0
    i_nan1 = 0
    i_nan2 = 0
    i_spelling = 0
    i_conflict = 0
    for item in examples_partial_different:
        if type(item[0][1]) != str or type(item[1][1]) != str:
            i_nan2 += 1
        elif type(item[0][1]) == '*' or item[1][1] == '*':
            i_nan1 += 1
        elif item[0][1] in spelling1 and item[1][1] in spelling1:
            i_spelling += 1
        elif item[0][1] in spelling2 and item[1][1] in spelling2:
            i_spelling += 1
        elif item[0][1] in relationship_static and item[1][1] in relationship_events:
            i_stat_dyn += 1
        elif item[1][1] in relationship_static and item[0][1] in relationship_events:
            i_stat_dyn += 1
        elif item[0][1] in unrest_static and item[1][1] in unrest_events:
            i_stat_dyn += 1
        elif item[1][1] in unrest_static and item[0][1] in unrest_events:
            i_stat_dyn += 1
        elif item[0][1] in stateplus_events and item[1][1] in internalplus_static:
            i_stat_dyn += 1
        elif item[1][1] in stateplus_events and item[0][1] in internalplus_static:
            i_stat_dyn += 1
        elif item[0][1] in statemin_events and item[1][1] in internalmin_static:
            i_stat_dyn += 1
        elif item[1][1] in statemin_events and item[0][1] in internalmin_static:
            i_stat_dyn += 1
        elif item[0][1] in conflict_static and item[1][1] in social_interact_conflict_events:
            i_stat_dyn += 1
        elif item[1][1] in conflict_static and item[0][1] in social_interact_conflict_events:
            i_stat_dyn += 1
        elif item[0][1] in possession_static and item[1][1] in possession_events:
            i_stat_dyn += 1
        elif item[1][1] in possession_static and item[0][1] in possession_events:
            i_stat_dyn += 1
        elif item[0][1] in translocation_static and item[1][1] in translocation_events:
            i_stat_dyn += 1
        elif item[1][1] in translocation_static and item[0][1] in translocation_events:
            i_stat_dyn += 1
        elif item[0][1] in violentcontest_events and item[1][1] in violentcontest_events:
            i_violentcontest += 1
        elif item[0][1] in translocation_events and item[1][1] in translocation_events:
            i_transloc += 1
        elif item[0][1] in possession_events and item[1][1] in possession_events:
            i_possess += 1
        elif item[0][1] in social_interact_conflict_events and item[1][1] in social_interact_conflict_events:
            i_conflict += 1
        elif item[0][1] in unrest_events and item[1][1] in unrest_events:
            i_unrest += 1
        elif item[0][1] in scalar_events and item[1][1] in scalar_events:
            i_scalar += 1
        elif item[0][1] in relationship_events and item[1][1] in relationship_events:
            i_relationship += 1
        else:
            real_disagreements.append((item[0][1], item[1][1]))
            #disagreement_dicts.append(
                #{'mention_span_ids': item[0][2], 'mention_span': item[0][3], 'annotation1': item[0][1],
                # 'annotation2': item[1][1], 'mention_in_context': item[0][0]})
            #process_disagreements.append({str(item[0][2]): [item[0][1], item[1][1]]})
            # print('Mismatches accross event categories: ', item[0][1], '&', item[1][1])

    print()
    print('Amount of disagreements because eventclass was not filled out: ', i_nan1, i_nan2)
    print('Amount of disagreements because of different spelling: ', i_spelling)
    print('Amount of disagreements between matching dynamic and static events', i_stat_dyn)
    print('Amount of disagreement within Translocation events: ', i_transloc)
    print('Amount of disagreement within ChangeOfPossession events: ', i_possess)
    print('Amount of disagreement within Uprising events: ', i_unrest)
    print('Amount of disagreement within RelationshipChange events: ', i_relationship)
    print('Amount of disagreement within ScalarChange events: ', i_scalar)
    print()
    print('Amount of problematic disagreements: ', len(real_disagreements))
    print('Listing all problematic disagreements....')
    for item in real_disagreements:
        print('Mismatch accross event categories: ', item)

    print()
    print('---------------------------------------------------------------------------------------')
    print()
    print("INTERMEDIATE SCORES")

    print()
    print(annotator2, ' compared to ', annotator1, ':')
    print("Partial span and exact event type match: ", ((len(examples_partial)/len(df2))*100))
    print("Partial span and event category match: ", (((len(examples_partial_different)-len(real_disagreements))/ len(df2)) * 100))
    print("Combined agreement score: ",
          ((((len(examples_partial_different) - len(real_disagreements)) + len(examples_partial))/ len(df2)) * 100))

    print("Combined agreement score with no resolutions: ",
          (len(examples_partial) / len(
              df2) * 100))
    print()
    print("Event category disagreement score: ", ((len(real_disagreements)/ len(df2)) * 100))
    print("Coverage disagreement score: ", (100-(len(real_disagreements)/ len(df2)) * 100)-(((len(examples_partial_different) - len(real_disagreements)) + len(examples_partial))/ len(df2)) * 100)
    print()
    print('---------------------------------------------------------------------------------------')




    #return(disagreement_dicts, process_disagreements)


print('---------------------------------------------------------------------------------------')
print()
print('GENERAL STATISTICS BEFORE CHECK TASK')
print()
general_statistics(df_foelie, df_kruidnagel)
print()
print('---------------------------------------------------------------------------------------')
print()


print('RESULTS foelie')
#d1,p1=analyse_annotator_pair(df_kruidnagel, df_foelie, 'Team Kruidnagel', 'Team foelie')
analyse_annotator_pair(df_kruidnagel, df_foelie, 'Team Kruidnagel', 'Team Foelie')
analyse_annotator_pair(df_nootmuskaat, df_foelie, 'Team Nootmuskaat', 'Team Foelie')

print('RESULTS kruidnagel')
#d2,p2=analyse_annotator_pair(df_foelie, df_kruidnagel, 'Team foelie', 'Team Kruidnagel')
analyse_annotator_pair(df_foelie, df_kruidnagel, 'Team Foelie', 'Team Kruidnagel')
analyse_annotator_pair(df_nootmuskaat, df_kruidnagel, 'Team Nootmuskaat', 'Team Kruidnagel')

print('RESULTS nootmuskaat')
#d2,p2=analyse_annotator_pair(df_foelie, df_kruidnagel, 'Team foelie', 'Team Kruidnagel')
analyse_annotator_pair(df_foelie, df_nootmuskaat, 'Team Foelie', 'Team Nootmuskaat')
analyse_annotator_pair(df_kruidnagel, df_nootmuskaat, 'Team Kruidnagel', 'Team Nootmuskaat')




