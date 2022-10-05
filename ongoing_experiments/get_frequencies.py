from pathlib import Path
from collections import Counter
import spacy

pathlist = Path("../data/text_annotationpilot_july22").glob('**/*.txt')
collected_texts = []
for path in pathlist:
    path_in_str = str(path)
    with open(path_in_str, encoding='utf-8') as txtfile:
        data_per_file = txtfile.read()
        collected_texts.append(data_per_file)

def preprocess(list_of_texts, chars_to_remove={'\n', ',', '.', '"', ':/', '/:'}):
    """
    a)clean a text by removing the characters that a user provides
    b)split a text on ' '
    :param lst list_of_texts: a list of strings
    :keyword param chars: a set
    """
    container = []
    for text in list_of_texts:
        for chars in text:
            if chars in chars_to_remove:
                text = text.replace(chars, '')
        split_text = text.split()
        for word in split_text:
            container.append(word)

    return (container)


def count(list_of_strings):
    """
    :param lst list_of_strings: list
    """
    a_list = preprocess(list_of_strings, chars_to_remove={'.', '(', ')', '„'})
    wordfreq = dict()

    for word in a_list:
        if word in wordfreq:  # add 1 to the dictionary if the keys exists
            wordfreq[word] += 1
        else:
            value = 1  # set default value to 1 if key does not exists
            wordfreq[word] = value
    return (wordfreq)


#wordfreq_dict = count(collected_texts)
#sort_dict = sorted(wordfreq_dict.items(), key=lambda x: x[1], reverse=True)
#print(len(sort_dict))
#for key, value in wordfreq_dict.items():
 #   if 10 <= value <= 50:
  #      print(key, value)

word_list = preprocess(collected_texts)
nlp = spacy.load("nl_core_news_sm")
#other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "tagger"]
#nlp.disable_pipes(*other_pipes)

tuples_pos = []
for word in nlp.pipe(word_list):
    doc = nlp(word)
    tuples_pos.append((doc[0].text, doc[0].tag_))

verbs = []
nouns = []
print(type(tuples_pos[0][1]))

for entry in tuples_pos:
    if entry[1].startswith('WW'):
        verbs.append(entry[0])
    if entry[1].startswith('N'):
        nouns.append(entry[0])

verbfreqs = Counter(verbs)
nounfreqs = Counter(nouns)

print(nounfreqs)



#doc = nlp(collected_texts[0])


#wordfreq_dict = Counter(word_list)
#print(wordfreq_dict)

#for word in word_list:
   #doc = nlp(word)
   #if doc[0].tag != 'N|soort|ev|basis|zijd|stan':
       #print(doc[0].tag_)
       #print(doc[0].text, doc[0].tag_)



