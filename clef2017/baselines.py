import operator

# Script to automatically generate baseline and oracle runs from CLEF 2017
# training data
# Baseline == random
# Oracle == makes use of abstract/document relevance judgements
# 
# Author: Mark Stevenson
# Last updated: 10/4/2017

# RUNID = "baseline-run"
# RUNID = "abs-oracle-run"
RUNID = "doc-oracle-run"

# Read through relevance judgements
if(RUNID == "abs-oracle-run" or RUNID == "baseline-run"):
    qrel_file = "TrainingData/qrel_abs_train"
elif(RUNID == "doc-oracle-run"):
    qrel_file = "TrainingData/qrel_content_train"

    
    # Dict containing rel judgements
judgements = {}

f = open(qrel_file, "r") 
for line in f: 
    items = line.split()
    topic = items[0]
    pid = items[2]
    qrel = items[3]
    
    if topic not in judgements:
        judgements[topic] = {}
    judgements[topic][pid] = qrel

 
# Print output
if(RUNID is "abs-oracle-run" or RUNID is "doc-oracle-run"):
    # Print out relevant documents with score of 1, and all others with 
    # score of 0
    for topic_id in judgements:
        rank = 1
        for doc_id,score in sorted(judgements[topic_id].items(), key=operator.itemgetter(1), reverse=True):
            print('{t} NF {d} {r} {s} {i}'.format(t=topic_id, d=doc_id, r=rank, s=score, i=RUNID))
            rank = rank + 1
        
else:
    # Print out documents in random order, score is 1 for ranked 1 and reduces
    # by 1/n for each subsequent document (where n is the number of documents
    # associated with the topic)
    for topic_id in judgements: 
        rank = 0
        # Work out how many pids associated with topic
        no_pids = len(judgements[topic_id])
        score = 1 - (rank / no_pids)
        for doc_id in judgements[topic_id].keys():
            score = 1 - (rank / no_pids)
            rank = rank + 1
            print('{t} NF {d} {r} {s} {i}'.format(t=topic_id, d=doc_id, r=rank, s=score, i=RUNID))
            