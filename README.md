# nlp-event-extraction
This repository contains the pilot code for automatic event extraction. It is a work in progress.
Currently, there is code that extracts English frames that correspond to modern Dutch translations of predicates taken from the General Letters from two datasets: the nl-luIndex and the predicate matrix. 

## data
### events_pos
An excel file with in each row a predicate extracted from the General Letters, the number of occurences and associated lemma's taken from a lexicon made for OCR and OCR-postcorrection, for the period from 1550 - to around 1970 (https://taalmaterialen.ivdnt.org/download/tstc-int-historische-woordenlijst/). The lemma's are provided with their POS-tags. 

### events_pos_devset
This is a subset of a filtered version of the events_pos file. It contains only those predicates that were associated with a lemma from the OCR lexicon with a VRB POS-tag. events_pos_devset represents the top 150 most ocurring predicates, provided with a modern Dutch translation. The translations were gathered by looking at the associated lemma that was labeled as a verb for each predicate and looking up its meaning in the Woordenboek der Nederlandsche Taal (WNT), which is a historical and scientific dictionary of the Dutch from 1500-1976 (https://gtb.ivdnt.org/search/#).

### nl-luIndex
An xml file containing Dutch predicates (lexical units) and their corresponding English frames.

### PredicateMatrix.v1.3.txt.role.odwn.gz
A .txt file containing Dutch predicates (synsets) and their corresponding English frames. In order to run the code, you need to unzip this file to a .txt.role.odwn file.

### devset_with_frames
The outfile of find_english_frame_matches.py

## find_english_frame_matches.py
This code matches modern Dutch translations of verbs in the events_pos_devset file to frames in the nl-luIndex and the predicate matrix
It first matches with the nl-luIndex and then with the predicate matrix. 
This version of the code takes a subset of the events_pos file (events_pos_devset)
Returns events_pos_devset as an excel file with three new columns
- English frames from the nl-luIndex that match the modern Dutch translation
- Enlgish frames from the predicate matrix that match the modern Dutch translation
- frames that were a match with the modern Dutch translation both in the nl-luIndex and the predicate matrix

