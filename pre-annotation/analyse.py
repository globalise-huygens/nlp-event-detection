"""
Code to analyse basic stats of different lexicon versions and compare
"""

import pandas as pd

df = pd.read_csv('lexicon_v2.csv')
tokens = df['tokens'].tolist()
labels = df['label'].tolist()
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





