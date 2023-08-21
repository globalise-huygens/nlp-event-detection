import ast

import pandas as pd

def get_resolutions(df, span_row_name):

    tuples = []

    #loop over (concatenated) df
    for index, row in df.iterrows():
        # if the annotation only spans one token
        if len(ast.literal_eval(row[span_row_name])) == 1:
            # and if the resolution is not to not annotate
            if row['Resolved class'] != '/':
                # then append the token_id and resolved class to the list of tuples
                tuples.append((ast.literal_eval(row[span_row_name])[0], row['Resolved class']))
        # if the annotation spans more than one token
        if len(ast.literal_eval(row[span_row_name])) > 1:
            # and if the resolution is not to not annotate
            if row['Resolved class'] != '/':
                # create a tuple for each token
                for i in range(0, len(ast.literal_eval(row[span_row_name]))):
                    tuples.append((ast.literal_eval(row[span_row_name])[i], row['Resolved class']))

    return(tuples)






df1 = pd.read_csv('data/handmade_resolutions/RES_annotated_disagreements_test_set_triggers - Blad1.tsv', sep= '\t')
df2 = pd.read_csv('data/handmade_resolutions/RES_filtered_coverage_disagreements_test_set_triggers - Blad1.tsv', sep='\t')



df1.loc[df1["Resolved span"].isnull(),'Resolved span'] = df1["mention_span_ids"]
df2.loc[df1["Resolved span"].isnull(),'Resolved span'] = df2["mention_span_ids"]


df = pd.concat([df1, df2])
df.to_csv('test.csv')



tuples3 = []
tuples4 = []

for index, row in df.iterrows():
    try:
        if len(ast.literal_eval(row['Resolved span'])) == 1:
            if row['Resolved class'] != '/':
                tuples3.append((ast.literal_eval(row['Resolved span'])[0], row['Resolved class']))
        if len(ast.literal_eval(row['Resolved span'])) > 1:
            for i in range(0, len(ast.literal_eval(row['Resolved span']))):
                tuples4.append((ast.literal_eval(row['Resolved span'])[i], row['Resolved class']))
    except ValueError:
        continue
print('...................')
print(tuples3)
print(tuples4)