MRCWOZ is a dialogue comprehension dataset, cureated from the MultiWOZ 2.2 (Zang et al., 2020) dataset, where the answer to every question is a segment of text, or span, from the corresponding dialogue. 

In order to convert MultiWOZ, which is normally a dialogue state tracking (DST) dataset, we annotate two questions for each slot in the restaurant, taxi and hotel domains. The original MultiWOZ dataset 
does not label the span of the answer in the dialogue but rather give the answer separately. We find spans of each answers in the dialogues and for each slot of a dialogue give pairs of question-answers 
in the same format that SQuAD (Rajpurkar et al., 2018) introduced. 

The "Domains" directory includes subdirectories for each "hotel", "restaurant" and "taxi" domains. Under each subdirectory there are files called "dev", "test", "train" and "vel_dev". The firt three are the above conversion process applied directly
to MultiWoz development, test and train files. The last file, vel_dev, is the set of dialogues that we use to create our synthetic data. For detailed explanation refer to the experiments section of the paper. 