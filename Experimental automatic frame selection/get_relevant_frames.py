"""
@author Stella Verkijk
"""

import pandas as pd
import xml.etree.ElementTree as ET

from find_english_frame_matches2 import xml_to_dict, match_verbs_find_frames, read_pm, extract_predicates_and_frames, match_to_predicate_matrix

def filter_on_frequency_range(filepath):

    if filepath.endswith('.ods'):
        df = pd.read_excel(filepath, engine = 'odf')
    else:
        df = pd.read_excel(filepath)

    pilot_df_0 = df[df[' nr. mentions'] >= 5]
    pilot_df = pilot_df_0[pilot_df_0[' nr. mentions'] <=15]

    return(pilot_df)

def filter_on_translation(pilot_df, rowname):
    
    trans_df = pilot_df[pilot_df[rowname] != 0] 
    return(trans_df)
    
def match_luindex(path_to_xml, df, rowname):
    
    dictionary_nlIndex = xml_to_dict(path_to_xml)
    df_with_nllu = match_verbs_find_frames(df, dictionary_nlIndex, rowname)
    
    return(df_with_nllu)
    
def match_predicate_matrix(path_to_predicate_matrix, df_with_nllu, rowname):
    
    list_lines = read_pm(path_to_predicate_matrix)
    extracted_synsets_and_frames = extract_predicates_and_frames(list_lines)
    df_with_frames = match_to_predicate_matrix(extracted_synsets_and_frames, df_with_nllu, rowname)
    
    return(df_with_frames)
    
def get_unique_frames(df):
    
    frames = []
    list_frames = df['all_matched_frames'].tolist()
    for l in list_frames:
        for item in l:
            frames.append(item)
        
    unique_frames = set(frames)
    return(unique_frames)

path_to_ordered_events_pos = 'data/events_pos_filter_VRB_ordered_frequency_over_1.ods'  
df = filter_on_frequency_range(path_to_ordered_events_pos) #this results in the Excel that is manually searched through and wehere relevant predicates are provided with a modern Dutch translation
#df.to_excel('../data/relevant frame selection/relevant_predicates_pilot_df.xlsx')

rowname_ships = 'Modern Dutch translation (Schepen)'
rowname_authority = 'Modern Dutch translation (Polities)'

df_with_translations = pd.read_excel('data/relevant frame selection/relevant_predicates_pilot_df.xlsx') #the Excel file with selected relevant predicates and their translations

df_ships = filter_on_translation(df_with_translations, rowname_ships)
df_polities = filter_on_translation(df_with_translations, rowname_authority)
    
# match with nl-luIndex       
path_to_xml = 'data/nl-luIndex.xml'
df_with_nllu_ships = match_luindex(path_to_xml, df_ships, rowname_ships)
df_with_nllu_authority = match_luindex(path_to_xml, df_polities, rowname_authority)

# match with predicate matrix 
path_to_predicate_matrix = 'data/PredicateMatrix.v1.3.txt.role.odwn'
df_with_frames_ships = match_predicate_matrix(path_to_predicate_matrix, df_with_nllu_ships, rowname_ships)
df_with_frames_authority = match_predicate_matrix(path_to_predicate_matrix, df_with_nllu_authority, rowname_authority)

#df_with_frames_ships.to_excel('../data/test_frames_ships.xlsx', index = False)

# make a column that shows which frames were matched with the modern Dutch translations both in the nllu index and the predicate matrix
df_with_frames_ships['frames_that_appear_in_both'] = [(set(a).intersection(b)) for a, b in zip(df_with_frames_ships['nl-luIndex_frame'], df_with_frames_ships['predicate_matrix_frame'])]
df_with_frames_authority['frames_that_appear_in_both'] = [(set(a).intersection(b)) for a, b in zip(df_with_frames_authority['nl-luIndex_frame'], df_with_frames_authority['predicate_matrix_frame'])]

# make a column that shows all frames that were matched with the modern Dutch translations, either in the nllu index and the predicate matrix
df_with_frames_ships['all_matched_frames'] = [(set(a).union(b)) for a, b in zip(df_with_frames_ships['nl-luIndex_frame'], df_with_frames_ships['predicate_matrix_frame'])]
df_with_frames_authority['all_matched_frames'] = [(set(a).union(b)) for a, b in zip(df_with_frames_authority['nl-luIndex_frame'], df_with_frames_authority['predicate_matrix_frame'])]

df_with_frames_ships.drop(labels=['supersynset', 'eso', 'synsets'], axis=1, inplace=True)
df_with_frames_ships.to_excel('data/relevant frame selection/ship_movement_frames.xlsx', index=False)

df_with_frames_authority.drop(labels=['supersynset', 'eso', 'synsets'], axis=1, inplace=True)
df_with_frames_authority.to_excel('data/relevant frame selection/authority_frames.xlsx', index=False)

unique_frames_ships = get_unique_frames(df_with_frames_ships)
unique_frames_authority = get_unique_frames(df_with_frames_authority)

with open ('data/relevant frame selection/unique_frames_ships.txt', 'w') as outfile:
    outfile.write(str(unique_frames_ships))
    
with open ('data/relevant frame selection/unique_frames_authority.txt', 'w') as outfile:
    outfile.write(str(unique_frames_authority))
    
print('Amount of unique frames associated with ship movement: ', len(unique_frames_ships))
print('Amount of unique frames associated with authority: ', len(unique_frames_authority))

unique_frames = unique_frames_ships.union(unique_frames_authority)
print(len(unique_frames))
      
