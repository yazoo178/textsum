CLEF2017 eHealth
Task 2: Technologically Assisted Reviews in Empirical Medicine
this project is for CLEF2017 task 2.

https://sites.google.com/site/clefehealth2017/task-2

we used python 3.6

***********************
Training data include 20 topics.

For each topic the following information is provided in topic train folder:
* Topic ID
* Topic title
* Topic query
* list of PubMed PIDs1. 

***********************

Training data folder:
qrel for abs and content 
topics train 

***********************

Data folder and subfolders:
Abstracts --> text files contain PIDs abstract
MeSHs --> text files contain MeSHs heading for each PID
Queries --> text files contain Queries extracted from topic train for each topic
MeSH and terms --> text files contain extracted MeSH and Terms from queries

***********************

Output:
conatins run1, run2, run3, run4 and run5 output in TREC eval format:
TOPIC-ID    INTERACTION    PID    RANK    SCORE    RUN-ID

***********************

Files:
retrive_data.py
reterive titles, abstracts and MeSHs from Medline.
Extract queries from data files.

***********************

find_terms_MeSH.py
Extract terms and MeSHs from queries.

***********************

encoded_MeSH.py
Add 'MeSH' prefix to MeSHs extracted from queries and retrieved with abstracts.

***********************

main_runs.py
Apply CLEF approach on training dataset or test dataset:
Sheffield_run_1
calculate the similarity between "the topic title" and "the PubMed title and abstract" based on cosine similarity

Sheffield_run_2
calculate the similarity between "the topic title" and "the PubMed title, abstract, and terms" based on cosine similarity

Sheffield_run_3
calculate the similarity between "the topic title and MeSH heading" and "the PubMed title, abstract, terms, and MeSH heading" based on cosine similarity

Sheffield_run_4
calculate the similarity between "the topic title and MeSH heading" and "the PubMed title, abstract, and terms" based on cosine similarity using PubMed stopwords

Sheffield_run_5
calculate the similarity between "the topic title and MeSH heading" and "the PubMed title, abstract, and MeSH heading" based on cosine similarity
retrive_query.py
extract queries from training data files

***********************

Log-likelihood.py
Calculate the Log likelihood for individual topics or for topics combined. 

***********************

