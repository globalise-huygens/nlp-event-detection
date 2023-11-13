import simpledorff
#Calculate krippendorff after check task

# this code is an extention of precision_recall.py, can't be run without it
# this code is not usable at the moment




to_drop = []
for index, row in gold.iterrows():
    if row['final_event'] == '0':
        to_drop.append(index)

df_kripp =pd.DataFrame()
df_kripp['token_id'] = gold['token_id'].to_list()
df_kripp['gold_anno'] = gold['final_event'].tolist()
df_kripp['ann1'] = anos_manj
df_kripp['ann2'] = annos_kay
df_kripp['ann3'] = annos_br
df_kripp['ann4'] = annos_lod
df_kripp = df_kripp.drop(to_drop)
df_kripp = df_kripp.drop(columns=['gold_anno'])
print(df_kripp)


list_of_annotators = ['ann1', 'ann2', 'ann3', 'ann4']
#list_of_rowinfo = []
#for ann in list_of_annotators:
#    for index, row in df_kripp.iterrows():
#        list_of_rowinfo.append()

transformed_data = []
for index, row in df_kripp.iterrows():
    token_id = row['token_id']
    for i, ann in enumerate(row[1:], start=1):
        transformed_data.append([token_id, ann, i])

transformed_df = pd.DataFrame(transformed_data, columns = ['token_id', 'ann', 'ann_id'])
#transformed_df.reset_index(drop=True, inplace=True)

print(transformed_df)


print(simpledorff.calculate_krippendorffs_alpha_for_df(transformed_df,experiment_col='token_id',
                                                 annotator_col='ann_id',
                                                 class_col='ann'))


#... second half


df_kripp =pd.DataFrame()
df_kripp['token_id'] = gold['token_id'].to_list()
df_kripp['gold_anno'] = gold['final_event'].tolist()
df_kripp['ann1'] = anos_manj
df_kripp['ann2'] = annos_kay
df_kripp['ann3'] = annos_br
df_kripp['ann4'] = annos_lod
df_kripp = df_kripp.drop(to_drop)
df_kripp = df_kripp.drop(columns=['gold_anno'])



list_of_annotators = ['ann1', 'ann2', 'ann3', 'ann4']
#list_of_rowinfo = []
#for ann in list_of_annotators:
#    for index, row in df_kripp.iterrows():
#        list_of_rowinfo.append()

transformed_data = []
for index, row in df_kripp.iterrows():
    token_id = row['token_id']
    for i, ann in enumerate(row[1:], start=1):
        transformed_data.append([token_id, ann, i])

transformed_df = pd.DataFrame(transformed_data, columns = ['token_id', 'ann', 'ann_id'])
#transformed_df.reset_index(drop=True, inplace=True)

print(transformed_df)


print(simpledorff.calculate_krippendorffs_alpha_for_df(transformed_df,experiment_col='token_id',
                                                 annotator_col='ann_id',
                                                 class_col='ann'))


#start processing spans
def check_spans(df, i):
    try:
    #check if the event class at i is the same as event class at i+1
        if df.at[i, 'final_event'] == df.at[i+1, 'final_event'] and df.at[i+1, 'final_event']!= 0:
            #check if the event class at i is not the same as the event class at i-1
            if df.at[i, 'final_event'] != df.at[i-1, 'final_event']:
                for i2 in range (1,20):
                    try:
                        if df.at[i, 'final_event'] != df.at[i+i2, 'final_event']:
                            return(int(i2))
                    except KeyError:
                        return(len(df)-i)
    except KeyError:
        return(None)


# maybe better to start with token classification