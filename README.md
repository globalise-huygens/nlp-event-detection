# nlp-event-detection
This repository contains code for several aspects of the automatic event detection pipeline. It mostly contains code to process our data in different ways in order to prepare it for different experiments. It also contains some (documentation of) preliminary, small experiments mainly used for orientation. This repo still gets changed and updated. There are several seperate repos that contain finished experiments or modules of the pipeline, namely:
- repo for our [lexical approach to event detection](https://github.com/globalise-huygens/nlp-event-lexical-approach)
- repo for our [paper on annotation strategies](https://github.com/StellaVerkijk/VarDial2024)
- repo introducing our [cross-validation on document-level approach](https://github.com/globalise-huygens/nlp-event-testset-experiment)
- repo for [building and evaluating binary event detection models](https://github.com/globalise-huygens/nlp-binary-event-detection-models)

Each (important) folder in this repo has their own README for further information. 

## annotated_data_processing_for_IAA
Probably the most important folder here; contains code to process data outputted from INCEpTION in cas_xmi to different file formats for different tasks. Currently: json for event detection and event classification and conllu for semantic role labelling.

## pre-annotation
Converts files exported from INCEpTION in XMI 1.0 to json and back with adapted code by Sophie Arnoult and pre-annotates using a lexicon.

## IAA / annotated_data_processing_for_IAA
In this folder code and data is stored to perform an IAA analysis on event mention detection and classification. For a more documented overview of our IAA data and analysis see our seperate repo on this.
annotated_data_processing_for_IAA also contains data and information on how we adjudicate our annotated data to create test data.

## preliminary_experiments
Contains thoroughly documented experiments performed in the orientation phase of establishing our annotation strategy. 

## built_resources
Contains several versions of a simple version of our event ontology in turtle format

## baselines
Contains some results of an orientation phase in finetuning models on binary event detection





