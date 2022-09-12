# Report Annotation Round 1 (Dry Annotation)
### Stella Verkijk, august 2, 2022

This document reports on the first round of event annotation for the Globalise project which took place in July 2022. This round of event annotation was performed without using the FrameNet annotation tool. In Section 1, the report will describe how the annotation was performed, and in Section 2 the resulting preliminary ontology will be described. Section 3 will outline problems that were recognised during annotation, future decisions that should be made and recommendations for a next annotation round.  
Annotation process

## 1.1 Stage one

During the first stage of ‘dry annotation’, we read the documents and i) identified relevant frames that should be annotated; ii) searched for a fitting frame in the Berkeley Framenet, and whenever there was no fitting frame we iii) defined a new frame, always keeping in mind whether it could be annotated in the actual text. In the last column of the table, the relation of the Globalise frame to the framenet frame is defined. ‘skos:exactMatch’ means that we use the original Berkeley frame. The following documents were included in this round of annotation (scan numbers are given for which annotations were made): Inv. nr 9018 scans 1737-39; Inv. nr 7586 Groenendaal scans 0381-5 and scans 253-4; Inv nr. 8105 scans 10-11;  Inv. No. 7586 scan 375; Inv. No. 7662 scans 39-40; Inv No. 7528 scans 17-19. 
During annotation, for each letter the top themes were defined after which the sentences representing these themes were identified alongside frames that could represent those sentences. This was done because it made it easier to identify relevant frames. However, it could be an idea to use this method or an inverse of this method (first identifying frames and then appointing them to a theme) throughout the project in order to give more space for either broader and narrower search queries in the final infrastructure. The idea behind classifying frames into themes and subthemes is that it gives the opportunity to researchers to search for broader concepts without losing event annotation on a detailed level. For example, a researcher could search for all events related to diplomatic relations and get all relevant documents in which any of the frames classified under diplomatic relations appear (also the frames with the sub-classification ‘internal relations VOC’). At any point in time, the researcher can choose to only get those frames classified under ‘internal relations VOC’. There would also still be an option to directly browse all annotated frames and search for one or more frames directly without having to deal with any classification within a theme. Frames do not get a classification or theme label during annotation, which means that if an instance of a frame does not belong to the theme it was assigned to it will not be lost. The classification into themes is only there to make the search process easier for the user. Of course, there would also be an option to select entities or places that play a role in the frames. An example of a search query could be: ‘Give me all documents about the condition of the crew on the ship Groenendaal’. The system would return all documents annotated with Being_sick, Dying, and Death in which the frame element ‘Place’ is an entity that is linked to the unique entity of the ship Groenendaal. 

## 1.2 Stage two

During stage two, a member of WP3 went through the documents taken up in the annotation round again, noting down each annotation formally this time, mostly to trace back where in the documents we found instances of which frames. In this document, predicates and frame elements were also indicated. This document can be found here.
Preliminary ontology

## 2.1 Creation

After stage one of the annotation process, WP4 began forming a preliminary ontology, taking up all Berkely frames as well as new frames that were needed to annotate the documents. Stage two of the annotation process relied on this draft of the preliminary ontology. When stage two of the annotation process was finished, the preliminary ontology relied on those annotations to give an example annotation for each frame indicated. 

## 2.2 Explanation

The preliminary ontology can be downloaded under the name globalise_ontology_annotation_round_one.xlsx 

### Colour legend
The cells that are coloured red represent decisions I made that I am not yet sure about. Cells coloured gray represent Globalise frames for which information is still missing. For example, for some new frames I have not found a frame yet in FrameNet to which it can be related within the SKOKS framework. Also, there are some new frames for which I have not yet defined the most important frame elements because I need more examples.

### SKOS relations

SKOS stands for Simple Knowledge Organization System. It is a common data model for sharing and linking knowledge organization systems via the Semantic Web. We use their mapping framework to match frames in the Globalise ontology to frames from FrameNet. In Table 2, the relationships used in Table 1 are explained.

Table 2: SKOS relations used:

![alt text](https://github.com/[globalise-huygens]/[nlp-event-detection]/blob/[master]/skos_table.jpg?raw=true) 


Website: https://www.w3.org/TR/skos-reference/#mapping


### Domains, themes and subthemes
The first three columns in the ontology represent areas to which the frame belongs. The domain is either polities (everywhere in Sheet 1) or ship movement (everywhere in Sheet 2). The themes and subthemes represent broader concepts the frame can be classified under as discussed in Section 1.1. 

### Frame elements
In this preliminary ontology, I have noted down the frame elements that seemed most important to annotate according to the pilot data. I have not yet made a distinction between core elements and non-core frame elements. This has two reasons: 1) I need more examples to know which frame elements should always be labeled;  2) the distinction between core elements and non-core elements within the FrameNet framework does not seem logical to me, since it is not the case that core elements always appear and therefore can always be annotated. This makes me wonder whether we should make this distinction or define a new sort of distinction. 
Future work

## 3.1 Notes
Not all frames in the preliminary ontology have an example of an annotation. This is because of two things. Firstly, not all frames that I noted down during dry annotation in the group setting re-appear in the annotations Henrike made afterwards. For example, Requesting_resignation and Hostile_encounter. In these two cases (if I remember correctly) we did see a sentence that would have been annotated with these frames. The second reason why there are frames without an example annotation is because we added some frames to the ontology based on (linguistic) intuition. For example, when we added the frame Having_a_contract because we saw a sentence that should be annotated with this frame, we also added the new frame Breaking_a_contract to the ontology, even though this was not represented in the texts from the pilot data. 

## 3.2 Unanswered questions
There are many questions that remain unanswered, the biggest one being whether this way of adapting the FrameNet frames is the best option when annotating events for the Globalise project. This section will discuss both some smaller questions that arose during this specific pilot and that haven’t been answered yet as well as some bigger questions that need to be addressed constantly during upcoming pilots. 

### Travel or Departing frame or both?
We have had discussions about whether to use both these frames or only choose one. The travel frame has as an upside that it takes many frame elements and can describe the whole journey as opposed to only the departing event, but it has as a downside that the definition in FrameNet seems to carry a connotation with traveling by plane / going on a holiday. 
### How to differentiate between different types of Sending?
In this pilot, we have seen the verb ‘sending’ being used in different ways. Sometimes, ships might be sent somewhere when other times persons might be sent away based on political reasons (more like a deportation). We need to think about whether we want to retain the basic meaning of sending in the sense of sending something or someone to a different place, and if so, how to do this if we also want to extract the more specific difference in meaning between for example deporting and sending on a journey. 
### Annotate without prepositions?
We should come to a consensus when it comes to which spans to annotate (dates with prepositions or without prepositions, etc.)
### Differentiate between core frame elements and non-core frame elements?
For me it is still an open discussion how to go about this. From what I have seen so far, I think that even if we use a framenet Frame precisely as it is described in FrameNet meaning wise, we might still want different core elements there (either less or more) than described in FrameNet, so it might be worthwhile to make our own rules for this. 
### How to differentiate between or combine contextual meaning and sentence level meaning?
This is one of the biggest questions we have to address. It is hard to extract important meanings while keeping true to what is literally stated on sentence level. We might want to think about either combining topic modeling on document level and FrameNet-style semantic role labeling on sentence level, or adopting a different method, for example mapping combinations of several frames to a contextual meaning that can also be found in the search interface. In the next pilot annotation round, we want to make annotators aware of the difference between sentence vs. document/contextual meaning, and ideally find a way to enable them to annotate both. 
### Downsides of following FrameNet?
The more I work and read about FrameNet, the less I am convinced of how suitable it is for our project in its current state. I am gathering my thoughts about this in a different document. 



