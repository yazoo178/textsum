import operator
import matplotlib.pyplot as plt
import math
import numpy as np
import sys, getopt
from matplotlib.legend_handler import HandlerLine2D

#import Image

# Script to visualise results from runs by plotting graphs showing the rate at which relevant 
# abstracts/documents were found
# 
# Author: Mark Stevenson
# Last updated: 1/6/2017    
#
# Usage: plot_runs.py -o output -q qrels

# qrel_file = "Training Data/qrel_abs_train"
# qrel_file = "Training Data/qrel_content_train"

#def usage():
#    print("plot_runs.py -o <run_file> -q <qrel_file>")
#    sys.exit()
#
#
#qrel_file = ''
#run_file = ''
#opts, args = getopt.getopt(sys.argv[1:],"ho:q:")
#for opt, arg in opts:
#    if opt == '-h':
#        usage()
#    elif opt in ("-o"):
#        run_file = arg
#    elif opt in ("-q"):
#        qrel_file = arg

#run_file = 'Output/Sheffield-run-4.5'
#run_file_2 = 'Output/Sheffield-run-4'
#qrel_file = 'qrel/qrel_abs_train'

run_file = 'Output/Test_Data_Sheffield-run-2.1'
run_file_2 = 'Output/Test_Data_Sheffield-run-2'
qrel_file = 'qrel/qrel_abs_test'

# Check arguments were parsed within problem
#if(run_file == '' or qrel_file == ''): 
#    usage()

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
        rel_count = 0
        docsFoundDoL[topic] = []
        last_topic = topic

    if(pid in judgements[topic]):
        rel_count = rel_count + 1

    # Store in list of running total of found documents
    docsFoundDoL[topic].append(rel_count)

###################################################
# Read through run output and create lists of number of documents found
docsFoundDoL_2 = {}
f = open(run_file_2, "r")

last_topic = "null"
topic_count = 0

for line in f:
    items = line.split()
    topic = items[0]
    pid = items[2]
    rank = items[3]

    if(topic != last_topic):
        rel_count = 0
        docsFoundDoL_2[topic] = []
        last_topic = topic

    if(pid in judgements[topic]):
        rel_count = rel_count + 1

    # Store in list of running total of found documents
    docsFoundDoL_2[topic].append(rel_count)
###################################################   
    
# Print out graphs
no_topics = len(docsFoundDoL)
rows = int(math.sqrt(no_topics))
cols = int(no_topics / rows)

fig, ax = plt.subplots(nrows=rows,ncols=cols,figsize=(20,15))
fig.subplots_adjust(wspace=0.3)
fig.subplots_adjust(hspace=0.7)

# Go through each topic (in order) and print graph
topic_count = 0
for topic in sorted(docsFoundDoL): 
    topic_count = topic_count + 1

    plt.subplot(rows, cols, topic_count)
    plt.title("Topic "+topic)

    # Check that there are some relevant documents - there's at least one otpic for which this is the case
    # Don't draw the graph if there are no relevant documents
    if docsFoundDoL[topic][-1] == 0:
        continue
    #baseline
    x = np.arange(0, docsFoundDoL[topic][-1], docsFoundDoL[topic][-1] / len(docsFoundDoL[topic]))
    #run 1
    y = np.array(docsFoundDoL[topic])
    #run 2
    z = np.array(docsFoundDoL_2[topic])

    # plt.xlabel('Rank')
    # plt.ylabel('Documents Found')
    plt.xticks(rotation=70)
#    plot1 = plt.plot(x,color='b', label = 'basline')
#    plot2 = plt.plot(y,color='r' , label = 'run')
#    plot3 = plt.plot(z,color='g' ,  label = 'enhancment')

#    plot1 = plt.plot(x,color='b')
#    plot2 = plt.plot(y,color='r')
#    plot3 = plt.plot(z,color='g')
#    plt.legend([plot1, plot2, plot3],['basline','run','enhancment'])
     
    plt.plot(x,color='b' , label = 'baseline')
    plt.plot(z,color='r' , label = 'run-4')
    plt.plot(y,color='g' , label = 'enhanc.')
    
    legend = plt.legend(loc='lower right', shadow=True)
    
#    plt.legend(handler_map={plot1: HandlerLine2D(numpoints=4)})


#plt.show()
# when saving, specify the DPI
plt.savefig("plot_test_4.4.png",bbox_inches='tight',dpi=100)
