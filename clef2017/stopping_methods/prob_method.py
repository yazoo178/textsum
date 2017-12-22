import operator
import matplotlib.pyplot as plt
import math
import numpy as np
import sys, getopt
import random

# Script to determine stopping for systematic reviews based on expected number of remaining relevant 
# documents
# Approach: read through first N documents and then estimate the number of relevant remaining based on 
# probability of most recent being relevant (using BATCH as batch size). Stop when number expected is 
# below some threshold
# 
# Author: Mark Stevenson
# Last updated: 26/6/2017    
#
# Usage: prob_method.py -o output -q qrels -c THRESHOLD


BATCH = 100  # Size of batches in which probabilities are estimated

def usage():
    print("prob_method.py -c THRESHOLD -o <run_file> -q <qrel_file>\n")
    print("-c cutoff threshold")
    print("\te.g. prob_method.py -c 0.1 continues until estimated that fewer than 10% of relevant documents remain\n")
    sys.exit()


qrel_file = ''
run_file = ''
cutoff = ''
opts, args = getopt.getopt(sys.argv[1:],"hc:o:q:")
for opt, arg in opts:
    if opt == '-h':
        usage()
    elif opt in ("-o"):
        run_file = arg
    elif opt in ("-q"):
        qrel_file = arg
    elif opt in ("-c"):
        cutoff = float(arg)

# Check arguments were parsed without problems
if(run_file == '' or qrel_file == ''): 
    usage()

if(cutoff == ''):
    cutoff = 0.1

print("Run file is ", run_file)
print("Qrel file is ", qrel_file)
print("Using probability cutoff method (cutoff of {c})".format(c = cutoff))


# Read through qrels to create dict containing rel judgements
judgements = {}

f = open(qrel_file, "r") 
for line in f: 
    items = line.split()
    topic = items[0]
    pid = items[2]
    qrel = items[3]

    if topic not in judgements:
        judgements[topic] = {}
    if(qrel is "1"): 
        judgements[topic][pid] = qrel
f.close()



# Dict containing relevance counts 
rel_count = {}
ranked_docs = {}

# Read through run output and create lists of pmids found
docsFoundDoL = {}
rankedDocsDoL = {}
f = open(run_file, "r")

last_topic = "null"
topic_count = 0

for line in f:
    items = line.split()
    topic = items[0]
    pid = items[2]
    rank = items[3]

    if(topic != last_topic):
        docsFoundDoL[topic] = []
        rankedDocsDoL[topic] = []
        last_topic = topic

    # Store in list of running total of found documents
    docsFoundDoL[topic].append(rel_count)
    # Store in list of ranked documents
    rankedDocsDoL[topic].append(pid)


# Run method for each topic
recall_stats = {}
effort_stats = {}

for topic in sorted(rankedDocsDoL): 
    total_docs = len(rankedDocsDoL[topic])
    
    examined = []  # List to store relevance judgements for docs looked at so far
    for i in range(0, total_docs):
        # Check whether document is relevant
        if rankedDocsDoL[topic][i] in judgements[topic]:
            examined.append(1)
        else:
            examined.append(0)

        # Estimate number of relevant documents left  
        if i % BATCH == 0: 
            # Take last n documents and estimate probability of relevant
            # Use this to estimate number of relevant documents remaining 
            rel = sum(examined[(i - BATCH):i])
            est_prob_rel = (rel / BATCH) + (2 * math.sqrt(0.25 / BATCH)) # MLE with upper estimate of 95% CI
            est_rel_remain = est_prob_rel * (total_docs - i) 
            rel_found = sum(examined)
            if est_rel_remain / (rel_found + est_rel_remain) < cutoff: 
                break

    # Now compute recall etc. for topic given that last rank
    total_rel = len(judgements[topic])
    rel_ret = sum(examined)
    recall = rel_ret / total_rel
    recall_stats[topic] = recall

    docs_examined = len(examined)
    total_docs = len(rankedDocsDoL[topic])
    effort = docs_examined / total_docs
    effort_stats[topic] = effort

    percent_rel = ( total_rel * 100 ) / total_docs
    # print("Topic {t} total_rel {o} total_docs {d} (percent: {p:3.2f}%)".format(t=topic, o=total_rel, d=total_docs, p = percent_rel))
    print("Topic {t}\tRecall {r:2.3f} Examined {e:2.3f}\t({o} / {d} = {p:3.2f}%)".format(t=topic, r=recall, e=effort,  o=total_rel, d=total_docs, p = percent_rel))

recall_avg = sum(recall_stats.values()) / len(recall_stats)
effort_avg = sum(effort_stats.values()) / len(effort_stats)
print("Averages:\tRecall {r:2.3f} Examined {e:2.3f}\n".format(r = recall_avg, e = effort_avg))
