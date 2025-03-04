"""
Code to analyse basic stats of different lexicon versions and compare
"""

import pandas as pd

df = pd.read_csv('lexicon_release1.csv')
tokens = df['tokens'].tolist()
labels = df['label'].tolist()
up1 = df['upperclass_1'].tolist()
up2 = df['upperclass_2'].tolist()
relationtypes = df['relationtype'].tolist()
zipped_ref = zip(tokens, labels, relationtypes)

tokentypes = 0
tokenvariations = 0
for typ in tokens:
    tokentypes += 1
    vars = len(typ.split(';'))
    tokenvariations += vars

print('Number of token types: ', tokentypes)
print('Number of token variations: ', tokenvariations)
print('Number of event types: ', len(set(labels)))


all_strings = []
for entry in tokens:
    strings = entry.split('; ')
    for string in strings:
        all_strings.append(string)

print(len(all_strings))
print(all_strings)
print('unique strings in lexicon first release: ', len(set(all_strings)))

all_event_types = []
for label in labels:
    all_event_types.append(label)
for ev_up1 in up1:
    all_event_types.append(ev_up1)
for ev_up2 in up2:
    all_event_types.append(ev_up2)

print(len(all_event_types))
print(len(set(all_event_types)))
print('unique event classes in lexicon first release: ', len(set(all_event_types)))

print()
print('event classes represented:')

for eventclass in set(all_event_types):
    print(eventclass)



