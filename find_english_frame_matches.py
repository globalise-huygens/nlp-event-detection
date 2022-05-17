"""
Match modern Dutch translations of verbs in the events_pos file to frames in the nl-luIndex and the predicate matrix
This version of the code takes a subset of the events_pos file
Returns an excel file that is events_pos with three new columns
- English frames from the nl-luIndex that match the modern Dutch translation
- Enslgish frames from the predicate matrix that match the modern Dutch translation
- frames that were a match with the modern Dutch translation both in the nl-luIndex and the predicate matrix
@author Stella Verkijk
"""

import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_dict(path_to_xml):
    """
    reads in xml file (nl-luIndex) and converts it to a dictionary of english Frame names and the matching dutch verbs
    :param path_to_xsml: str
    """
    
    xmlfile = path_to_xml
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    
    #create a list with frame names and dutch lexical units, retaining indexing. 
    list_frames = []
    list_dutch = []
    for entry in root.findall('{http://framenet.icsi.berkeley.edu}lu'):
        frameName = entry.get('frameName')
        name = entry.get('name')
        list_frames.append(frameName)
        #only append the lexical unit, without '.v' or '.n' 
        list_dutch.append(name[:-2])
        
    #create a dataframe with one column for frame names and one column for the corresponding dutch lexical units
    df = pd.DataFrame({'Frame':list_frames, 'Dutch lexical unit':list_dutch})
    
    #group the df so that for each dutch lexical unit, all corresponding frame names are collected. 
    #the df will order the Dutch lexical units in alphabetical order
    grouped_df = df.groupby('Dutch lexical unit')['Frame'].apply(lambda x: '%s' % ', '.join(x))
    
    #process frames
    frames_unprocessed = grouped_df.tolist() #creates list of strings where multiple frame names are part of the same string
    frames = [] #create empty list
    for entry in frames_unprocessed: #loop over list of strings
        list_strings = entry.split(', ') #split each string at the comma level and add to a list
        frames.append(list_strings) #append each list of strings to the complete list of frame names
        
    #process dutch_verbs
    dutch_units_unprocessed = df['Dutch lexical unit'].tolist() #create a list of all lexical units from the original, non-grouped df
    dutch_units_set = set(dutch_units_unprocessed) #turn the list into a set so that there is only one entry for each lexical unit
    dutch_units_list = list(dutch_units_set) #turn the set back into a list
    dutch_units = sorted(dutch_units_list) #place the lexical units in alphabetical order in order to correspond with the frame name ordering
    
    dictionary_nlindex = dict(zip(dutch_units, frames)) #create a dictionary where keys are dutch lexical units and values are lists of frame names. 
    
    return(dictionary_nlindex) #return the dictionary
    
    
def match_verbs_find_frames(path_to_events_pos, dictionary_nlIndex):
    """
    Searches through the modern dutch translations in events_pos, finds matching dutch verbs in the keys of a dictionary and adds a column of the corresponding frames (values in the dictionary) from the nl-luIndex to the events_pos document.
    :param path_to_events_pos: str
    :dictionary_nlIndex: dict
    """

    df_events_pos = pd.read_excel(path_to_events_pos, engine='odf')
       
    list_corresponding_frames = []
    for index, row in df_events_pos.iterrows(): #loop through events_pos df
        if row['Modern Dutch translation (inf.)'] in dictionary_nlIndex.keys(): #if match between modern dutch translation and lexical unit 
            frame_collection = dictionary_nlIndex[row['Modern Dutch translation (inf.)']] #then the value of the key that is the same as the modern dutch translation is the list of corresponding frames
            list_corresponding_frames.append(frame_collection) #add the list of corresponding frames to a list
        else:
            list_corresponding_frames.append('none') #if there is no match, add a zero to the list.
      
    df_events_pos['nl-luIndex_frame'] = list_corresponding_frames #add the resulting list as a column to the events_pos df
    
    return(df_events_pos)


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

def match_to_predicate_matrix(extracted_info, df_with_nllu):
    """
    matches modern Dutch translations with Dutch predicates from the predicate matrix and gathers corresponding frames in new column in the events_pos dataframe.
    Returns the events_pos dataframe with a column of corresponding frames from the predicate matrix
    
    :param extracted_info: list of lists
    :param path_to_events_pos: str
    """

    modern_d = df_with_nllu['Modern Dutch translation (inf.)'].tolist() #gather modern dutch translations in a list
    
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
        
    df_with_nllu['predicate_matrix_frame'] = matched_frames #add a column to the events_pos file with the matched and processed frames
    return(df_with_nllu)
    

# match with nl-luIndex       
path_to_xml = '../data/nl-luIndex.xml'
path_to_events_pos = '../data/events_pos_devset.ods'
path_to_predicate_matrix = '../data/PredicateMatrix.v1.3.txt.role.odwn'

dictionary_nlIndex = xml_to_dict(path_to_xml)
df_with_nllu = match_verbs_find_frames(path_to_events_pos, dictionary_nlIndex)
    
# match with predicate matrix    
list_lines = read_pm(path_to_predicate_matrix)
extracted_synsets_and_frames = extract_predicates_and_frames(list_lines)
df_with_frames = match_to_predicate_matrix(extracted_synsets_and_frames, df_with_nllu)

# make a column that shows which frames were matched with the modern Dutch translations both in the nllu index and the predicate matrix
df_with_frames['frames_that_appear_in_both'] = [(set(a).intersection(b)) for a, b in zip(df_with_frames['nl-luIndex_frame'], df_with_frames['predicate_matrix_frame'])]

df_with_frames.to_excel('../data/test_frames.xlsx', index=False)




 

    

