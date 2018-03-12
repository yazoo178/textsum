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

    recall = (scores[x_sam_val] / max(scores))
    print(filename + ":" + str(recall))





opts, args = getopt.getopt(sys.argv[1:],"hc:o:q:")
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
    true_scores_file = open('intergrates_bin/' + filename , "r+")
    eval(true_scores_file, curve_scores[i], filename)










