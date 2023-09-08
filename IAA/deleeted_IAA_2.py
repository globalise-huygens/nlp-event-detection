
########## Get label disagreements

all_disagreements = d1+d2
all_processed = p1+p2

# Gather all annotations for mentions where disagreement occurs, where each annotation from different anntotators are seperate entries
dd = defaultdict(list)
for d in all_processed:
    for key, value in d.items():
        dd[key].extend(value)


# Gather all annotations by all annotators for one specific mention together
## In order to do this, list values for mention_ids have to be converted to strings
gather_all = []
for d in all_disagreements:
    for key, value in dd.items():
        if str(d['mention_span_ids']) == key:
            gather_all.append({'mention_span_ids': str(d['mention_span_ids']), 'mention_span': d['mention_span'], 'annotations': str(set(dd[key])), 'mention_in_context':d['mention_in_context']})

merge_duplicates = [dict(t) for t in {tuple(d.items()) for d in gather_all}]

# As a final step we convert mention_ids and lists of annotated event trigger labels back to list objects
final_annotated_disagreements = []
for d in merge_duplicates:
    final_annotated_disagreements.append({'mention_span_ids': eval(d['mention_span_ids']), 'mention_span': d['mention_span'], 'annotations':eval(d['annotations']),'mention_in_context':d['mention_in_context']})

df_type_disagreements = pd.DataFrame(final_annotated_disagreements)
print(df_type_disagreements)
