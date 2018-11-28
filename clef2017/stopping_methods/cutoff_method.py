import operator
import matplotlib.pyplot as plt
import math
import numpy as np
import sys, getopt
import random


CONFIDENCE = 0.05  # Confidence level if using flexible cutoffs


def usage():
    sys.exit()


def eval(scoreCounts, judgements, cutoffs, rankedDocsDoL):

    totalRecall = 0
    totalEffort = 0
    relieability = 0
    for key in judgements:
        recall = scoreCounts[key] / len(judgements[key])
        effort = cutoffs[key] / len(rankedDocsDoL[key])
        #print("Recall:{0} \t Effort{1}".format(recall, effort))

        totalRecall+=recall
        totalEffort+=effort
        
        if recall > 0.7:
            relieability+=1

    averageRecall = totalRecall / len(rankedDocsDoL)
    averageEffort = totalEffort / len(rankedDocsDoL)
    relieability = relieability / len(rankedDocsDoL)

    return("{0}\t{1}\t{2}".format(averageRecall, relieability, averageEffort))



     



qrel_file = ''
run_file = ''
target = ''
cutoff = ''
approach = "undefined"
min = 1
starPoint = None

opts, args = getopt.getopt(sys.argv[1:],"hk:c:o:q:m:s:")
for opt, arg in opts:
    if opt == '-h':
        usage()
    elif opt in ("-o"):
        run_file = arg
    elif opt in ("-m"):
        min = float(arg)
    elif opt in ("-q"):
        qrel_file = arg
        approach = "target"
    elif opt in ("-c"):
        cutoff = float(arg)
        approach = "cutoff"
    elif opt in ("-s"):
        starPoint = int(arg) - 1
        if starPoint < 0:
            exit("starting point must be > 1")
        


# Check arguments were parsed without problem and work out which
# approach being used
if(run_file == '' or qrel_file == '' or approach == "undefined"): 
    usage()

# Print out info about which approach being run
#print("Run file is ", run_file)
#print("Qrel file is ", qrel_file)
if approach == "target": 
    pass
    #print("Using target method (target of {t})".format(t = target))
elif approach == "cutoff":
    pass
   # print("Using flexible cutoff method (cutoff of {c}, p < {p})".format(c = cutoff, p = CONFIDENCE))


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
    score = items[4]

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
    rankedDocsDoL[topic].append({'pid' : pid, 'score' : score})



def run():
    recall_stats = {}
    effort_stats = {}

    cutoffs = {}


    for topic in rankedDocsDoL:
        lastScore = 0

        #min docus to look at for this topic
        minDocs = int(float(len(rankedDocsDoL[topic])) * min)

        for x, study in enumerate(rankedDocsDoL[topic]):
            score = study['score']

            if cutoff == 0:
                if x >= minDocs:
                    cutoffs[topic] = x
                    break

            else:
                #always look at one document
                if x == 0:
                    lastScore = score
                    continue

                #if our simularity score has reached 0 then end
                if float(lastScore) == 0.0:
                    cutoffs[topic] = len(rankedDocsDoL[topic])
                    break

                if starPoint is not None:
                    topDoc = (float(rankedDocsDoL[topic][starPoint]['score']))
                    decrase = topDoc - float(lastScore)
                    dif  = decrase / topDoc 

                    

                else:
                    #calculate the dif between current score and last score
                    decrase = (float(lastScore)  - float(score))
                    dif  = decrase / (float(lastScore))


                #if difference is greater than cut off then break. 
                if dif >= cutoff and x >= minDocs:
                    cutoffs[topic] = x
                    break

                if x + 1 == len(rankedDocsDoL[topic]):
                    cutoffs[topic] = len(rankedDocsDoL[topic])
                    break

                lastScore = score
        
        
    scoreCounts = {}

    for cut in cutoffs:
        subset = rankedDocsDoL[cut][0:cutoffs[cut]]
        scoreCounts[cut] = 0

        for doc in subset:
            docId = doc['pid']

            if doc['pid'] in judgements[cut]:
                scoreCounts[cut] +=1


    score = eval(scoreCounts, judgements, cutoffs, rankedDocsDoL)
    return score


#results = open('output_cutoff_sim.txt', "w")
scores = run()
print(scores)
exit()

for x in range(1, int(cutoff * 10000) + 1):
    cutoff = (x / 10000)
    scores = run()
    results.write(scores + "\n")
    results.flush()
    


