'''
This code prints an IAA report and writes unresolved disagreements to tsv files.
IAA is calculated taking coverage agreement into account and resolving non-problematic disagreements
For more information on how scores were calculated, see the Event annotation IAA August 2023 report for GLOBALISE
@author StellaVerkijk
'''

import pandas as pd
from process_inception_output import main
import sys, os
from prettytable import PrettyTable


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

path_input_kaneel = "team_data_2024/inception_output/kaneel_IAA_feb_2024.tsv"
path_input_foelie = "team_data_2024/inception_output/foelie_IAA_feb_2024.tsv"
path_output = "team_data_2024/processed/"

def preprocess(path_input, path_output, teamname):
    main(path_input, path_output+teamname+'.tsv', path_output+teamname+'-triggers-c.tsv', path_output+teamname+'-triggers-conll.json')

preprocess(path_input_foelie, path_output, 'foelie')
preprocess(path_input_kaneel, path_output, 'kaneel')

#df_foelie = post_clean("team_data_2024/processed/foelie-triggers-conll.json", 'print')
#df_kruidnagel = post_clean("team_data_2024/processed/kruidnagel-triggers-conll.json", 'print')
#df_nootmuskaat = post_clean("team_data_2024/processed/nootmuskaat-triggers-conll.json", 'print')

df_foelie = post_clean("team_data_2024/processed/foelie-triggers-conll.json", 'print')
df_kaneel = post_clean("team_data_2024/processed/kaneel-triggers-conll.json", 'print')

print('Total amount of annotations Foelie: ', len(df_foelie))
print('Total amount of annotations Kaneel:', len(df_kaneel))

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


def general_statistics(df1, df2):
    foelie = make_dict(df_foelie)
    kaneel = make_dict(df_kaneel)

    print('Total amount of annotations Foelie: ', len(df_foelie))
    print('Total amount of annotations Kaneel: ', len(df_kaneel))

    all_annos = [x for x in foelie + kaneel]
    agreements = [x for x in foelie + kaneel if x in foelie and x in kaneel]

    print('Number of total annotations: ', len(all_annos))

    print('Number of tokens that received an event class label of all annotators: ', len(agreements))
    #print(agreements)

    print('Percentage of mention detection agreement: ', (len(agreements)/len(all_annos))*100)

    print()
    print('Average amount of annotations is: ' , (len(foelie)+len(kaneel))/2)


    print()

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
    occupation_events = ['TakingUnderControl', 'Enslaving']
    visit_events = ['Visit', 'Encounter', 'SocialInteraction']

    translocation_static = ['BeingAtAPlace']
    possession_static = ['HavingInPossession']
    conflict_static = ['BeingInConflict', 'War']
    unrest_static = ['Unrest']
    relationship_static = ['BeingInARelationship']
    internalmin_static = ['HavingInternalState-', 'HavingInternalState']
    internalplus_static = ['HavingInternalState+']
    occupation_static = ['Occupation']

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
    i_visit = 0
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
        elif item[0][1] in occupation_static and item[1][1] in occupation_events:
            i_stat_dyn += 1
        elif item[1][1] in occupation_static and item[0][1] in occupation_events:
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
        elif item[0][1] in visit_events and item[1][1] in visit_events:
            i_visit += 1
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
    print('Amount of disagreement within Visit events: ', i_visit)
    print('Amount of disagreement within ScalarChange events: ', i_scalar)
    print()
    print('Amount of problematic disagreements: ', len(real_disagreements))
    print('Listing all problematic disagreements....')
    for item in real_disagreements:
        print('Mismatch accross event categories: ', item)

    print()
    print('---------------------------------------------------------------------------------------')
    print()
    print("SCORES")

    print()
    print(annotator2, ' compared to ', annotator1, ':')
    print("Partial span and exact event type match: ", ((len(examples_partial)/len(df2))*100))
    print("Partial span and event category match: ", (((len(examples_partial_different)-len(real_disagreements))/ len(df2)) * 100))

    agree_res = ((((len(examples_partial_different) - len(real_disagreements)) + len(examples_partial))/ len(df2)) * 100)

    print("Combined agreement score: ",
          ((((len(examples_partial_different) - len(real_disagreements)) + len(examples_partial))/ len(df2)) * 100))

    agree_nores = (len(examples_partial) / len(df2) * 100)

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


    scores = {'agree_nores':agree_nores, 'agree_res':agree_res, 'class_agreement': class_agreement, 'class_agreement_reso': class_agreement_reso}
    return(scores)


print('---------------------------------------------------------------------------------------')
print()
print('GENERAL STATISTICS')
print()
general_statistics(df_foelie, df_kaneel)
print()
print('---------------------------------------------------------------------------------------')
print()


print('RESULTS foelie')
#d1,p1=analyse_annotator_pair(df_kruidnagel, df_foelie, 'Team Kruidnagel', 'Team foelie')
scores_FK = analyse_annotator_pair(df_kaneel, df_foelie, 'Team Kaneel', 'Team Foelie')


print('RESULTS kaneel')
#d2,p2=analyse_annotator_pair(df_foelie, df_kruidnagel, 'Team foelie', 'Team Kruidnagel')
scores_KF = analyse_annotator_pair(df_foelie, df_kaneel, 'Team Foelie', 'Team Kaneel')


avg_nores = (scores_FK['agree_nores'] + scores_KF['agree_nores']) / 2

avg_res = (scores_FK['agree_res'] + scores_KF['agree_res'] ) / 2


print("Scores after check and after resolution (fin_agree_res)")
table = PrettyTable()
table.field_names = ["", "Kaneel/Foelie", "Foelie/Kaneel", "avg"]
table.add_row(["Before resolution", scores_FK['agree_nores'], scores_KF['agree_nores'], avg_nores])
table.add_row(["After resolution", scores_FK['agree_res'], scores_KF['agree_res'], avg_res])

print(table)

print()
print()

avg_br = (scores_FK['class_agreement'] + scores_KF['class_agreement']) /2
avg_ar = (scores_FK['class_agreement_reso'] + scores_KF['class_agreement_reso']) /2

print("Average class agreement scores (span level; partial overlap")
table = PrettyTable()
table.field_names = ["", "class agreement"]
table.add_row(["BR", avg_br])
table.add_row(["AR", avg_ar])
print(table)

