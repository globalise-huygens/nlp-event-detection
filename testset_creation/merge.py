import pandas as pd

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

for item in classes:
    for i in range(0,4):
        print(item[i])
