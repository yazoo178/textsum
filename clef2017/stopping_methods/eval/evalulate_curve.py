import operator
import matplotlib.pyplot as plt
import math
import numpy as np
import sys, getopt
import random
import os
import re
#-k 10 -o Output/Test_Data_Sheffield-run-2 -q qrel/qrel_abs_test

def usage():
    sys.exit()



qrel_file = ''
run_file = ''
cutoff = ''
true_scores_file = ''
rate = 70
sample_rate = 3


def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

def findIn(score, x):
    for ind, x1 in enumerate(x):
        if score == x1:
            return ind

def eval(true_scores_file, curve_scores, filename):

    y_p = []
    scores = []
    X_samps = []

    
    c = 0
    for line in true_scores_file:
        c = c + sample_rate
        for val in re.split(r'\t+', line):
            if val == "\n":
              continue
          #if float(line) not in scores:

        scores.append(int(val))
        X_samps.append(float(c))


    for curveScore in open('./curve_scores/' + mode + "/" + curve_scores, 'r+'):
        y_p.append(float(curveScore))

    y_p = np.array(y_p)


    x_sam_val = find_nearest(y_p, max(y_p) * (rate / 100))
    x_val_true = findIn(int(round(max(scores) * (rate / 100))), scores)

    effort =  (((len(scores) - x_sam_val)/ sample_rate) + x_sam_val) / len(scores) 

    recall = (scores[x_sam_val] / max(scores))
    return [recall, effort, len(scores), max(scores)]





opts, args = getopt.getopt(sys.argv[1:],"hc:o:q:")
dictResults = []
mode = "lin"

for opt, arg in opts:
    if opt == '-h':
        usage()
    elif opt in ("-r"):
        rate = int(arg)
    elif opt in ("-s"):
        sample_rate = int(arg)


print("Recalls:")
curve_scores = []
for filename in os.listdir('curve_scores/' + mode + "/"):
    curve_scores.append(filename)

for i,filename in enumerate(os.listdir('intergrates_bin')):
    rSet = {}
    
    true_scores_file = open('intergrates_bin/' + filename , "r+")
    results = eval(true_scores_file, curve_scores[i], filename)

    rSet['recall'] = results[0]
    rSet['above ' + str(rate)] = float(rSet['recall']) > (float(rate) / 100)
    rSet['effort'] = results[1]
    rSet['docs'] = results[2]
    rSet['rels'] = results[3]

    print(rSet)


    dictResults.append(rSet)

f = open(mode + '_results_' + str(rate) + "_" + str(sample_rate) +".csv", "w")
f.write("recall" + "," + "above " + str(rate) + "," + "effort" + "," "number of docs" + "," + "number of relevant" + "\n")



sums = []
sums.append(0)
sums.append(0)
sums.append(0)

for element in dictResults:
    f.write(str(element['recall']) + "," + str(element['above ' + str(rate)]) + "," + str(element['effort']) + "," + str(element['docs']) + "," +  str(element['rels']))
    sums[0]+=element['recall']
    sums[1]+=  int(element['above ' + str(rate)])
    sums[2]+=element['effort']
    f.write('\n')

f.write('\n')
f.write(str(sums[0] / len(dictResults)) + "," + str(float(sums[1] / len(dictResults))) + "," + str(sums[2] / len(dictResults)))

f.close()










