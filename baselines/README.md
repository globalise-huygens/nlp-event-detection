# Baseline system event detection & classification GLOBALISE


## First experiments 

Stella Verkijk, 10 dec 2023

This document reports on experiments with finetuning XLM-R for event detection with lightning on Snellius. I am using code written by Sophie that I have adapted to work for events (to be published on GitHub). This includes the data processing with Sophie’s cas2json function. 



1. Experiment 1:<span style="text-decoration:underline;"> XLM-R finetuning</span>. **Data** = annotation round 3, **tagset** = all event types

train = 171KB; .json

test = 22KB; .json


<table>
  <tr>
   <td>nr
   </td>
   <td>Epoch settings
   </td>
   <td>Epochs trained
   </td>
   <td>P / R
   </td>
  </tr>
  <tr>
   <td>1.1
   </td>
   <td>min: 3
<p>
max: 6
   </td>
   <td>4
   </td>
   <td>0.00 / 0.00
<p>
all classes
   </td>
  </tr>
  <tr>
   <td>1.2
   </td>
   <td>min: 6
<p>
max: 12
   </td>
   <td>6
   </td>
   <td>0.00 / 0.00
<p>
all classes
   </td>
  </tr>
  <tr>
   <td>1.3
   </td>
   <td>min: 12
<p>
max: 18
   </td>
   <td>12
   </td>
   <td>0.00 / 0.00
<p>
all classes
   </td>
  </tr>
  <tr>
   <td>1.4
   </td>
   <td>min: 20
<p>
max: 25
   </td>
   <td>20
   </td>
   <td>0.00 / 0.00
<p>
all classes
   </td>
  </tr>
  <tr>
   <td>1.5
   </td>
   <td>min: 50
<p>
max: 50
   </td>
   <td>50
   </td>
   <td>0.00 / 0.00 
<p>
all classes
<p>
EXCEPT
<p>
'Translocation': {'precision': 0.125, 'recall': 0.375, 'f1': 0.1875, 'number': 8}
<p>
<strong>note</strong>: 
<p>
'Transportation': {'precision': 0.0, 'recall': 0.0, 'f1':  0.0, 'number': 24}
   </td>
  </tr>
</table>




2. Experiment 2: <span style="text-decoration:underline;">XLM-R Finetuning</span>. **Data** = annotation round 3, **tagset** = ‘I-event, ‘B-event’, ‘O’

train = 171KB; .json

test = 22KB; .json

This experiment only tests event detection, no classification, as we have very limited data for many event types.


<table>
  <tr>
   <td>nr
   </td>
   <td>Epoch settings
   </td>
   <td>Epochs trained
   </td>
   <td>P / R
   </td>
  </tr>
  <tr>
   <td>2.1
   </td>
   <td>min: 3
<p>
max: 6
   </td>
   <td>6
   </td>
   <td>0.00 / 0.00
   </td>
  </tr>
  <tr>
   <td>2.2
   </td>
   <td>min: 6
<p>
max: 12
   </td>
   <td>9
   </td>
   <td>0.34 / 0.24
   </td>
  </tr>
  <tr>
   <td>2.3
   </td>
   <td>min: 12
<p>
max: 18
   </td>
   <td>12
   </td>
   <td>0.40 / 0.36
   </td>
  </tr>
  <tr>
   <td>2.4
   </td>
   <td>min: 20
<p>
max: 25
   </td>
   <td>20
   </td>
   <td>0.40 / 0.43
   </td>
  </tr>
  <tr>
   <td>2.5
   </td>
   <td>min: 50
<p>
max: 50
   </td>
   <td>50
   </td>
   <td>0.54 / 0.32
   </td>
  </tr>
</table>




3. Experiment 3: lexical baseline. **Data** = annotation round 3, **tagset** = ‘I-event, ‘B-event’, ‘O’

train = 171KB; .json

test = 22KB; .json

In this experiment, I extracted all tokens with an event annotation from the training data and mapped all extracted tokens to tokens in the test data. I experimented using the lexicon as-is, without filtering out interpunction and function words and I experimented with filtering out interpunction and function words. I also evaluated on binary (event/non event) level since the BIO labels were taken out of context when mapping them from the training data to the test data. For example, it might happen that in the training data a string like ‘is ontfangen’ is annotated with B-EVENT, I-EVENT, whereas ‘ontfangen’ might be a B-EVENT in the test data. 


<table>
  <tr>
   <td>
   </td>
   <td>filtering out interpunction?
   </td>
   <td>filtering out function words?
   </td>
   <td>binary / BIO eval
   </td>
   <td>P/R
   </td>
  </tr>
  <tr>
   <td>3.1
   </td>
   <td>no
   </td>
   <td>no
   </td>
   <td>BIO
<p>
binary
   </td>
   <td>0.03 / 0.16 \
0.04 / 0.21
   </td>
  </tr>
  <tr>
   <td>3.2
   </td>
   <td>yes
   </td>
   <td>no
   </td>
   <td>BIO
<p>
binary
   </td>
   <td>0.05 / 0.15
<p>
0.07 / 0.20
   </td>
  </tr>
  <tr>
   <td>3.3
   </td>
   <td>no
   </td>
   <td>yes
   </td>
   <td>BIO
<p>
binary
   </td>
   <td>0.03 / 0.07
<p>
0.04 / 0.10
   </td>
  </tr>
  <tr>
   <td>3.4
   </td>
   <td>yes
   </td>
   <td>yes
   </td>
   <td>BIO
<p>
binary
   </td>
   <td>0.08 / 0.07
<p>
0.12 / 0.09
   </td>
  </tr>
</table>




4. Experiment: Annotating the training data with annotations gathered from the training data

I also wanted to know what would happen if we would annotate the training data with the automatically derived lexicon and then continue pre-training on the test data, since we know it can happen that annotators miss events. 

I checked for how many instances (tokens) in the training data a token from the lexicon that is not a function word or interpunction we could add an annotation (i.e., it was not annotated as an event previously). This was the case for 35 tokens. I decided to go through them manually to see if it were instances of annotators missing events or whether it was granted for the token to be labeled as non-event. 



5. Annotating testdata with more elaborate lexicon

Result binary evaluation only detection: P  0.92  / R  0.22 

Thoughts for further experiments: 



* take nootmuskaat docs and annotate with curated lexicon. 
* take docs from annotation round 2 and annotate with curated lexicon
* create different versions of training data and finetune XLM again with different epochs
* test fine-tuning XLM on 171 KB of contemporary data
* create word embeddings for lexicon entries and use as augmentation method
    * See how many missed events are left and what kinds of events they are
    * create evaluation set. cleaned up lexicon; set of missed items; run different approaches, word2vec, gysbert, etc. 
* Think about: ways of predicting how much variation is left after each improvement of the lexicon
* Thing about: 2 gram collocations, PMI. How often do tokens occur together?
6. Appendices

**Predictions experiment 2 with 20 and 50 epochs**

**[https://docs.google.com/spreadsheets/d/1R42BiIXT5RFOHY5qyhW3bKQk1tcDec-PbK9RwRtumWQ/edit?usp=sharing](https://docs.google.com/spreadsheets/d/1R42BiIXT5RFOHY5qyhW3bKQk1tcDec-PbK9RwRtumWQ/edit?usp=sharing)**

**Predictions experiment 3**

**[https://docs.google.com/spreadsheets/d/1smAZZqv2Mn2ODS4YfsqzNq8KY6ry3hsfV1u8xOO7TIU/edit?usp=sharing](https://docs.google.com/spreadsheets/d/1smAZZqv2Mn2ODS4YfsqzNq8KY6ry3hsfV1u8xOO7TIU/edit?usp=sharing)**
