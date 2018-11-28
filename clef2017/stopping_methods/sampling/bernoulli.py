import numpy as np
import matplotlib
#matplotlib.use('agg')
from matplotlib import pyplot as plt
import re
import os
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF,DotProduct,Matern, RationalQuadratic, ConstantKernel as C
from sklearn.utils.extmath import softmax
import itertools
from scipy.optimize import curve_fit
from scipy.special import expit
from scipy.stats.distributions import  t
from sklearn.gaussian_process.kernels import WhiteKernel, ExpSineSquared
import sys, getopt
import math
import random
import pandas as pd
import string
import decimal
from scipy.optimize import curve_fit
import pickle
from pathlib import Path
from sklearn.model_selection import train_test_split

#Class for reprsenting a topic
class record:
    def __init__(self, qId):
        self.queryId = qId
        self.docsReturned = []

    def addDoc(self, doc):
        self.docsReturned.append(doc)



#load test tests from qrel
def loadTestResults(file):
    records = {}
    with open(file) as content:
        lastId = "Start"

        for line in content:
            tabbed = re.split("\s", line)

            if lastId == tabbed[0]:
                records[lastId].addDoc(tabbed[2])

            else:
                lastId = tabbed[0]
                records[lastId] = record(lastId)
                records[lastId].addDoc(tabbed[2])

    return records






qrel = ""
files = []
sampleRate = 1
desiredRecall = 0.6
failedTopics = []
useCutOffOnFail = True

opts, args = getopt.getopt(sys.argv[1:],"hc:i:q:r:")

for opt, arg in opts:
    if opt == '-h':
        print ("-q qrel file, -i intgration file")
    elif opt in ("-q"):
        qrel_file = arg
    elif opt in ("-i"):
        files = arg.split('$')
    elif opt in ("-r"):
        runData = loadTestResults(arg)
        #loadrun(arg, qrel)



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


error = 0
numberOfDocs = 0
for x, filename in enumerate((os.listdir(files[0]))):
    #windows/mac/linux general way for loading file    
    data_folder = Path(files[0])
    file_to_open = data_folder / filename
    numberOfRel = None
    numberEstimate = 0
    numberOfDocs +=1

    #its a folder skip over
    if os.path.isdir(file_to_open):
        continue

    #particpants in the clef 2017 task
    #by default files will contain only sheffield run 2
    for file in files:
        
        data_folder = Path(file)
        file_to_open = data_folder / filename
        fileContent = open(file_to_open , "r").readlines()

        c = 0
        X = []
        scores = []
        for line in fileContent:
            c = c + sampleRate
            for val in re.split(r'\t+', line):
                if val == "\n":
                   continue

                else:
                    scores.append(float(val)) # y-axis
                    X.append(float(c))     # x-axis

        numberOfRel = max(scores)

    pointsToStop = []
    X_vals = np.array(range(0, len(scores)))

    splits = train_test_split(X_vals, test_size = 0.333)

    for i in splits[1]: 
        if runData[filename.split('.')[0]].docsReturned[i - 1] in judgements[filename.split('.')[0]]:
            numberEstimate +=1

    numberEstimate = len(scores) * (numberEstimate / len(splits[1]))
    error += ((numberOfRel - numberEstimate) ** 2)

    print(filename.split('.')[0], " Estimate:", str(numberEstimate), " True:", str(numberOfRel))

print("MSE: ", error/numberOfDocs)




        
         
    
    
