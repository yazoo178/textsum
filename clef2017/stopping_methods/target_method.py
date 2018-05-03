import operator
import matplotlib.pyplot as plt
import math
import numpy as np
import sys, getopt
import random

# Script to implement Cormack and Grossman (2016) method for determining
# when to stop examining documents for systematic reviews 
# reviews
# Script also extended to implememts "cutoff" method which estimates total 
# number of relevant document (based on percentage of sampled documents that 
# are relevant and number of documents yet to be examined)
#
# Author: Mark Stevenson
# Last updated: 25/3/2018
#
# Usage: target_method.py -o output -q qrels

CONFIDENCE = 0.05  # Confidence level if using flexible cutoffs


def usage():
    print("target_method.py -k INT -c THRESHOLD -o <run_file> -q <qrel_file>\n")
    print("-k option uses simple target method (Cormack and Grossman, 2016)")
    print("\te.g. target_method.py -k 10 continues until 10 relevant documents have been found\n")
    print("-c option uses flexible threshold")
    print("\te.g. target_method.py -c 0.1 continues until estimated that fewer than 10% of relevant documents remain\n")
    print("If both options defined in command line then last one mentioned gets used")
    sys.exit()


qrel_file = ''
run_file = ''
target = ''
cutoff = ''
approach = "undefined"
opts, args = getopt.getopt(sys.argv[1:],"hk:c:o:q:m:")
for opt, arg in opts:
    if opt == '-h':
        usage()
    elif opt in ("-o"):
        run_file = arg
    elif opt in ("-q"):
        qrel_file = arg
    elif opt in ("-k"):
        target = int(arg)
        approach = "target"
    elif opt in ("-c"):
        cutoff = float(arg)
        approach = "cutoff"

# Check arguments were parsed without problem and work out which
# approach being used
if(run_file == '' or qrel_file == '' or approach == "undefined"): 
    usage()

# Print out info about which approach being run
print("Run file is ", run_file)
print("Qrel file is ", qrel_file)
if approach == "target": 
    print("Using target method (target of {t})".format(t = target))
elif approach == "cutoff":
    print("Using flexible cutoff method (cutoff of {c}, p < {p})".format(c = cutoff, p = CONFIDENCE))


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
        rel_count = 0
        docsFoundDoL[topic] = []
        rankedDocsDoL[topic] = []
        last_topic = topic

    # Code to create graph of output - might as well keep this here for now
    if(pid in judgements[topic]):
        rel_count = rel_count + 1

    # Store in list of running total of found documents
    docsFoundDoL[topic].append(rel_count)
    # Store in list of ranked documents
    rankedDocsDoL[topic].append(pid)

# Run target method for each topic
recall_stats = {}
effort_stats = {}

for topic in sorted(rankedDocsDoL):
    # Create randomised list of ranks (simplifies sampling without replacement)
    total_docs = len(rankedDocsDoL[topic])
    ranks = list(range(0, len(rankedDocsDoL[topic])))
    random_ranks = random.sample(ranks, len(ranks))

    rel_found = 0       # Number of relevant documents found
    last_ranked = 0     # Rank of last relevant document found
    docs_sampled = 0    # Number of documents that have been looked at 
    for i in random_ranks:
        docs_sampled += 1
        # Check whether document is relevant
        if rankedDocsDoL[topic][i] in judgements[topic]:
            rel_found += 1
            if i > last_ranked:
                last_ranked = i
                 
            # Simple target method (i.e. continue until found k relevant)       
            if approach == "target": 
                if rel_found == target: 
                    break
           
            # Cutoff method 
            if approach == "cutoff":
                # Computes the estimated cutoff and stops when falls below set 
                # threshold 95% CI estimate for R (total number of relevant 
                # documents) 
                # (1) estimate total number of relevant documents (with 
                # confidence interval) 
                est_prob_rel = rel_found / docs_sampled +  (2 * math.sqrt(0.25 / docs_sampled))
                est_total_rel = ( est_prob_rel * total_docs )
                # print("Rank {i} rel_found {r} docs_examined {d} est_prob_rel {t}".format(i = i, r = rel_found, d = docs_examined, t = est_prob_rel))
                # (2) Use that estimate to estimate how many of the relevant 
                # documents have already been seen
                if rel_found < est_total_rel: 
                    cutoff_est = math.log(CONFIDENCE) / ( est_total_rel * math.log(1 - (rel_found / est_total_rel)))
                    # print("Rank {i} cutoff {c}".format(i = i, c = cutoff_est))
                    if cutoff_est < cutoff: 
                        break


    # Compute recall, i.e. how many of the relevant documents would be returned
    # if exmained everything up to last_rank
    total_rel = len(judgements[topic])
    rel_ret = 0
    for i in range(0, last_ranked+1): 
        if rankedDocsDoL[topic][i] in judgements[topic]:
            rel_ret += 1
    recall = rel_ret / total_rel
    recall_stats[topic] = recall

    total_docs = len(rankedDocsDoL[topic])

    # Compute effort (== total number of documents that had to be examined)
    # Calculate as everything up to last ranked plus all sampled documents 
    # with rank > last_rank
    total_docs_examined = last_ranked
    for i in random_ranks[:last_ranked]: 
        if(i > last_ranked):
            total_docs_examined += 1

    effort = total_docs_examined / total_docs
    effort_stats[topic] = effort

    # Compute some stats about topic for information
    percent_rel = ( total_rel * 100 ) / total_docs
    # print("Topic {t} total_rel {o} total_docs {d} (percent: {p:3.2f}%)".format(t=topic, o=total_rel, d=total_docs, p = percent_rel))
    print("Topic {t}\tRecall {r:2.3f}  Effort {e:2.3f}\t({o} / {d} = {p:3.2f}%)".format(t=topic, r=recall, e=effort,  o=total_rel, d=total_docs, p = percent_rel))

aboveN = [x for x in recall_stats.values() if float(x) > 0.7]
print("Reliability:" + str(len(aboveN)/ len(recall_stats)))
recall_avg = sum(recall_stats.values()) / len(recall_stats)
effort_avg = sum(effort_stats.values()) / len(effort_stats)
print("Averages:\tRecall {r:2.3f}  Effort {e:2.3f}\n".format(r = recall_avg, e = effort_avg))

