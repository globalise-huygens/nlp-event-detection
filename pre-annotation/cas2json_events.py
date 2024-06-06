from cassis import *
import os
from enum import Enum
import itertools
import json
import zipfile as z
import re

TYPESYSTEM = "TypeSystem.xml"
TRAIN = "*.xmi"
SENTENCE = "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Sentence"
TOKEN = "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token"
NAMED_ENTITY = "de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity"
EVENT = "webanno.custom.SemPredGLOB"
SEM_ARG = "de.tudarmstadt.ukp.dkpro.core.api.semantics.type.SemArg"


class BIO(Enum):
    O = "O"
    B = "B"
    I = "I"

    @classmethod
    def begin(cls, label):
        #return f"B-event"
        return "B-"+str(label)

    @classmethod
    def midword(cls, label):
        #return f"I-event"
        return "I-"+str(label)

def get_tokens_and_labels_events(sentence, cas):
    tokens = cas.select_covered(TOKEN, sentence)
    events = cas.select_covered(EVENT, sentence)
    entities = cas.select_covered(NAMED_ENTITY, sentence)
    labels = []
    i = 0
    for e in events:
        while i < len(tokens) and tokens[i].begin < e.begin:
            labels.append(BIO.O.value)
            i += 1
        labels.append(BIO.begin(e.category)) #was e.value for ner
        i += 1
        while i < len(tokens) and tokens[i].end <= e.end:
            labels.append(BIO.midword(e.category)) #was e.value for ner
            i += 1
    labels.extend(list(itertools.chain.from_iterable(itertools.repeat(BIO.O.value, len(tokens) - i))))
    return list(map(lambda x: x.get_covered_text(), tokens)), labels

def get_tokens_and_labels(sentence, cas):
    tokens = cas.select_covered(TOKEN, sentence)
    events = cas.select_covered(EVENT, sentence)
    entities = cas.select_covered(NAMED_ENTITY, sentence)
    labels = []
    i = 0
    for e in entities:
        while i < len(tokens) and tokens[i].begin < e.begin:
            labels.append(BIO.O.value)
            i += 1
        labels.append(BIO.begin(e.value)) #was e.value for ner
        i += 1
        while i < len(tokens) and tokens[i].end <= e.end:
            labels.append(BIO.midword(e.value)) #was e.value for ner
            i += 1
    labels.extend(list(itertools.chain.from_iterable(itertools.repeat(BIO.O.value, len(tokens) - i))))
    return list(map(lambda x: x.get_covered_text(), tokens)), labels


def cas2jsonl_ner(cas, jsonl):
    with open(jsonl, 'w') as f:
        for sentence in cas.select(SENTENCE):
            tokens, labels = get_tokens_and_labels(sentence, cas)
            json.dump({'words': tokens, 'ner': labels}, f)
            f.write("\n")

def cas2json_zip(datadir, json_zip_path):
    """converts xmi files from an Inception export (preferably unzipped) into json"""
    with z.ZipFile(os.path.join(datadir, 'jsonfiles.zip'), 'w') as ozf:
        for doc_folder in os.listdir(os.path.join(datadir, 'input_for_lexicon_v2/xmi')):
            with open(os.path.join(datadir, 'input_for_lexicon_v2/xmi', doc_folder, TYPESYSTEM), 'rb') as f:
                typesystem = load_typesystem(f)
            with open(os.path.join(datadir, 'input_for_lexicon_v2/xmi', doc_folder, str(doc_folder) + ".xmi"), 'rb') as f:
                cas = load_cas_from_xmi(f, typesystem=typesystem)
            json_path = os.path.basename(doc_folder).split()[0] +'.json'
            cas2jsonl_ner(cas, json_path)
            ozf.write(json_path)
    print(f"converted {len(z.ZipFile(json_zip_path).namelist())} files")


def json2cas_zip(json_path, casdir, doc_folder, prediction_dir="pre-annotated"):
    """Copies curated xmi files from the 'curation' folder of CASDIR to a PREDICTION_DIR subfolder of CASDIR,
    replacing entities with those found at JSON_PATH.

    #json_path = file with predictions
    #casdir = inception output without predictions = oct23
    #prediction_dir = outfile

    The documents in JSON_PATH are concatenated and assumed to correspond in order to those of 'curation'"""
    # fix for whitespace tokens in annotations xmi
    pattern = re.compile(" +")

    #doc_folders = sorted(os.listdir(os.path.join(casdir, 'firstfive')))
    os.makedirs(os.path.join(casdir, prediction_dir), exist_ok=True)
    with open(json_path) as f:
        json_lines = f.readlines()
    json_line_offset = 0
    #for doc_folder in doc_folders:
    with open(os.path.join(casdir, 'data_inception_output', doc_folder, TYPESYSTEM), 'rb') as f:
        typesystem = load_typesystem(f)
    with open(os.path.join(casdir, 'data_inception_output', doc_folder, str(doc_folder) + ".xmi"), 'rb') as f:
        cas = load_cas_from_xmi(f, typesystem=typesystem)
        nb_sentences = len(cas.select(SENTENCE))
        event_tags = []
        for line in json_lines[json_line_offset:json_line_offset + nb_sentences]:
            jdic = json.loads(line)
            #event_tags.extend(jdic["ner"])
            event_tags.extend(jdic["preds"])
        # Remove event tags already present
        for e in cas.select(EVENT):
            cas.remove(e)
        # Remove entity tags already present
        for e in cas.select(NAMED_ENTITY): # DO NOT USE THIS LINE AND THE FOLLOWING IF YOU ARE PRE-ANNOTATING A FILE PRE-ANNOTATED WITH ENTITIES ALREADY
            cas.remove(e)
        # Remove SemArg for cleaner look
        for e in cas.select(SEM_ARG):
            cas.remove(e)

        # filter out whitespace tokens
        tokens = [t for t in cas.select(TOKEN) if not re.match(pattern, t.get_covered_text())]
        compress_BIO_tags(event_tags, tokens, cas, typesystem)
        cas.to_xmi(os.path.join(casdir, prediction_dir, f"{doc_folder}.xmi"))
        json_line_offset += nb_sentences


def compress_BIO_tags(entity_bio_tags, tokens, cas, typesystem, treat_I_init_as_B=True):
    recording = True #True for pre-annotation
    current_type = "X"
    #NamedEntity = typesystem.get_type(NAMED_ENTITY)
    Event = typesystem.get_type(EVENT) # this one for pre-anno
    #entity_tokens = [(bio, token) for (bio, token) in zip(entity_bio_tags, tokens) if bio != "O"]
    event_tokens = [(bio, token) for (bio, token) in zip(entity_bio_tags, tokens) if bio != "O"]
    for bio, token in event_tokens:
        val = bio.split('-')[1]
        relation = bio.split('-')[2]
        is_start = bio.startswith('B')
        maybe_start = bio.startswith('I') and treat_I_init_as_B and val != current_type
        maybe_last = not bio.startswith('O')
        follows_last = not bio.startswith('I') and recording
        if is_start or maybe_start:
            start = token.begin
            current_type = val
            recording = True # True for pre-annotation
        if maybe_last:
            end = token.end
        if follows_last:
            cas.add(Event(begin=start, end=end, category=val, relationtype=relation))
            recording = True
    if recording:
        try:
            cas.add(Event(begin=start, end=end, category=val, relationtype=relation))
        except UnboundLocalError:
            y = 0



filenames_readme = ['NL-HaNA_1-8','NL-HaNA_1-9', 'NL-HaNA_1-10', 'NL-HaNA_1.04.02_3598_0797-0809', 'NL-HaNA_1.04.02_11012_0229-0251']


#cas2json_zip("data/", "data/jsonfiles.zip")

#for file in filenames:
    #json2cas_zip("data/predictions/rel-pre_annotate-"+file+'.json', 'data/', file)



###### June 2024

filenames_june2024 = ['data/globalise-xmi-2024-05-31-ner/NL-HaNA_1.04.02_8596_0761-0766.xmi']

for filename in filenames_june2024:
    with open('data/globalise-xmi-2024-05-31-ner/TypeSystem.xml', 'rb') as f:
        typesystem = load_typesystem(f)
    with open(filename, 'rb') as f:
        cas = load_cas_from_xmi(f, typesystem=typesystem)
    json_path = 'data/globalise-xmi-2024-05-31-ner/globalise-xmi-2024-06-03-ner-events/NL-HaNA_1.04.02_8596_0761-0766.json'
    cas2jsonl_ner(cas, json_path)


pattern = re.compile(" +")
filenames_june2024_json = ['data/pre-annotated_june2024/json/preannotated-NL-HaNA_1.04.02_8596_0761-0766.json']
for file in filenames_june2024_json:
    with open(file) as f:
        json_lines = f.readlines()
    json_line_offset = 0
    with open('data/globalise-xmi-2024-05-31-ner/TypeSystem.xml', 'rb') as f:
        typesystem = load_typesystem(f)
    with open('data/globalise-xmi-2024-05-31-ner/NL-HaNA_1.04.02_8596_0761-0766.xmi', 'rb') as f:
        cas = load_cas_from_xmi(f, typesystem=typesystem)
        nb_sentences = len(cas.select(SENTENCE))
        event_tags = []
        for line in json_lines[json_line_offset:json_line_offset + nb_sentences]:
            jdic = json.loads(line)
            #event_tags.extend(jdic["ner"])
            event_tags.extend(jdic["events"])

        # filter out whitespace tokens
        tokens = [t for t in cas.select(TOKEN) if not re.match(pattern, t.get_covered_text())]
        compress_BIO_tags(event_tags, tokens, cas, typesystem)
        cas.to_xmi('data/pre-annotated_june2024/preannotated-NL-HaNA_1.04.02_8596_0761-0766.xmi')
        json_line_offset += nb_sentences

