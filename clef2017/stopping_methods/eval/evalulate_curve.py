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


    for curveScore in open('./curve_scores/'+ curve_scores, 'r+'):
        y_p.append(float(curveScore))

    y_p = np.array(y_p)


    x_sam_val = find_nearest(y_p, max(y_p) * (rate / 100))
    x_val_true = findIn(int(round(max(scores) * (rate / 100))), scores)

    effort = ((len(scores) - x_sam_val) / sample_rate) / x_val_true

    recall = (scores[x_sam_val] / max(scores))
    return [recall, effort]





opts, args = getopt.getopt(sys.argv[1:],"hc:o:q:")
results = []
for opt, arg in opts:
    if opt == '-h':
        usage()
    elif opt in ("-r"):
        rate = int(arg)
    elif opt in ("-s"):
        sample_rate = int(arg)


print("Recalls:")
curve_scores = []
for filename in os.listdir('curve_scores/'):
    curve_scores.append(filename)

for i,filename in enumerate(os.listdir('intergrates_bin')):
    rSet = {}
    
    true_scores_file = open('intergrates_bin/' + filename , "r+")
    results = eval(true_scores_file, curve_scores[i], filename)

    rSet['recall'] = results[0]
    rSet['above ' + str(rate)] = float(rSet['recall']) < float(rate)
    rSet['effort'] = results[1]
    print(rSet)


    results.append(rSet)










