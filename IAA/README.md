# Inter-Annotator Agreement Analysis 
## Overview 
This is code written to analyse the annotations on event classes made in the GLOBALISE Annotation Pilot 2 (2022).
Note: this code does not analyse agreement among event argument annotations.
The document that was annotated by all four annotators active at the time was NL-HaNA_1.04.02_1092_0017_0021 (VOC archive = 1.04.02; inventory number = 1092; scans 17 to 21).
See the first original scan [here](https://www.nationaalarchief.nl/onderzoeken/archief/1.04.02/invnr/1092/file/NL-HaNA_1.04.02_1092_0017)

## Data
The data provided with the code that is needed to run it are four documents exported from Inception, each document represents the same scans but is annotated by a different annotator.

## Use
Running IAA_analysis.py will print a complete report on Inter-Annotator Agreement. Also, it writes disagreements that were not automatically resolved to .tsv files. Outputted files:
- in ./individual_data/processed Inception output but without full sentences in tsv format for each annotator
- in ./individual_data/processed Inception output (each row represents one annotated event) for each annotator in tsv format
- in ./individual_data/processed Inception output (each row represents one annotated event) for each annotator in json format
- in ./individual_data/unresolved_disagreements: all disagreements that should be solved manually (two files)
- in ./team_data/processed Inception output but without full sentences in tsv format for each annotator
- in ./team_data/processed Inception output (each row represents one annotated event) for each annotator in tsv format
- in ./team_data/processed Inception output (each row represents one annotated event) for each annotator in json format
These files will be used to resolve the problematic disagreements amongst all annotators, creating a reliable test set for a Event Trigger Classification system. 
IAA_analysis.py uses files processed by process_inception_output.py.

For more information on how IAA was analyzed, see [this report](https://docs.google.com/document/d/1MwkARk0_K2c8tQIeM1eLbb6N5QwhUhEQb1zJAzxe1Lw/edit?usp=sharing)
For more information on how the test set was created, see [this report](https://docs.google.com/document/d/1yMQXSOlToAFLvL4NFlZkI-O37MUIz-Msvqme0MMq3w0/edit?usp=sharing)

## Requirements
pandas == 2.0.3


