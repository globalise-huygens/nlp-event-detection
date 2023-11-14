import pandas as pd
from collections import Counter as count


df = pd.read_csv('FINAL_testset.tsv', delimiter='\t')
print(df)

i_annos=0
events = df['final_event'].tolist()
for event in events:
    if event!='0':
        i_annos+=1

print('Amount of tokens in testset document: ', len(events))
print('Amount of tokens with event label: ', i_annos)

counted = count(events)
print(counted)

annotated_tokens = []
for index, row in df.iterrows():
    if row['final_event'] != '0':
        annotated_tokens.append(row['token'])

counted_tokens = count(annotated_tokens)
print()
print(counted_tokens)

l_tokens = []
l_counts = []
for key, value in counted_tokens.items():
    l_tokens.append(key)
    l_counts.append(value)


df1 = pd.DataFrame()
df1['tokens'] = l_tokens
df1['counts'] = l_counts

l_events = []
l_counts = []
for key, value in counted.items():
    l_events.append(key)
    l_counts.append(value)

df2 = pd.DataFrame()
df2['events'] = l_events
df2['counts'] = l_counts



