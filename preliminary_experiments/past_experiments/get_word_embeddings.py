# get word embeddings with BERT
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification
tokenizer = RobertaTokenizer.from_pretrained("pdelobelle/robbert-v2-dutch-base", output_hidden_states = True)
model = RobertaForSequenceClassification.from_pretrained("pdelobelle/robbert-v2-dutch-base")
from scipy.spatial.distance import cosine
from pathlib import Path


pathlist = Path("../data/text_annotationpilot_july22").glob('**/*.txt')
collected_texts = []
for path in pathlist:
    path_in_str = str(path)
    with open(path_in_str, encoding='utf-8') as txtfile:
        data_per_file = txtfile.read()
        collected_texts.append(data_per_file)

tokenized_text = tokenizer.tokenize(collected_texts[0])

# Map the token strings to their vocabulary indeces.
indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)

tokens_tensor = torch.tensor([indexed_tokens])
model.eval()

with torch.no_grad():
    outputs = model(tokens_tensor, segments_tensors)
    hidden_states = outputs[2]

token_embeddings = torch.stack(hidden_states, dim=0)
token_embeddings = torch.squeeze(token_embeddings, dim=1)
token_embeddings = token_embeddings.permute(1,0,2)

# Stores the token vectors, with shape [22 x 3,072]
token_vecs_cat = []

# `token_embeddings` is a [22 x 12 x 768] tensor.

# For each token in the sentence...
for token in token_embeddings:
    # `token` is a [12 x 768] tensor

    # Concatenate the vectors (that is, append them together) from the last
    # four layers.
    # Each layer vector is 768 values, so `cat_vec` is length 3,072.
    cat_vec = torch.cat((token[-1], token[-2], token[-3], token[-4]), dim=0)

    # Use `cat_vec` to represent `token`.
    token_vecs_cat.append(cat_vec)

print('Shape is: %d x %d' % (len(token_vecs_cat), len(token_vecs_cat[0])))
