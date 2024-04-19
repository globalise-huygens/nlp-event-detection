import pandas as pd
from prettytable import PrettyTable

df = pd.read_csv("data/POS-tagging-gold-input_3-1.csv", sep = ',')
print(df)

def get_score(df, model):

    zipped = zip(df[model].tolist(), df['gold'].tolist())
    tp = 0

    for item in zipped:
        if item[0] ==  item[1]:
            tp += 1
    acc = (tp / len(df))*100

    return (acc)


xlm_acc = get_score(df, 'xlm')
rob_acc = get_score(df, 'robbert')
gys_acc = get_score(df, 'gysbert')
gys2_acc = get_score(df, 'gysbert_2')
spacy_sm = get_score(df, 'spacy_nl_core_news_sm')
spacy_lg = get_score(df, 'spacy_nl_core_news_lg')

print("Zero-shot POS-tagging")
table = PrettyTable()
table.field_names = ["", "spacy_nl_core_news_sm", "spacy_nl_core_news_lg", "RobBERT", "XLM-R", "GysBERT", "GysBERT-v2"]
table.add_row(["accuracy", spacy_sm, spacy_lg, rob_acc, xlm_acc, gys_acc, gys2_acc])
print(table)
