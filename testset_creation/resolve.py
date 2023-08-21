import pandas as pd

df = pd.read_csv('data/processed/MERGED.tsv')

def delete_errors(df):
    for index, row in df.iterrows():
        print(type(row['anchor_type']))
            #print(x)

delete_errors(df)