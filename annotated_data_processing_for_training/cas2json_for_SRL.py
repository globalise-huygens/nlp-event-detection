"""
@StellaVerkijk
Adaptation of original code by Sophie Arnoult
"""

from cassis import *
from enum import Enum
import itertools
from utils import*
import pathlib
import random

TYPESYSTEM = "TypeSystem.xml"
TRAIN = "*.xmi"
SENTENCE = "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Sentence"
TOKEN = "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token"
EVENT = "webanno.custom.SemPredGLOB"
SEM_ARG = "de.tudarmstadt.ukp.dkpro.core.api.semantics.type.SemArg"
SEM_ARG_LINK = "webanno.custom.SemPredGLOBArgumentsLink"
NAMED_ENTITY = "de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity"


class BIO(Enum):
    O = "O"
    B = "B"
    I = "I"

    @classmethod
    def begin(cls, label):
        #return f"B-event"      # for binary mention detection
        return "B-"+str(label)  # for classification

    @classmethod
    def midword(cls, label):
        #return f"I-event"
        return "I-"+str(label)


def merge_lists(lists):
    """
    ChatGPT was used for this function
    :param lists: list of lists , each sublist list has to be of the same length but list of lists can be of any length
    :return: one list with merged elements
    """
    # Assuming all lists are of the same length
    merged_list = []

    # Iterate through each group of elements from all lists
    for elements in zip(*lists):
        # Find the first non-'O' element or return 'O' if all are 'O'
        merged_list.append(next((e for e in elements if e != 'O'), 'O'))

    return merged_list

def get_data_per_event(sentence, cas, with_entities=False):
    """
    Inputs a text region and outputs a list of dictionaries. Each dictionary represents the text region with one event annotation.
    If the text region contains multiple event annotations, the list will have multiple dictionaries.

    :param sentence: text region selecgted from cas
    :param cas: cas file format loaded from xmi doc + typesystem
    :return: list of dictionaries
    """
    tokens = cas.select_covered(TOKEN, sentence)
    events = cas.select_covered(EVENT, sentence)
    entities = cas.select_covered(NAMED_ENTITY, sentence)

    data_per_text_region = []

    annotation_id = 0
    for e in events:
        annotation_id+=1
        i = 0
        data_per_event = {}
        info_event = []
        info_args = []
        annotation_ids = []
        info_entities = []

        while i < len(tokens):
            annotation_ids.append(annotation_id)
            data_per_event['annotation_ids'] = annotation_ids
            i+=1

        i=0

        while i < len(tokens) and tokens[i].begin < e.begin:
            info_event.append(BIO.O.value)  # when no event
            i += 1
        info_event.append((BIO.begin(e.category)) ) #+ '_' + str(e.begin))  # was e.value for ner
        i += 1  # when begin event
        while i < len(tokens) and tokens[i].end <= e.end:
            info_event.append((BIO.midword(e.category)) ) #+ '_' + str(e.begin))  # when mid or end event
            i += 1
        info_event.extend(list(itertools.chain.from_iterable(itertools.repeat(BIO.O.value, len(tokens) - i))))
        data_per_event['events'] = info_event

        if with_entities==True:

            all_entities_lists = []
            for ent in entities:
                list_per_entity = []
                i=0
                while i < len(tokens) and tokens[i].begin < ent.begin:
                    list_per_entity.append(BIO.O.value)  # when no entity
                    i += 1
                list_per_entity.append((BIO.begin(ent.value)))
                i += 1  # when begin event
                while i < len(tokens) and tokens[i].end <= ent.end:
                    list_per_entity.append((BIO.midword(ent.value)) )
                    i += 1
                list_per_entity.extend(list(itertools.chain.from_iterable(itertools.repeat(BIO.O.value, len(tokens) - i))))
                all_entities_lists.append(list_per_entity)
            info_entities = merge_lists(all_entities_lists)
        data_per_event['entities'] = info_entities


        i=0
        try:
            all_arg_lists = []
            for arg in e.arguments.elements:
                list_per_arg = []
                #print(arg)
                i=0
                while i < len(tokens) and tokens[i].begin < arg.target.begin:
                    list_per_arg.append(BIO.O.value)  # when no arg
                    i += 1
                list_per_arg.append((BIO.begin(arg.role)) )#+ '_' + str(e.begin))
                i += 1  # when begin arg
                while i < len(tokens) and tokens[i].end <= arg.target.end:
                    list_per_arg.append((BIO.midword(arg.role)) )#+ '_' + str(e.begin))  # when mid or end arg
                    i += 1
                list_per_arg.extend(list(itertools.chain.from_iterable(itertools.repeat(BIO.O.value, len(tokens) - i))))
                all_arg_lists.append(list_per_arg)
            info_args = merge_lists(all_arg_lists)
        except AttributeError:  # when an event has no arguments
           # print('attribute error')
            while i < len(tokens) and tokens[i].begin < e.begin:
                info_args.append(BIO.O.value)  # when no event
                i += 1
        data_per_event['args'] = info_args

        data_per_event['tokens'] = list(map(lambda x: x.get_covered_text(), tokens))

       # print(data_per_event)
        data_per_text_region.append(data_per_event)
    return(data_per_text_region)


def cas2conll(doc_id, cas, conllfile):
    with open(conllfile, 'w') as f:
        region_id = 0
        for sentence in cas.select(SENTENCE):
            data_per_text_region = get_data_per_event(sentence, cas)
            for dict in data_per_text_region:
                tok_id = 1
                #print('LENGTHS', len(dict['tokens']), len(dict['events']),
                      #len(dict['args']))
                zipped = zip(dict['annotation_ids'], dict['tokens'], dict['events'], dict['args'])
                for anno_id, tok, e, a in zipped:
                    #print(tok, e, a)
                    f.write('doc_'+str(doc_id))
                    f.write('\t')
                    f.write('reg_'+str(region_id))
                    f.write('\t')
                    f.write('anno_'+str(anno_id))
                    f.write('\t')
                    f.write('tok_'+str(tok_id))
                    f.write('\t')
                    f.write(tok)
                    f.write('\t')
                    f.write(e)
                    f.write('\t')
                    f.write(a)
                    f.write('\n')
                    tok_id+=1
                f.write('\n\n')
            region_id += 1

def cas2conll_with_entities(doc_id, cas, conllfile):
    with open(conllfile, 'w') as f:
        region_id = 0
        for sentence in cas.select(SENTENCE):
            data_per_text_region = get_data_per_event(sentence, cas, with_entities=True)
            for dict in data_per_text_region:
                tok_id = 1
                zipped = zip(dict['annotation_ids'], dict['tokens'], dict['events'], dict['args'], dict['entities'])
                for anno_id, tok, e, a, ent in zipped:
                    #print(tok, e, a)
                    f.write('doc_'+str(doc_id))
                    f.write('\t')
                    f.write('reg_'+str(region_id))
                    f.write('\t')
                    f.write('anno_'+str(anno_id))
                    f.write('\t')
                    f.write('tok_'+str(tok_id))
                    f.write('\t')
                    f.write(tok)
                    f.write('\t')
                    f.write(e)
                    f.write('\t')
                    f.write(a)
                    f.write('\t')
                    f.write(ent)
                    f.write('\n')
                    tok_id+=1
                f.write('\n\n')
            region_id += 1

def cas2conll_with_curated_entities(doc_id, cas, cas_curated, conllfile):
    with open(conllfile, 'w') as f:
        region_id = 0
        for sentence in cas.select(SENTENCE):
            data_per_text_region = get_data_per_event(sentence, cas, with_entities=True)
            data_per_text_region2 = get_data_per_event(sentence, cas_curated, with_entities=True)
            for dict in data_per_text_region:
                tok_id = 1
                zipped = zip(dict['annotation_ids'], dict['tokens'], dict['events'], dict['args'], dict['entities'])
                for anno_id, tok, e, a, ent in zipped:
                    #print(tok, e, a)
                    f.write('doc_'+str(doc_id))
                    f.write('\t')
                    f.write('reg_'+str(region_id))
                    f.write('\t')
                    f.write('anno_'+str(anno_id))
                    f.write('\t')
                    f.write('tok_'+str(tok_id))
                    f.write('\t')
                    f.write(tok)
                    f.write('\t')
                    f.write(e)
                    f.write('\t')
                    f.write(a)
                    f.write('\t')
                    f.write(ent)
                    f.write('\n')
                    tok_id+=1
                f.write('\n\n')
            region_id += 1

def get_SRL(input_path):
    folder = pathlib.Path(input_path)
    filenames = list(folder.glob("*.xmi"))

    file_list = get_filepath_list("json_per_doc/")
    data_inv = create_data_inventory(file_list)

    file_id = 0
    for filename in filenames:
        print(filename)
        file_id +=1
        for dict in data_inv:
            print(dict['original_filename'])
            if str(filename).split('/')[-1][:-4] == dict['original_filename'][:-5]: #check filename against metadata in the data inventory to get the inventory number of the document as doc_id
                doc_id = dict['inv_nr']
        with open('TypeSystem.xml', 'rb') as f:
            typesystem = load_typesystem(f)
        with open(filename, 'rb') as f:
            cas = load_cas_from_xmi(f, typesystem=typesystem)
        conllu_path = 'SRL_data/'+str(filename)[:-4]+'.conllu'
        cas2conll(doc_id, cas, conllu_path)


def get_curated_SRL(input_path):
    folder = pathlib.Path(input_path)
    filenames = list(folder.glob("*der E Comp en oppe...xmi"))

    file_list = get_filepath_list("json_per_doc/")
    data_inv = create_data_inventory(file_list)

    file_id = 0
    for filename in filenames:
        file_id +=1
        for dict in data_inv:
            print(dict['original_filename'][:-5])
            print(str(filename).split('/')[-1][:-4])
            if str(filename).split('/')[-1][:-4] == dict['original_filename'][:-5]: #check filename against metadata in the data inventory to get the inventory number of the document as doc_id
                doc_id = dict['inv_nr']
        with open('TypeSystem.xml', 'rb') as f:
            typesystem = load_typesystem(f)
        with open(filename, 'rb') as f:
            cas = load_cas_from_xmi(f, typesystem=typesystem)
        conllu_path = 'SRL_data_curated_entities_and_all_events/' + str(filename)[:-4] + '.conllu'
        cas2conll(doc_id, cas, conllu_path)


def main():
    get_SRL("train/train_5")

if __name__ == '__main__':
    main()