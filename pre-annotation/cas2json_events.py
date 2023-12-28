from cassis import *
import click
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
        return f"B-event"

    @classmethod
    def midword(cls, label):
        return f"I-event"


def get_tokens_and_labels(sentence, cas):
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


def cas2jsonl_ner(cas, jsonl):
    with open(jsonl, 'w') as f:
        for sentence in cas.select(SENTENCE):
            tokens, labels = get_tokens_and_labels(sentence, cas)
            json.dump({'words': tokens, 'events': labels}, f)
            f.write("\n")


def cas2json_zip(datadir, json_zip_path):
    """converts xmi files from an Inception export (prealably unzipped) into json"""
    with z.ZipFile(os.path.join(datadir, 'json.zip'), 'w') as ozf:
        for doc_folder in os.listdir(os.path.join(datadir, 'firstfive')):
            with open(os.path.join(datadir, 'firstfive', doc_folder, TYPESYSTEM), 'rb') as f:
                typesystem = load_typesystem(f)
            with open(os.path.join(datadir, 'firstfive', doc_folder, str(doc_folder) + ".xmi"), 'rb') as f:
                cas = load_cas_from_xmi(f, typesystem=typesystem)
            json_path = os.path.basename(doc_folder).split()[0]
            cas2jsonl_ner(cas, json_path)
            ozf.write(json_path)
    print(f"converted {len(z.ZipFile(json_zip_path).namelist())} files")


def json2cas_zip(json_path, casdir, doc_folder, prediction_dir="predicted/with_types"):
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
    with open(os.path.join(casdir, 'firstfive', doc_folder, TYPESYSTEM), 'rb') as f:
        typesystem = load_typesystem(f)
    with open(os.path.join(casdir, 'firstfive', doc_folder, str(doc_folder) + ".xmi"), 'rb') as f:
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
        for e in cas.select(NAMED_ENTITY):
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
            cas.add(Event(begin=start, end=end, category=val))
            recording = True
    if recording:
        try:
            cas.add(Event(begin=start, end=end, category=val))
        except UnboundLocalError:
            y = 0

@click.command()
@click.option('--json2cas/--cas2json', default=False, help="add predicted entities to xmi files (default: cas2json)")
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.Path(exists=False))
def cli(json2cas, input, output):
    """Extracts json files of tokens and entities from an inception directory,
    or adds entities from json files to inception xmi files.

    INPUT: inception directory or json file path if JSON2CAS is set\n
    OUTPUT: zip of json files or reference/output inception directory if JSON2CAS is set"""
    if json2cas:
        json2cas_zip(input, output)
    else:
        cas2json_zip(input, output)


# if __name__ == '__main__':
#     cli()

#filenames = ['NL-HaNA_1-8.json','NL-HaNA_1-9.json', 'NL-HaNA_1-10.json', 'NL-HaNA_1.04.02_3598_0797-0809.json', 'NL-HaNA_1.04.02_11012_0229-0251.json']



#cas2json_zip("annotations/to_annotate_2024/", "data/dummy.zip")
json2cas_zip("predictions/to_annotate_2024/with_types/type-pre_annotate-NL-HaNA_1-10.json", 'annotations/to_annotate_2024/', 'NL-HaNA_1-10')