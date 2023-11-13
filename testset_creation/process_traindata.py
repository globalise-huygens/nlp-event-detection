import glob, os
import pandas as pd
from process_inception import main
#from merge_and_resolve import drop_splitup_tokens, delete_mistakes

tokens = []
tags = []
all_events = []
token_count = 0

os.chdir("./Training Data Sep 2023")
#i=0
#for file in glob.glob("*.tsv"):
    #i+=1
    #main(file, "processed/doc_"+str(i)+"_pre.tsv", "processed/doc_"+str(i)+"_processed.tsv")
    #print('pre-processing '+file+'......')

for file in glob.glob("processed/*processed.tsv"):
    print('extracting events from '+file+'......')
    df = pd.read_csv(file)
    #df = drop_splitup_tokens(df)
    #df = delete_mistakes(df)

    event_annos = df['eventclass_no_number'].tolist()
    tags.append(event_annos)
    for anno in event_annos:
        token_count+=1
        if anno != '0':
            all_events.append(anno)
        #tags.append(anno)

    #tokens = df['token'].tolist()
    #for token in tokens:
        #tokens.append(token)


print(len(all_events))
print(token_count)

print(len(tokens))
print(len(tags))
