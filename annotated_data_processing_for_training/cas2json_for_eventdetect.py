"""
@StellaVerkijk
Adaptation of original code by Sophie Arnoult
"""

from cassis import *
from enum import Enum
import itertools
import json
import pathlib

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
        #return f"B-event"          # for binary mention detection
        #return "B-"+str(label)     # for BIO classification
        return str(label)           # for IO classification

    @classmethod
    def midword(cls, label):
        #return f"I-event"
        #return "I-"+str(label)
        return str(label)

def get_tokens_and_labels_events(sentence, cas):
    tokens = cas.select_covered(TOKEN, sentence)
    events = cas.select_covered(EVENT, sentence)

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


def cas2jsonl(cas, jsonl):
    with open(jsonl, 'w') as f:
        for sentence in cas.select(SENTENCE):
            tokens, labels = get_tokens_and_labels_events(sentence, cas)
            json.dump({'words': tokens, 'events': labels}, f)
            f.write("\n")


def get_json_data(input_path):

    folder = pathlib.Path(input_path)
    filenames = list(folder.glob("*.xmi"))


    file_id = 0
    for filename in filenames:
        print(filename)
        file_id +=1
        with open('TypeSystem.xml', 'rb') as f:
            typesystem = load_typesystem(f)
        with open(filename, 'rb') as f:
            cas = load_cas_from_xmi(f, typesystem=typesystem)
        json_path = 'json_per_doc_class_IO/'+str(filename)[:-4]+'.json'
        cas2jsonl(cas, json_path)

def main():
    get_json_data("train/train_5")

if __name__ == '__main__':
    main()

