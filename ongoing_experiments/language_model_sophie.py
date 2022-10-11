from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained("CLTL/gm-ner-xlmrbase")
model = AutoModelForTokenClassification.from_pretrained("CLTL/gm-ner-xlmrbase")

nlp = pipeline("ner", model=model, tokenizer=tokenizer)
example = "Pattam is in de problemen"

ner_results = nlp(example)
print(ner_results)