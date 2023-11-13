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
from prettytable import PrettyTable
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


main("individual_data/inception_output/NL-HaNA_1.04.02_1092_0017_0021-per-text-region-1.tsv", "individual_data/processed/Manjusha.tsv", "individual_data/processed/Manjusha-triggers-c.tsv", "individual_data/processed/Manjusha-triggers-conll.json")
main("individual_data/inception_output/NL-HaNA_1.04.02_1092_0017_0021-per-text-region-2.tsv", "individual_data/processed/Kay.tsv", "individual_data/processed/Kay-triggers-c.tsv", "individual_data/processed/Kay-triggers-conll.json")
main("individual_data/inception_output/NL-HaNA_1.04.02_1092_0017_0021-per-text-region-3.tsv", "individual_data/processed/Brecht.tsv", "individual_data/processed/Brecht-triggers-c.tsv", "individual_data/processed/Brecht-triggers-conll.json")
main("individual_data/inception_output/NL-HaNA_1.04.02_1092_0017_0021-per-text-region-4.tsv", "individual_data/processed/Lodewijk.tsv", "individual_data/processed/Lodewijk-triggers-c.tsv", "individual_data/processed/Lodewijk-triggers-conll.json")

df_Manjusha = post_clean("individual_data/processed/Manjusha-triggers-conll.json", 'print')
df_Brecht = post_clean("individual_data/processed/Brecht-triggers-conll.json", 'print')
df_Kay = post_clean("individual_data/processed/Kay-triggers-conll.json", 'print')
df_Lodewijk = post_clean("individual_data/processed/Lodewijk-triggers-conll.json", 'print')

print('Total amount of annotations Manjusha: ', len(df_Manjusha))
print('Total amount of annotations Lodewijk:', len(df_Lodewijk))
print('Total amount of annotations Brecht: ', len(df_Brecht))
print('Total amount of annotations Kay:', len(df_Kay))

#EXACT MATCHES ALL ANNOTATORS

def make_dict(df):
    l = []
    for index, row in df.iterrows():
        l.append({'mention_token_id': row['mention_token_id']})
    return(l)

def make_span_dict(df):
    l = []
    for index, row in df.iterrows():
        l.append({'mention_ids': row['mention_ids']})
    return(l)

def general_statistics(df_Brecht, df_Kay, df_Manjusha, df_Lodewijk):
    Brecht = make_dict(df_Brecht)
    Lodewijk = make_dict(df_Lodewijk)
    Manjusha = make_dict(df_Manjusha)
    Kay = make_dict(df_Kay)
    print(Kay)

    print('Total amount of annotations Manjusha: ', len(df_Manjusha))
    print('Total amount of annotations Lodewijk:', len(df_Lodewijk))
    print('Total amount of annotations Brecht: ', len(df_Brecht))
    print('Total amount of annotations Kay:', len(df_Kay))
    print()

    all_annos = [x for x in Brecht + Lodewijk + Manjusha + Kay]
    print('all annos, ', all_annos)
    agreements = [x for x in Brecht + Lodewijk + Manjusha + Kay if x in Brecht and x in Kay and x in Lodewijk and x in Manjusha]

    print('Number of total annotations: ', len(all_annos))

    print('Number of tokens that received an event class label of all annotators: ', len(agreements))
    #print(agreements)

    print('Percentage of mention detection agreement (token level): ', (len(agreements)/len(all_annos))*100)

    print()
    print('Average amount of annotations is: ' , ((len(Brecht)+len(Lodewijk)+len(Manjusha)+len(Kay))/4))
    print('Average amount of annotations per scan is: ' , ((len(Brecht)+len(Lodewijk)+len(Manjusha)+len(Kay))/4) / 5)

    print()

    Brecht = make_span_dict(df_Brecht)
    Lodewijk = make_span_dict(df_Lodewijk)
    Manjusha = make_span_dict(df_Manjusha)
    Kay = make_span_dict(df_Kay)
    print(Kay)

    print('Total amount of span annotations Manjusha: ', len(df_Manjusha))
    print('Total amount of span annotations Lodewijk:', len(df_Lodewijk))
    print('Total amount of span annotations Brecht: ', len(df_Brecht))
    print('Total amount of span annotations Kay:', len(df_Kay))
    print()

    all_annos = [x for x in Brecht + Lodewijk + Manjusha + Kay]
    print('all annos, ', all_annos)
    agreements = [x for x in Brecht + Lodewijk + Manjusha + Kay if x in Brecht and x in Kay and x in Lodewijk and x in Manjusha]

    print('Number of total span annotations: ', len(all_annos))

    print('Number of spans that received an event class label of all annotators (perfect match): ', len(agreements))
    #print(agreements)

    print('Percentage of mention detection agreement (span level): ', (len(agreements)/len(all_annos))*100)

    print()
    print('Average amount of span annotations is: ' , ((len(Brecht)+len(Lodewijk)+len(Manjusha)+len(Kay))/4))
    print('Average amount of span annotations per scan is: ' , ((len(Brecht)+len(Lodewijk)+len(Manjusha)+len(Kay))/4) / 5)




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

def analyse_annotator_pair(df1, df2, annotator1, annotator2, df_check1, df_check2):


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

    int_agree_res = ((((len(examples_partial_different) - len(real_disagreements)) + len(examples_partial))/ len(df2)) * 100)
    print("Combined agreement score: ",
          ((((len(examples_partial_different) - len(real_disagreements)) + len(examples_partial))/ len(df2)) * 100))

    int_agree_nores = (len(examples_partial) / len(df2) * 100)
    print("Combined agreement score with no resolutions: ",
          (len(examples_partial) / len(
              df2) * 100))
    print()
    print("Event category disagreement score: ", ((len(real_disagreements)/ len(df2)) * 100))
    print("Coverage disagreement score: ", (100-(len(real_disagreements)/ len(df2)) * 100)-(((len(examples_partial_different) - len(real_disagreements)) + len(examples_partial))/ len(df2)) * 100)
    print()
    print()
    all_spans_by_both_annotators = len(examples_partial) + len(examples_partial_different)
    class_agreement = (len(examples_partial) / all_spans_by_both_annotators) * 100
    print('amount of class agreement before reso: ', class_agreement)

    class_agreement_reso = ((len(examples_partial) + (len(examples_partial_different)-len(real_disagreements))) / all_spans_by_both_annotators) * 100
    print('amount of class agreement after reso: ', class_agreement_reso)
    print('---------------------------------------------------------------------------------------')


    print('ANALYSIS ANNOTATOR PAIR ' +annotator1+" & "+annotator2+ " after secondary check-annotation task")


    complete1 = append_checked_annotations(df1, df_check1)
    complete2 = append_checked_annotations(df2, df_check2)


    print('Total amount of annotations '+annotator1+': ', len(complete1))
    print('Total amount of annotations '+annotator2+': ', len(complete2))

    #EXACT MATCHES
    examples_exact=[]
    for index_1, row_1 in complete1.iterrows():
        for index_2, row_2 in complete2.iterrows():
            if row_1['mention_ids'] == row_2['mention_ids'] and row_1['eventclass_no_number'] == row_2['eventclass_no_number']: #if row_l['mention_span'] == row_2['mention_span'] and
                    examples_exact.append(row_2['mention_in_context'])


    print("# exact span matches: ", len(examples_exact))


    #EXACT SPAN MATCHES DIFFERENT LABEL
    examples_exact_different=[]
    for index_1, row_1 in complete1.iterrows():
        for index_2, row_2 in complete2.iterrows():
            if row_1['mention_ids'] == row_2['mention_ids'] and row_1['eventclass_no_number'] != row_2['eventclass_no_number']: #if row_l['mention_span'] == row_2['mention_span'] and
                    examples_exact_different.append(((row_1['mention_in_context'], row_1['eventclass_no_number']), (row_2['mention_in_context'], row_2['eventclass_no_number'])))

    print("# exact span matches different label: ", len(examples_exact_different))

    #for item in examples_exact_different[:5]:
    #    print(item)

    #PARTIAL SPAN MATCHES

    examples_partial=[]
    for index_1, row_1 in complete1.iterrows():
        for index_2, row_2 in complete2.iterrows():
            if len(set(row_1['mention_ids']).intersection(set(row_2['mention_ids'])))>0 and row_1['eventclass_no_number'] == row_2['eventclass_no_number']:
                examples_partial.append(((row_1['mention_in_context'], row_1['eventclass_no_number']), (row_2['mention_in_context'], row_2['eventclass_no_number'])))


    print("# partial span matches: ", len(examples_partial))

    #for item in examples_partial[:5]:
    #    print(item)


    ### PARTIAL SPAN MATCHES DIFFERENT LABEL seeing which spans are annotated with a different label

    examples_partial_different = []

    for index_1, row_1 in complete1.iterrows():
        for index_2, row_2 in complete2.iterrows():
            if len(set(row_1['mention_ids']).intersection(set(row_2['mention_ids'])))>0 and row_1['eventclass_no_number'] != row_2['eventclass_no_number']:
                examples_partial_different.append(((row_1['mention_in_context'], row_1['eventclass_no_number'], row_1['mention_ids'], row_1['mention_span']), (row_2['mention_in_context'], row_2['eventclass_no_number'], row_2['mention_ids'], row_2['mention_span'])))


    print("partial span matches different label: ", len(examples_partial_different))

    translocation_events = ['TransLocation', 'Transportation', 'Leaving', 'Arriving', 'Voyage', 'Translocation']
    possession_events = ['Buying', 'Selling', 'Getting', 'Giving', 'LosingPossession', 'FinancialTransaction', 'Trade', 'ChangeOfPossession']
    violentcontest_events = ['ViolentContest', 'Attacking', 'Besieging', 'Invasion', 'Killing']
    conflict_events = ['StartingAWar', 'EndingAWar', 'EndingAConflict', 'StartingAConflict']
    unrest_events = ['Mutiny', 'Riot', 'PoliticalRevolution', 'Uprising']
    relationship_events = ['BeginningARelationship', 'RelationshipChange', 'AlteringARelationship', 'EndingARelationship']
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

    #def count_confusion_types(event_type)
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
        elif type(item[0][1]) =='*' or item[1][1] == '*':
            i_nan1 += 1
        elif item[0][1] in spelling1 and item[1][1] in spelling1:
            i_spelling += 1
        elif item[0][1] in spelling2 and item[1][1] in spelling2:
            i_spelling += 1
        elif item[0][1] in relationship_static and item[1][1] in relationship_events:
            i_stat_dyn +=1
        elif item[1][1] in relationship_static and item[0][1] in relationship_events:
            i_stat_dyn +=1
        elif item[0][1] in unrest_static and item[1][1] in unrest_events:
            i_stat_dyn +=1
        elif item[1][1] in unrest_static and item[0][1] in unrest_events:
            i_stat_dyn +=1
        elif item[0][1] in stateplus_events and item[1][1] in internalplus_static:
            i_stat_dyn +=1
        elif item[1][1] in stateplus_events and item[0][1] in internalplus_static:
            i_stat_dyn +=1
        elif item[0][1] in statemin_events and item[1][1] in internalmin_static:
            i_stat_dyn +=1
        elif item[1][1] in statemin_events and item[0][1] in internalmin_static:
            i_stat_dyn +=1
        elif item[0][1] in conflict_static and item[1][1] in conflict_events:
            i_stat_dyn +=1
        elif item[1][1] in conflict_static and item[0][1] in conflict_events:
            i_stat_dyn +=1
        elif item[0][1] in possession_static and item[1][1] in possession_events:
            i_stat_dyn +=1
        elif item[1][1] in possession_static and item[0][1] in possession_events:
            i_stat_dyn +=1
        elif item[0][1] in translocation_static and item[1][1] in translocation_events:
            i_stat_dyn +=1
        elif item[1][1] in translocation_static and item[0][1] in translocation_events:
            i_stat_dyn +=1
        elif item[0][1] in violentcontest_events and item[1][1] in violentcontest_events:
            i_violentcontest += 1
        elif item[0][1] in translocation_events and item[1][1] in translocation_events:
            i_transloc += 1
        elif item[0][1] in possession_events and item[1][1] in possession_events:
            i_possess += 1
        elif item[0][1] in conflict_events and item[1][1] in conflict_events:
            i_conflict += 1
        elif item[0][1] in unrest_events and item[1][1] in unrest_events:
            i_unrest += 1
        elif item[0][1] in scalar_events and item[1][1] in scalar_events:
            i_scalar += 1
        elif item[0][1] in relationship_events and item[1][1] in relationship_events:
            i_relationship += 1
        else:
            real_disagreements.append((item[0][1], item[1][1]))
            disagreement_dicts.append({'mention_span_ids': item[0][2], 'mention_span':item[0][3], 'annotation1': item[0][1], 'annotation2': item[1][1], 'mention_in_context':item[0][0]})
            process_disagreements.append({str(item[0][2]):[item[0][1], item[1][1]]})
            #print('Mismatches accross event categories: ', item[0][1], '&', item[1][1])

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
    check_count = i_nan1 + i_nan2 + i_spelling + i_stat_dyn + i_transloc + i_possess + i_unrest + i_relationship + i_scalar + i_conflict + i_violentcontest

    print('Amount of problematic disagreements: ', len(real_disagreements), len(examples_partial_different)-check_count)

    print('Listing all problematic disagreements...')
    for item in real_disagreements:
        print('Mismatch accross event categories: ', item)



    print()
    print('---------------------------------------------------------------------------------------')

    print("FINAL SCORES")

    print()
    print(annotator2, ' compared to ', annotator1, ':')
    print("Partial span and exact event type match: ", ((len(examples_partial)/len(complete2))*100))
    print("Partial span and event category match: ", (((len(examples_partial_different)-len(real_disagreements))/ len(complete2)) * 100))

    fin_agree_res = ((((len(examples_partial_different) - len(real_disagreements)) + len(examples_partial))/ len(complete2)) * 100)
    print("Combined agreement score: ",
          ((((len(examples_partial_different) - len(real_disagreements)) + len(examples_partial))/ len(complete2)) * 100))

    fin_agree_nores = (len(examples_partial) / len(complete2) * 100)
    print("Combined agreement score with no resolutions: ",
          (len(examples_partial) / len(
              complete2) * 100))
    print()
    print("Event category disagreement score: ", ((len(real_disagreements)/ len(complete2)) * 100))
    print("Coverage disagreement score: ", (100-(len(real_disagreements)/ len(complete2)) * 100)-(((len(examples_partial_different) - len(real_disagreements)) + len(examples_partial))/ len(complete2)) * 100)
    print()
    print()
    all_spans_by_both_annotators = len(examples_partial) + len(examples_partial_different)
    class_agreement2 = (len(examples_partial) / all_spans_by_both_annotators) * 100
    print('amount of class agreement before reso: ', class_agreement2)

    class_agreement_reso2 = ((len(examples_partial) + (len(examples_partial_different)-len(real_disagreements))) / all_spans_by_both_annotators) * 100
    print('amount of class agreement after reso: ', class_agreement_reso2)
    print('---------------------------------------------------------------------------------------')

    scores = {'int_agree_nores': int_agree_nores, 'int_agree_res':int_agree_res, 'fin_agree_nores':fin_agree_nores, 'fin_agree_res':fin_agree_res, 'class_agreement': class_agreement, 'class_agreement_reso': class_agreement_reso, 'class_agreement2': class_agreement2, 'class_agreement_reso2': class_agreement_reso2}
    return(scores, disagreement_dicts, process_disagreements)

Lcheck1= pd.read_csv('individual_data/checked_data/Lcheck1.tsv', delimiter='\t', index_col=None)
Lcheck2= pd.read_csv('individual_data//checked_data/Lcheck2.tsv', delimiter='\t', index_col=None)
Lcheck3= pd.read_csv('individual_data//checked_data/Lcheck3.tsv', delimiter='\t', index_col=None)

Mcheck2= pd.read_csv('individual_data//checked_data/Mcheck2.tsv', delimiter='\t', index_col=None)
Mcheck3= pd.read_csv('individual_data//checked_data/Mcheck3.tsv', delimiter='\t', index_col=None)
Mcheck4= pd.read_csv('individual_data//checked_data/Mcheck4.tsv', delimiter='\t', index_col=None)

Kcheck1= pd.read_csv('individual_data//checked_data/Kcheck1.tsv', delimiter='\t', index_col=None)
Kcheck3= pd.read_csv('individual_data//checked_data/Kcheck3.tsv', delimiter='\t', index_col=None)
Kcheck4= pd.read_csv('individual_data//checked_data/Kcheck4.tsv', delimiter='\t', index_col=None)

Bcheck1= pd.read_csv('individual_data//checked_data/Bcheck1.tsv', delimiter='\t', index_col=None)
Bcheck2= pd.read_csv('individual_data//checked_data/Bcheck2.tsv', delimiter='\t', index_col=None)
Bcheck4= pd.read_csv('individual_data//checked_data/Bcheck4.tsv', delimiter='\t', index_col=None)

complete_B = append_checked_annotations2(df_Brecht, Bcheck1, Bcheck2, Bcheck4)
complete_L = append_checked_annotations2(df_Lodewijk, Lcheck1, Lcheck2, Lcheck3)
complete_K = append_checked_annotations2(df_Kay, Kcheck1, Kcheck3, Kcheck4)
complete_M = append_checked_annotations2(df_Manjusha, Mcheck2, Mcheck3, Mcheck4)

print('---------------------------------------------------------------------------------------')
print()
print('GENERAL STATISTICS BEFORE CHECK TASK')
print()
general_statistics(df_Brecht, df_Kay, df_Manjusha, df_Lodewijk)
print()
print('---------------------------------------------------------------------------------------')
print()
print('GENERAL STATISTICS AFTER CHECK TASK')
print()
general_statistics(complete_K, complete_B, complete_M, complete_L)
print()
print('---------------------------------------------------------------------------------------')

print('RESULTS LODEWIJK')
scores_LK,d1,p1=analyse_annotator_pair(df_Kay, df_Lodewijk, 'Kay', 'Lodewijk', Kcheck4, Lcheck2)
scores_LM,d2,p2=analyse_annotator_pair(df_Manjusha, df_Lodewijk, 'Manjusha', 'Lodewijk', Mcheck4, Lcheck1)
scores_LB,d3,p3=analyse_annotator_pair(df_Brecht, df_Lodewijk, 'Brecht', 'Lodewijk', Bcheck4, Lcheck3)

print('RESULTS BRECHT')
scores_BM,d4,p4=analyse_annotator_pair(df_Manjusha, df_Brecht, 'Manjusha', 'Brecht', Mcheck3, Bcheck1)
scores_BL,d5,p5=analyse_annotator_pair(df_Lodewijk, df_Brecht, 'Lodewijk', 'Brecht', Lcheck3, Bcheck4)
scores_BK,d6,p6=analyse_annotator_pair(df_Kay, df_Brecht, 'Kay', 'Brecht', Kcheck3, Bcheck2)

print('RESULTS KAY')
scores_KB,d7,p7=analyse_annotator_pair(df_Brecht, df_Kay, 'Brecht', 'Kay', Bcheck2, Kcheck3)
scores_KL,d8,p8=analyse_annotator_pair(df_Lodewijk, df_Kay, 'Lodewijk', 'Kay', Lcheck2, Kcheck4)
scores_KM,d9,p9=analyse_annotator_pair(df_Manjusha, df_Kay, 'Manjusha', 'Kay', Mcheck2, Kcheck1)

print('RESULTS MANJUSHA')
scores_ML,d10,p10=analyse_annotator_pair(df_Lodewijk, df_Manjusha, 'Lodewijk', 'Manjusha', Lcheck1, Mcheck4)
scores_MK,d11,p11=analyse_annotator_pair(df_Kay, df_Manjusha, 'Kay', 'Manjusha', Kcheck1, Mcheck2)
scores_MB,d12,p12=analyse_annotator_pair(df_Brecht, df_Manjusha, 'Brecht', 'Manjusha', Bcheck1, Mcheck3)


########## Get label disagreements

all_disagreements = d1+d2+d3+d4+d5+d6+d7+d8+d9+d10+d11+d12
all_processed = p1+p2+p3+p4+p5+p6+p7+p8+p9+p10+p11+p12

# Gather all annotations for mentions where disagreement occurs, where each annotation from different anntotators are seperate entries
dd = defaultdict(list)
for d in all_processed:
    for key, value in d.items():
        dd[key].extend(value)


# Gather all annotations by all annotators for one specific mention together
## In order to do this, list values for mention_ids have to be converted to strings
gather_all = []
for d in all_disagreements:
    for key, value in dd.items():
        if str(d['mention_span_ids']) == key:
            gather_all.append({'mention_span_ids': str(d['mention_span_ids']), 'mention_span': d['mention_span'], 'annotations': str(set(dd[key])), 'mention_in_context':d['mention_in_context']})

merge_duplicates = [dict(t) for t in {tuple(d.items()) for d in gather_all}]

# As a final step we convert mention_ids and lists of annotated event trigger labels back to list objects
final_annotated_disagreements = []
for d in merge_duplicates:
    final_annotated_disagreements.append({'mention_span_ids': eval(d['mention_span_ids']), 'mention_span': d['mention_span'], 'annotations':eval(d['annotations']),'mention_in_context':d['mention_in_context']})

df_type_disagreements = pd.DataFrame(final_annotated_disagreements)



########### Get coverage disagreements

# Get all disagreements of mentions of which at least one annotator said it should receive a label and at least one annotator said it should not receive a label

def get_cover_disagree(df):
    """
    Returns a list of dictionaries containing all relevant mentions (token ids) and labels
    """
    mentions = []
    indces = []
    for index, row in df.iterrows():
        if row['Should this mention be annotated as an event?'] == 'yes':
            indces.append(index)
    df = df.drop(indces)

    for index, row in df.iterrows():
        mentions.append({'mention_span_ids':str(row['mention_ids']), 'mention_span':row['mention_span'], 'mention_in_context':row['mention_in_context']})

    return(mentions)

list1 = get_cover_disagree(Bcheck1)
list2 = get_cover_disagree(Bcheck2)
list3 = get_cover_disagree(Bcheck4)
list4 = get_cover_disagree(Kcheck1)
list5 = get_cover_disagree(Kcheck3)
list6 = get_cover_disagree(Kcheck4)
list7 = get_cover_disagree(Mcheck2)
list8 = get_cover_disagree(Mcheck3)
list9 = get_cover_disagree(Mcheck4)
list10 = get_cover_disagree(Lcheck1)
list11 = get_cover_disagree(Lcheck2)
list12 = get_cover_disagree(Lcheck3)

all = list1+list2+list3+list4+list5+list6+list7+list8+list9+list10+list11+list12


all_coverage_disagreements = [dict(t) for t in {tuple(d.items()) for d in all}]

final_coverage_disagreements = []
for d in all_coverage_disagreements:
    final_coverage_disagreements.append({'mention_span_ids': eval(d['mention_span_ids']), 'mention_span': d['mention_span'], 'mention_in_context':d['mention_in_context']})


df_coverage = pd.DataFrame(final_coverage_disagreements)

#### delete overlap of coverage disagreements with label disagreements

condition = df_coverage['mention_span_ids'].isin(df_type_disagreements['mention_span_ids'])
df_coverage.drop(df_coverage[condition].index, inplace = True)

#df_type_disagreements.to_csv("data/unresolved_disagreements/annotated_disagreements_test_set_triggers.tsv")
#df_coverage.to_csv('data/unresolved_disagreements/filtered_coverage_disagreements_test_set_triggers.tsv')

############# print tables

# before check before resolution (int_agree_nores)

print("Scores before check and before resolution (int_agree_nores)")
table = PrettyTable()
table.field_names = ["", "Ann1", "Ann2", "Ann3", "Ann4"]
table.add_row(["Ann1", "X", scores_KM['int_agree_nores'], scores_BM['int_agree_nores'], scores_LM['int_agree_nores']])
table.add_row(["Ann2", scores_MK['int_agree_nores'], 'X', scores_BK['int_agree_nores'], scores_LK['int_agree_nores']])
table.add_row(["Ann3", scores_MB['int_agree_nores'], scores_KB['int_agree_nores'], 'X', scores_LB['int_agree_nores']])
table.add_row(["Ann4", scores_ML['int_agree_nores'], scores_KL['int_agree_nores'], scores_BL['int_agree_nores'], 'X'])
print(table)

print()
print()

print("Scores before check and after resolution (int_agree_res)")
table = PrettyTable()
table.field_names = ["", "Ann1", "Ann2", "Ann3", "Ann4"]
table.add_row(["Ann1", "X", scores_KM['int_agree_res'], scores_BM['int_agree_res'], scores_LM['int_agree_res']])
table.add_row(["Ann2", scores_MK['int_agree_res'], 'X', scores_BK['int_agree_res'], scores_LK['int_agree_res']])
table.add_row(["Ann3", scores_MB['int_agree_res'], scores_KB['int_agree_res'], 'X', scores_LB['int_agree_res']])
table.add_row(["Ann4", scores_ML['int_agree_res'], scores_KL['int_agree_res'], scores_BL['int_agree_res'], 'X'])
print(table)

print()
print()

print("Scores after check and before resolution (fin_agree_nores)")
table = PrettyTable()
table.field_names = ["", "Ann1", "Ann2", "Ann3", "Ann4"]
table.add_row(["Ann1", "X", scores_KM['fin_agree_nores'], scores_BM['fin_agree_nores'], scores_LM['fin_agree_nores']])
table.add_row(["Ann2", scores_MK['fin_agree_nores'], 'X', scores_BK['fin_agree_nores'], scores_LK['fin_agree_nores']])
table.add_row(["Ann3", scores_MB['fin_agree_nores'], scores_KB['fin_agree_nores'], 'X', scores_LB['fin_agree_nores']])
table.add_row(["Ann4", scores_ML['fin_agree_nores'], scores_KL['fin_agree_nores'], scores_BL['fin_agree_nores'], 'X'])
print(table)

print()
print()

print("Scores after check and after resolution (fin_agree_res)")
table = PrettyTable()
table.field_names = ["", "Ann1", "Ann2", "Ann3", "Ann4"]
table.add_row(["Ann1", "X", scores_KM['fin_agree_res'], scores_BM['fin_agree_res'], scores_LM['fin_agree_res']])
table.add_row(["Ann2", scores_MK['fin_agree_res'], 'X', scores_BK['fin_agree_res'], scores_LK['fin_agree_res']])
table.add_row(["Ann3", scores_MB['fin_agree_res'], scores_KB['fin_agree_res'], 'X', scores_LB['fin_agree_res']])
table.add_row(["Ann4", scores_ML['fin_agree_res'], scores_KL['fin_agree_res'], scores_BL['fin_agree_res'], 'X'])
print(table)


print()
print()

avg_bc_br = (scores_KM['class_agreement'] + scores_KL['class_agreement'] + scores_KB['class_agreement'] + scores_MK['class_agreement'] + scores_MB['class_agreement'] + scores_ML['class_agreement'] + scores_BL['class_agreement'] + scores_BK['class_agreement'] + scores_BM['class_agreement'] + scores_LM['class_agreement'] + scores_LK['class_agreement'] + scores_LB['class_agreement']) /12
avg_bc_ar = (scores_KM['class_agreement_reso'] + scores_KL['class_agreement_reso'] + scores_KB['class_agreement_reso'] + scores_MK['class_agreement_reso'] + scores_MB['class_agreement_reso'] + scores_ML['class_agreement_reso'] + scores_BL['class_agreement_reso'] + scores_BK['class_agreement_reso'] + scores_BM['class_agreement_reso'] + scores_LM['class_agreement_reso'] + scores_LK['class_agreement_reso'] + scores_LB['class_agreement_reso']) /12
avg_ac_br = (scores_KM['class_agreement2'] + scores_KL['class_agreement2'] + scores_KB['class_agreement2'] + scores_MK['class_agreement2'] + scores_MB['class_agreement2'] + scores_ML['class_agreement2'] + scores_BL['class_agreement2'] + scores_BK['class_agreement2'] + scores_BM['class_agreement2'] + scores_LM['class_agreement2'] + scores_LK['class_agreement2'] + scores_LB['class_agreement2']) /12
avg_ac_ar = (scores_KM['class_agreement_reso2'] + scores_KL['class_agreement_reso2'] + scores_KB['class_agreement_reso2'] + scores_MK['class_agreement_reso2'] + scores_MB['class_agreement_reso2'] + scores_ML['class_agreement_reso2'] + scores_BL['class_agreement_reso2'] + scores_BK['class_agreement_reso2'] + scores_BM['class_agreement_reso2'] + scores_LM['class_agreement_reso2'] + scores_LK['class_agreement_reso2'] + scores_LB['class_agreement_reso2']) /12

print("Average class agreement scores (span level; partial overlap")
table = PrettyTable()
table.field_names = ["", "S1.1", "S1.2"]
table.add_row(["BR", avg_bc_br, avg_ac_br])
table.add_row(["AR", avg_bc_ar, avg_ac_ar])
print(table)