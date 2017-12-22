import operator
import matplotlib.pyplot as plt
import math
import numpy as np
import sys, getopt
from scipy.optimize import curve_fit

# Script to visualise results from runs by plotting graphs showing the rate at which relevant 
# abstracts/documents were found
# 
# Author: Mark Stevenson
# Last updated: 27/6/2017    
#
# Usage: fit_curves.py -o output -q qrels

def usage():
    print("plot_runs.py -c -o <run_file> -q <qrel_file>")
    sys.exit()


# Define form of function going to try to fit to curve
def model_func(x, a, k):
    return a * np.exp(-k*x)



qrel_file = ''
run_file = ''
opts, args = getopt.getopt(sys.argv[1:],"ho:q:")
for opt, arg in opts:
    if opt == '-h':
        usage()
    elif opt in ("-o"):
        run_file = arg
    elif opt in ("-q"):
        qrel_file = arg

# Check arguments were parsed within problem
if(run_file == '' or qrel_file == ''): 
    usage()

print("Run file is ", run_file)
print("Qrel file is ", qrel_file)
    


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
    if(qrel is "1"): 
        judgements[topic][pid] = qrel
f.close()

# Dict containing relevance counts 
rel_count = {}

# Read through run output and create lists of number of documents found
docsFoundDoL = {}
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
        last_topic = topic

    if(pid in judgements[topic]):
        docsFoundDoL[topic].append(1)
    else: 
        docsFoundDoL[topic].append(0)



# Print out graphs
no_topics = len(docsFoundDoL)
rows = int(math.sqrt(no_topics))
cols = int(no_topics / rows)

fig, ax = plt.subplots(nrows=rows,ncols=cols)
fig.subplots_adjust(wspace=0.3)
fig.subplots_adjust(hspace=0.7)

# Go through each topic (in order), normalise scales, attempt to fit funtion to it and print graph
topic_count = 0
for topic in sorted(docsFoundDoL): 
    topic_count = topic_count + 1
 
    plt.subplot(rows, cols, topic_count)
    plt.title("Topic "+topic)

    # Check that there are some relevant documents - there's at least one topic for which this is the case
    # Don't draw the graph if there are no relevant documents
    if sum(docsFoundDoL[topic]) == 0:
        continue

    # Transform lists (documents found -> proportion of documents
    # missing; documents examined -> proportion of documents examined)
    total_rel = sum(docsFoundDoL[topic])
    # print("Topic {t}, total_rel {d}".format(t= topic, d = total_rel))
    x = np.linspace(0, 1, num=len(docsFoundDoL[topic]))

    if 0: 
        perc_missing = 1
        y = []
        for i in range(0, len(docsFoundDoL[topic])):
            if docsFoundDoL[topic][i] == 1: 
                perc_missing -=  ( 1 / total_rel)
                if perc_missing < 0:   # Avoid value becoming (very slightly) negative
                    perc_missing = 0
                    y.append(perc_missing)

    y = []
    rel_total = sum(docsFoundDoL[topic])
    doc_total = len(docsFoundDoL[topic])
    window_width = 200
    for i in range(0, doc_total):
        lower = i - window_width
        if lower < 0: 
            lower = 0
        upper = i + window_width
        if upper > doc_total:
            upper = doc_total
        window = (upper + 1) - lower
        rel_prob = sum(docsFoundDoL[topic][lower:upper]) / window
        y.append(rel_prob)


    # Try to fit exponential curve to data
    fit_ratio = 0.33 # First N items use to model decay
    fit_docs = int(len(x) * fit_ratio)
    # print("fit_docs {f}".format(f=fit_docs))
    x_fit = x[0:fit_docs]
    y_fit = y[0:fit_docs]
    #x_fit = x
    #y_fit = y

    p0 = (0.3,5) # starting search coefs 
    # opt, pcov = curve_fit(model_func, x, y, p0)
    opt, pcov = curve_fit(model_func, x_fit, y_fit, p0)
    # a, k, b = opt
    a, k = opt

    # y2 = model_func(x, a, k, b)
    y2 = model_func(x, a, k)

    print("Topic {t} Fit. func: f(x) = {a:.3f} e^(-{k:.3f} x)".format(t = topic, a = a, k = k))

    # plt.xlabel('Rank')
    # plt.ylabel('Documents Found')
    plt.xticks(rotation=70)
    plt.plot(x, y)

    plt.plot(x, y2, label='Fit. func: f(x) = %.3f e^{-%.3f x}' % (a,k))

plt.show()


