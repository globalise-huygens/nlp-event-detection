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
#SEM_ARG = "webanno.custom.SemPredGLOBArgumentsLink"


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

def get_tokens_and_labels(sentence, cas):
    tokens = cas.select_covered(TOKEN, sentence)
    events = cas.select_covered(EVENT, sentence)
    entities = cas.select_covered(NAMED_ENTITY, sentence)
    arguments = cas.select_covered(SEM_ARG, sentence)
    event_labels = []
    ignition_labels = []
    argument_labels = []
    i = 0
    for e in events:
        while i < len(tokens) and tokens[i].begin < e.begin:
            ignition_labels.append(BIO.O.value)
            event_labels.append(BIO.O.value)
            i += 1
        ignition_labels.append(BIO.begin(e.relationtype))
        event_labels.append(BIO.begin(e.category))#was e.value for ner; e.category for events
        i += 1
        while i < len(tokens) and tokens[i].end <= e.end:
            ignition_labels.append(BIO.midword(e.relationtype)) #was e.value for ner; e.category for events
            event_labels.append(BIO.midword(e.category))
            i += 1
    i = 0
    for a in arguments:
        while i < len(tokens) and tokens[i].begin < a.begin:
            argument_labels.append(BIO.O.value)
            i += 1
        argument_labels.append(BIO.begin('arg'))
        i += 1
        while i < len(tokens) and tokens[i].end <= a.end:
            argument_labels.append(BIO.midword('arg'))
            i += 1
    ignition_labels.extend(list(itertools.chain.from_iterable(itertools.repeat(BIO.O.value, len(tokens) - i))))
    event_labels.extend(list(itertools.chain.from_iterable(itertools.repeat(BIO.O.value, len(tokens) - i))))
    argument_labels.extend(list(itertools.chain.from_iterable(itertools.repeat(BIO.O.value, len(tokens) - i))))
    return list(map(lambda x: x.get_covered_text(), tokens)), ignition_labels, event_labels, argument_labels



def cas2jsonl_combined(cas, jsonl):
    with open(jsonl, 'w') as f:
        for sentence in cas.select(SENTENCE):
            tokens, ignition_labels, event_labels, argument_labels = get_tokens_and_labels(sentence, cas)
            json.dump({'words': tokens, 'ignition': ignition_labels, 'events': event_labels, 'arguments': argument_labels}, f)
            f.write("\n")


def cas2json_args(datadir):
    """converts xmi files from an Inception export into json with arguments"""
    with z.ZipFile('team_data_2024/jsonfiles.zip', 'w') as ozf:
        for doc_folder in os.listdir(datadir):
            with open(os.path.join(datadir, doc_folder, TYPESYSTEM), 'rb') as f:
                typesystem = load_typesystem(f)
            with open(os.path.join(datadir, doc_folder, str(doc_folder) + ".xmi"), 'rb') as f:
                cas = load_cas_from_xmi(f, typesystem=typesystem)
            json_path = os.path.basename(doc_folder).split()[0] + '.json'
            cas2jsonl_combined(cas, json_path)
            ozf.write(json_path)
    print(f"converted {len(z.ZipFile('team_data_2024/jsonfiles.zip').namelist())} files")


#cas2json_args("team_data_2024/cas")

dict1 = {"words": ["De", "heer", "Kommandeur", "van", "Angelbeek", "heeft", "ons", "Wel", "seshonderd", "lasten", "rijst", "toegezegd", ",", "doch", "dezelve", "moeten", "in", "de", "aanstaande", "maand", "April", "Worden", "afgehaald", ",", "Wijl", "ner", "laater", "geen", "schip", "op", "de", "koettjiensche", "rheede", "durf", "vertrouwen", ",", "en", "daar", "toe", "zien", "wij", "geen", "mogelijkheid", ",", "Vermits", "wij", "geen", "scheepen", "tot", "den", "afhaal", "aan", "harden"], "ignition": ["O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-evokes", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-isOfType", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-evokes", "O", "O", "O", "O", "O"], "events": ["O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-Giving", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-Transportation", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-Transportation", "O", "O", "O", "O", "O"], "arguments": ["B-arg", "I-arg", "I-arg", "I-arg", "I-arg", "O", "B-arg", "O", "B-arg", "I-arg", "I-arg", "O", "O", "O", "O", "O", "O", "B-arg", "I-arg", "I-arg", "I-arg", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-arg", "O", "B-arg", "O", "O", "O", "O", "O"]}

dict = {"words": ["hebben", "en", "Wanneer", "Wij", "dezelve", "ook", "hadden", ",", "zonden", "ze", "dog", "zonder", "een", "goed", "konvooij", "niet", "gewaagd", "Worden", ",", "Wijl", "de", "Bombaijsche", "fregatten", "nog", "bestendig", "op", "de", "hoogte", "van", "koetsjien", "kruissen", ".", "Wat", "er", "te", "gen", "de", "opere", "Vaart", "/", ":", "die", "niet", "Voor", "half", "Oktober", "gerekend", "mag", "Worden:/", "op", "Mallabaar", "Voorvallen", "kan", ",", "mogen", "wij", "niet", "gissen", ",", "en", "zoo", "Wij", "deeze", "zelkonder-", "lasten", "Mallabaers", "rijst", "kreegen", ",", "bij", "de", "geeischte", "Javasche", ",", "zoude", "onze", "Voorraad", "naar", "maatig", "zijn", ",", "Wijl", "de", "Fransche", "Vloot", "zeken", "on", "rijst", "zal", "vraagen", ",", "en", "de", "gemeente", "geen", "aanvoer", "uit", "Boengaale", "hoopen", "kan", ".", "Om", "deeze", "reedenen", "verzoeken", "Wij", "Uwe", "Hoog", "Edelheeden", "nogmaals", "op", "het", "ootmoedigste", ",", "om", "onzer", "voormelden", "Eisch", "kompleet", "te", "Willen", "voldoen", ",", "Wijl", "wij", "andersints", "in", "een", "indoorkonelijke", "Verleegerheid", "zouden", "VerVallen", ".", "Een", "schip", "Voor", "Gale", "en", "een", "Voor", "Kolombo", ",", "zouden", "in", "Juri", "dienen", "te", "Vertrekken", ",", "om", "tijding", "in", "Augustus", "hier", "te", "weezen", "zij", "komen", "bewesten", "de", "Maldivos", "en", "mag", "de", "reize", "dus", "op", "niet", "minder", "dan", "twee", "maanden", "bereekend", "Worden", ".", "Wanneer", "UWe", "Hoogedelheeden", ",", "gelijk", "doorgaans", ",", "groote", "scheepen", "tot", "deezer", "togt", "uit", "kiezen", ",", "zal", "nog", "een", "derde", "niet", "alleen", "de", "gevraagde", "rijst", ",", "maar", "ook", "de", "overige", "goederen", "kunnen", "mede", "neemen", ",", "Vermits", "wij", "zo", "lang", "de", "oorlog", "duurt", ",", "op", "geen", "onderlaag", "voor", "de", "retourscheepen", "denken", "mogen", ".", "Wij", "verzoeken", "dan", ",", "dat", "ook", "dit", "derde", "schip", "de", "twee", "anderen", "spoedig", "volge", ",", "op", "dat", "het", "in", "september", "hier", "zij", ",", "Voor", "dat", "de", "goede", "Moesson", "Vijandelijke", "kruissers", "na", "deezer", "kant", "doe", "Verschijnen", ",", "en", "dat", "alle", "drie", "scheepen", "last", "krijgen", "om", "de", "Mallabaarsche", "kust", ",", "na", "dat", "zij", "het", "karaal", "tusschen", "de", "Maldivos", "en", "LakkeriVes", "doorgevaaren", "zijn", ",", "op", "eene", "voorzigtige", "Wijze", "te", "Verkennen", ",", "en", "na", "\u201e"], "ignition": ["O", "O", "O", "O", "O", "O", "B-isOfType", "O", "O", "O", "O", "O", "O", "O", "B-evokes", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-isOfType", "O", "O", "O", "O", "O", "O", "O", "B-isOfType", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-isOfType", "O", "O", "O", "B-isOfType", "O", "O", "O", "O", "B-evokes", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-isOfType", "O", "O", "O", "O", "O", "B-isOfType", "O", "O", "O", "O", "O", "O", "O", "O", "B-isOfType", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-evokes", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-evokes", "I-evokes", "I-evokes", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-isOfType", "B-isOfType", "O", "O", "O", "O", "O", "B-isOfType", "I-isOfType", "O", "B-isOfType", "O", "O", "O", "O", "O", "O", "B-isOfType", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-isOfType", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-isOfType", "O", "O", "O", "O", "O", "O", "O", "O", "B-isOfType", "I-isOfType", "O", "O", "O", "O", "O", "O", "B-isOfType", "O", "O", "O", "O", "B-isOfType", "O", "O", "B-evokes", "O", "O", "O", "O", "B-isOfType", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-evokes", "B-evokes", "O", "O", "O", "O", "O", "B-isOfType", "I-isOfType", "O", "O", "O", "O", "O", "O", "B-evokes", "O", "O", "O", "O", "O", "B-isOfType", "O", "O", "O", "O", "O", "O", "B-isOfType", "I-isOfType", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-isOfType", "O", "O", "O", "O", "O", "O", "O", "B-evokes", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"], "events": ["O", "O", "O", "O", "O", "O", "B-HavingInPossession", "O", "O", "O", "O", "O", "O", "O", "B-Translocation", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-BeingAtAPlace", "O", "O", "O", "O", "O", "O", "O", "B-Voyage", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-Getting", "O", "O", "O", "B-Request", "O", "O", "O", "O", "B-HavingInPossession", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-Request", "O", "O", "O", "O", "O", "B-Transportation", "O", "O", "O", "O", "O", "O", "O", "O", "B-Request", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-Request", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-SocialStatusChange", "I-SocialStatusChange", "I-SocialStatusChange", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-Leaving", "B-Leaving", "O", "O", "O", "O", "O", "B-BeingAtAPlace", "I-BeingAtAPlace", "O", "B-Arriving", "O", "O", "O", "O", "O", "O", "B-Voyage", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-Voyage", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-Request", "O", "O", "O", "O", "O", "O", "O", "O", "B-Transportation", "I-Transportation", "O", "O", "O", "O", "O", "O", "B-BeingInConflict", "O", "O", "O", "O", "B-BeingDestroyed", "O", "O", "B-Voyage", "O", "O", "O", "O", "B-Request", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-Translocation", "B-Translocation", "O", "O", "O", "O", "O", "B-BeingAtAPlace", "I-BeingAtAPlace", "O", "O", "O", "O", "O", "O", "B-BeingInConflict", "O", "O", "O", "O", "O", "B-Arriving", "O", "O", "O", "O", "O", "O", "B-BeingInConflict", "I-BeingInConflict", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-Translocation", "O", "O", "O", "O", "O", "O", "O", "B-Voyage", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"], "arguments": ["O", "O", "B-arg", "B-arg", "B-arg", "O", "O", "O", "O", "B-arg", "O", "O", "O", "O", "B-arg", "O", "O", "O", "O", "O", "B-arg", "I-arg", "I-arg", "O", "O", "B-arg", "I-arg", "I-arg", "I-arg", "I-arg", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-arg", "O", "B-arg", "I-arg", "I-arg", "I-arg", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-arg", "I-arg", "I-arg", "O", "O", "O", "O", "O", "O", "O", "B-arg", "I-arg", "O", "O", "O", "B-arg", "O", "O", "O", "O", "O", "O", "O", "B-arg", "B-arg", "I-arg", "I-arg", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-arg", "O", "O", "O", "O", "O", "O", "O", "O", "B-arg", "I-arg", "B-arg", "I-arg", "B-arg", "B-arg", "I-arg", "I-arg", "B-arg", "O", "O", "B-arg", "O", "O", "O", "O", "O", "O", "O", "B-arg", "B-arg", "O", "O", "B-arg", "O", "B-arg", "I-arg", "I-arg", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-arg", "I-arg", "O", "O", "O", "O", "O", "O", "O", "O", "B-arg", "I-arg", "O", "O", "B-arg", "I-arg", "I-arg", "O", "O", "O", "B-arg", "I-arg", "I-arg", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-arg", "I-arg", "O", "O", "O", "B-arg", "O", "O", "O", "O", "O", "B-arg", "I-arg", "I-arg", "B-arg", "I-arg", "I-arg", "O", "O", "O", "O", "O", "O", "O", "B-arg", "B-arg", "O", "O", "O", "O", "O", "O", "O", "B-arg", "I-arg", "B-arg", "B-arg", "I-arg", "O", "O", "O", "O", "O", "B-arg", "I-arg", "I-arg", "O", "O", "B-arg", "I-arg", "I-arg", "I-arg", "O", "O", "O", "B-arg", "B-arg", "I-arg", "I-arg", "I-arg", "I-arg", "I-arg", "I-arg", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"]}


print(len(dict['words']))
print(len(dict['ignition']))
print(len(dict['events']))
print(len(dict['arguments']))

zipped = zip(dict['words'], dict['arguments'])
for item in zipped:
    print(item)

