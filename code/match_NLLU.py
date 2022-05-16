"""
Match modern Dutch translations of verbs in the events_pos file to frames in the nl-luIndex
This version of the code takes a subset of the events_pos file
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
        #only append the lexical unit, without '.v' or '.n' --> I am considering filtering out the '.n' ones. 
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
            list_corresponding_frames.append(0) #if there is no match, add a zero to the list.
    
    
    df_events_pos['nl-luIndex_frame'] = list_corresponding_frames #add the resulting list as a column to the events_pos df
    
    return(df_events_pos)
    
        
path_to_xml = 'data/nl-luIndex.xml'
path_to_events_pos = 'data/events_pos_development_set1.ods'

dictionary_nlIndex = xml_to_dict(path_to_xml)
df_with_frames = match_verbs_find_frames('data/events_pos_development_set1.ods', dictionary_nlIndex)

df_with_frames.to_excel('data/test_nllu.xlsx', index=False)

