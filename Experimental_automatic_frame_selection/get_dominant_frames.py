"""
Input: 
- ship_movement_frames.xlsx
- authority_frames.xlsx

Output:
Overview of dominant frames from both files. Frames are dominant when they occur more than 3 times.
"""

import pandas as pd
from ast import literal_eval
from collections import Counter


def read_excel(filepath):
    df = pd.read_excel(filepath)
    return(df)

def get_frames(df, rowname):
    
    all_frames = []
    frames = df[rowname].tolist()
    for item in frames:
        l = literal_eval(item)
        for frame in l:
            all_frames.append(frame)
            
    return(all_frames)


def count_frames(luFrames, pmFrames):
    
    all_frames = luFrames + pmFrames
    counted_dict = Counter(all_frames)
    return(counted_dict)


df = read_excel('data/relevant frame selection/ship_movement_frames.xlsx')
luFrames = get_frames(df, 'nl-luIndex_frame')
pmFrames = get_frames(df, 'predicate_matrix_frame')

counted_dict = count_frames(luFrames, pmFrames)
print(counted_dict)

