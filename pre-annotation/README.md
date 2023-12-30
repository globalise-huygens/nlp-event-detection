# Pre-annotation
This code 
1. converts XMI 1.0 files extracted from INCEpTION to .json files with code that is an adaptation of code by Sophie Arnoult
2. pre-annotates event mentions with a lexicon
3. converts the pre-annotated .json files back to .xmi files to be uploaded in INCEpTION, again with code that is an adaptation of code by Sophie Arnoult

This repository works with five files that have been selected for annotation in 2024.

### Executing step 1
In cas2json_events.py, comment out the last two lines, uncomment the line <#cas2json_zip("data/", "data/jsonfiles.zip")> and run the .py file. The converted .json documents will be stored in *data/jsonfiles.zip*. 

### Executing step 2
Unzip and put the files you just converted to .json in the *data/* folder. Run add_dictionary_annotations.py. .json files with lexion pre-annotations will be stored in *data/predictions/*

### Executing step 3
In cas2json_events.py, comment out the command you used for step 1 and uncomment the last two lines. Run the .py file. The converted .xmi documents will be stored in *data/pre-annotated*
