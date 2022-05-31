# nlp-event-extraction
This repository contains the pilot code for automatic event extraction. It is a work in progress.
Currently, there is code that extracts English frames that correspond to modern Dutch translations of predicates taken from the General Letters from two datasets: the nl-luIndex and the predicate matrix. 

## data
### events_pos.xlsx
An excel file with in each row a predicate extracted from the General Letters, the number of occurences and associated lemma's taken from a lexicon made for OCR and OCR-postcorrection, for the period from 1550 - to around 1970 (https://taalmaterialen.ivdnt.org/download/tstc-int-historische-woordenlijst/). The lemma's are provided with their POS-tags. 

### events_pos_filter_VRB_ordered_frequency_over_1.ods
This is a filtered version of the events_pos file. It contains only those predicates that were associated with a lemma from the OCR lexicon with a VRB POS-tag and it is ordered according to the frequency of occurence of the predicates.

### events_pos_devset.ods
This is a subset of events_pos_filter_VRB_ordered_frequency_over_1.ods: it represents the top 150 most ocurring predicates, provided with a modern Dutch translation. The translations were gathered by looking at the associated lemma that was labeled as a verb for each predicate and looking up its meaning in the Woordenboek der Nederlandsche Taal (WNT), which is a historical and scientific dictionary of the Dutch from 1500-1976 (https://gtb.ivdnt.org/search/#).

### nl-luIndex.xml
An xml file containing Dutch predicates (lexical units) and their corresponding English frames.

### PredicateMatrix.v1.3.txt.role.odwn.gz
A .txt file containing Dutch predicates (synsets) and their corresponding English frames. In order to run the code, you need to unzip this file to a .txt.role.odwn file.

### devset_with_frames.xlsx
The outfile of find_english_frame_matches.py

### relevant frame selection
This folder contains one input file: relevant_predicates_pilot_df.ods, which is a subset of events_pos_filter_VRB_ordered_frequency_over_1.ods, where only those predicates that occurred between 5 and 15 times were selected, and the predicates that seemed relevant for either ship movement or authority were provided with a modern Dutch translation (one column for ship movement translations an another column for authority translations). 
The rest of the files in this folder are output files: ship_movement_frames.xlsx and authority_frames.xlsx contain those predicates that were selected as relevant with the matching frames from the nl_luIndex and the predicate matrix. unique_frames_ships.txt and unique_frames_authority.txt are lists of the frames that were matched with the relevant predicates. 

## find_english_frame_matches.py
This code matches modern Dutch translations of verbs in the events_pos_devset file to frames in the nl-luIndex and the predicate matrix
It first matches with the nl-luIndex and then with the predicate matrix. 
This version of the code takes a subset of the events_pos file (events_pos_devset)
Returns events_pos_devset as an excel file with three new columns
- English frames from the nl-luIndex that match the modern Dutch translation
- Enlgish frames from the predicate matrix that match the modern Dutch translation
- frames that were a match with the modern Dutch translation both in the nl-luIndex and the predicate matrix

## get_relevant_frames.py
This code matches the predicates in relevant_predicates_pilot_df.ods to frames in the nl-luIndex and the predicate matrix. 

## find_english_frame_matches2.py
contains the functions used by get_relevant_frames.py. The functions are based on those in find_english_frame_matches but differ in the fact that they deal with mpodern Dutch translations in different columns and multiple translations per column. 
