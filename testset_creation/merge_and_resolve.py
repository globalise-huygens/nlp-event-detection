import pandas as pd
from collections import Counter as count
import ast
from prepare_resolutions import get_resolutions

B = pd.read_csv('data/processed/Brecht-annotations.tsv')
M = pd.read_csv('data/processed/Manjusha-annotations.tsv')
L = pd.read_csv('data/processed/Lodewijk-annotations.tsv')
K = pd.read_csv('data/processed/Kay-annotations.tsv')

print(len(B))
print(len(M))

token_ids_B = B['token_id'].tolist()
token_ids_M = M['token_id'].tolist()

print(token_ids_M)

im = 0
for item in token_ids_M:
    if '.' in item:
        im+=1
        print(item)

print()
ib = 0
for item in token_ids_B:
    if '.' in item:
        ib+=1
        print(item)

print()
print(im)
print(ib)

print(im-ib)
print(len(M)-len(B))

# For now I am removing the split up tokens in order to make the dfs of the same length

def drop_splitup_tokens(df):
    indices_to_drop = []
    for index, row in df.iterrows():
        if '.' in row['token_id']:
            indices_to_drop.append(index)
    new_df = df.drop(indices_to_drop)
    return(new_df)

M = drop_splitup_tokens(M)
K = drop_splitup_tokens(K)
B = drop_splitup_tokens(B)
L = drop_splitup_tokens(L)


print(len(M))
print(len(K))
print(len(B))
print(len(L))

def delete_mistakes(l):
    new = []
    for item in l:
        if item == '*':
            new.append(0)
        else:
            new.append(item)

    return(new)

def merge_annotations(df1, df2, df3, df4):
    annos1 = df1['eventclass_no_number'].tolist()
    annos2 = df2['eventclass_no_number'].tolist()
    annos3 = df3['eventclass_no_number'].tolist()
    annos4 = df4['eventclass_no_number'].tolist()

    anchors1 = df1['anchor_type'].tolist()
    anchors2 = df2['anchor_type'].tolist()
    anchors3 = df3['anchor_type'].tolist()
    anchors4 = df4['anchor_type'].tolist()

    #filter out mistakes
    ann1 = delete_mistakes(annos1)
    ann2 = delete_mistakes(annos2)
    ann3 = delete_mistakes(annos3)
    ann4 = delete_mistakes(annos4)

    anch1 = delete_mistakes(anchors1)
    anch2 = delete_mistakes(anchors2)
    anch3 = delete_mistakes(anchors3)
    anch4 = delete_mistakes(anchors4)


    merged_eventclasses = list(zip(ann1, ann2, ann3, ann4))
    merged_anchors = list(zip(anch1, anch2, anch3, anch4))

    df = pd.DataFrame()
    df['token'] = df1['token']
    df['token_id'] = df1['token_id']
    df['anchor_type'] = merged_anchors
    df['event_anno'] = merged_eventclasses


    return(df, merged_eventclasses)

df, classes = merge_annotations(M, K, B, L)
#print(df)



#anchors = []
#classes = []

#for index, row in df.iterrows():
#    l_anch = list(row['anchor_type'])
#    i = 0
#    while i < len(l_anch):
#        if l_anch[i] == '*':
#            l_anch[i] = 0
#    anchors.append(tuple(l_anch))

#print(anchors)

#df['anchor_type'] = anchors
#df['event_anno'] = classes

#df.to_csv('data/processed/MERGED2.tsv')

print()
print()

#first_resolve_class = []
i = -1
to_add = []
for tuple in classes:
    i+=1
    counted = count(tuple)
    for key, value in counted.items():
        if value >= 3:
            to_add.append((i, key))
       # if value <= 3:
        #    first_resolve_class.append(tuple)
print()
print('...')
print(len(classes))
print(len(to_add))

for x in to_add:
    classes[x[0]] = x[1]

print('...')
print(classes)

i_class=0
i_noneclass = 0
i_unresolved = 0
for item in classes:
    if type(item) == str and item != '0':
        i_class += 1
        print(item)
    if type(item) == str and item == '0':
        i_noneclass += 1
    if type(item) != str:
        i_unresolved +=1

print()
print('First resolve step (merging classes on token level that are annotated by three or four annotators, we resolved ', i_class, ' classes and ', i_noneclass, ' none-classes')
print('not resolved: ', i_unresolved)

translocation_events = ['TransLocation', 'Transportation', 'Leaving', 'Arriving', 'Voyage', 'Translocation']
df['event_resolve1'] = classes

def taxonomic_resolve(annos, possible_classes, resolution):
    i = -1
    to_add = []
    for tuple in annos:
        i+=1
        i_key=0
        for key in tuple:
            if key in possible_classes:
                i_key += 1
            if i_key >= 3:
                to_add.append((i, resolution))

    return(to_add)



result = taxonomic_resolve(classes, translocation_events, 'Translocation')
print('RESULT')
print(result)

for x in result:
    print(x)
    classes[x[0]] = x[1]


print('....')

i_class=0
i_noneclass = 0
i_unresolved = 0
for item in classes:
    if type(item) == str and item != '0':
        i_class += 1
        print(item)
    if type(item) == str and item == '0':
        i_noneclass += 1
    if type(item) != str:
        i_unresolved +=1

print()
print('Second resolve step (merging classes on taxonomic level for Translocation events) resulted in a total resolution of ', i_class)
print('not resolved: ', i_unresolved)

df['event_resolve2'] = classes


i_annos = 0
i = 0
for item in classes:
    if item!= '0':
        i_annos+=1
    if item == '0':
        i+=1


print(i_annos)
print(i)



########## insert handmade resolutions

# read in files
df1 = pd.read_csv('data/handmade_resolutions/RES_annotated_disagreements_test_set_triggers - Blad1.tsv', sep= '\t')
df2 = pd.read_csv('data/handmade_resolutions/RES_filtered_coverage_disagreements_test_set_triggers - Blad1.tsv', sep='\t')

# create one column with all relevant token_ids
df1.loc[df1["Resolved span"].isnull(),'Resolved span'] = df1["mention_span_ids"]
df2.loc[df2["Resolved span"].isnull(),'Resolved span'] = df2["mention_span_ids"]

# merge in one df
df_reso = pd.concat([df1, df2])
df_reso.to_csv('test.csv')

# get event resolutions
list_of_tuples = get_resolutions(df_reso, 'Resolved span')

print(list_of_tuples)

for x in list_of_tuples:
    print(x)
    #classes[x[0]] = x[1]


print('....')

i_class=0
i_noneclass = 0
i_unresolved = 0
for item in classes:
    if type(item) == str and item != '0':
        i_class += 1
        print(item)
    if type(item) == str and item == '0':
        i_noneclass += 1
    if type(item) != str:
        i_unresolved +=1


print()
print('Third resolve step (merging classes on taxonomic level for Translocation events) resulted in a total resolution of ', i_class)
print('not resolved: ', i_unresolved)

df['event_resolve3'] = classes


i_annos = 0
i = 0
for item in classes:
    if item!= '0':
        i_annos+=1
    if item == '0':
        i+=1


print(i_annos)
print(i)