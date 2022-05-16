"""
Match modern Dutch translations of verbs in the events_pos file to frames in the predicate matrix
This version of the code takes a subset of the events_pos file
@author Stella Verkijk
"""

import pandas as pd

def read_pm(path_to_predicate_matrix):
    """
    Reads predicate matrix and returns a list of lines
    :param path_to_predicate_matrix: str
    """
    list_lines = []
    with open (path_to_predicate_matrix, 'r', encoding='utf-8') as infile:
        for line in infile:
            list_lines.append(line)
        
    return(list_lines)


def extract_predicates_and_frames(list_lines):
    """
    Takes lines from the predicate matrix and extracts lists of dutch synsets and corresponding frames
    :param list_lines: list of lists
    """
    
    info = []
    for line in list_lines: #loop over lines in predicate matrix 
        split = line.split(' ') #create a list with seperate strings (line is split on whitespace)
        temp_info = [] #create temporary list to add the frame name and a list of the corresponding dutch predicates for each line
        for item in split:
            if item.startswith('fn:'):
                temp_info.append(item[3:])
            if item.startswith('odwn-synset:'):
                temp_info.append((item.split(':')[1][:-1]).split(';'))
                info.append(temp_info) #add the list for each line to a bigger list to represent the whole predicate matrix
    
    #add a zero to each time where there is no corresponding frame for a set of dutch predicates (done for further processing)
    for item in info:
        if len(item) == 1:
            item.append(0)
        
    return(info)

def match_to_predicate_matrix(extracted_info, path_to_events_pos):
    """
    matches modern Dutch translations with Dutch predicates from the predicate matrix and gathers corresponding frames in new column in the events_pos dataframe.
    Returns the events_pos dataframe with a column of corresponding frames from the predicate matrix
    
    :param extracted_info: list of lists
    :param path_to_events_pos: str
    """

    df_events_pos = pd.read_excel(path_to_events_pos)
    modern_d = df_events_pos['Modern Dutch translation (inf.)'].tolist() #gather modern dutch translations in a list
    
    list_matched_frames = []
    for md in modern_d: #loop over modern dutch translations
        temp_list = []
        for item in extracted_info: #for each list of dutch predicates and their corresponding frame
            if md in item[0]: #if the modern dutch translation matches with one of the predicates of a specific line in the predicate matrix
                temp_list.append(item[1]) #append the corresponding frame to a temporary list
        list_matched_frames.append(temp_list) #append the collection of corresponding frames to a bigger list
        
    #we process the collected frames in order to delete duplicates and zeroes
    matched_frames = [] 
    for item in list_matched_frames: #loop over the matched frames
        new_item = set(item) #turn the list into a set in order to get rid of double entries
        newest_item = list(new_item) #turn the set back into a list
        if 0 in newest_item: #remove any zeroes from the list
            newest_item.remove(0)
        matched_frames.append(newest_item)
        
    df_events_pos['predicate_matrix_frame'] = matched_frames #add a column to the events_pos file with the matched and processed frames
    return(df_events_pos)
    
    
path_to_predicate_matrix = 'data/PredicateMatrix.v1.3.txt.role.odwn'
path_to_events_pos = 'data/test_nllu.xlsx'

list_lines = read_pm(path_to_predicate_matrix)
extracted_synsets_and_frames = extract_predicates_and_frames(list_lines)
df_with_frames = match_to_predicate_matrix(extracted_synsets_and_frames, path_to_events_pos)

        
df_with_frames.to_excel('data/test_pm.xlsx', index=False)
 


