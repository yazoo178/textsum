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
import matplotlib.backends.backend_pdf
from numpy import polyfit, poly1d
import numpy.polynomial.polynomial as poly
from methods import *
from sklearn.model_selection import train_test_split
from BaseRules import *

def process(rate, k):

    if k == 0:
        return ((decimal.Decimal(rate) ** decimal.Decimal(k)) * (decimal.Decimal(math.e) ** decimal.Decimal(-rate))) / math.factorial(decimal.Decimal(k))

    return ((decimal.Decimal(rate) ** decimal.Decimal(k)) * (decimal.Decimal(math.e) ** decimal.Decimal(-rate))) / stirling(decimal.Decimal(k))


def stirling(n):
    return decimal.Decimal( (decimal.Decimal((math.sqrt(decimal.Decimal(2) * decimal.Decimal(math.pi) * n))) * ((n / decimal.Decimal(math.e)) ** n )))

def hom_func(rate, D, r):
    rate = decimal.Decimal(rate)
    D = decimal.Decimal(D)
    r = decimal.Decimal(r)

    if r == 0:
        return (((rate*D)**r) / math.factorial(r)) * decimal.Decimal(math.e)**(-rate*D) 

    return (((rate*D)**r) / stirling(r)) * decimal.Decimal(math.e)**(-rate*D) 

qrel = ""
files = []

SAMPLE_RATE = 1
DES_RECALL = 0.7 #Desired Recall
DEGREE = 5 #Poly degree
WINDOW_SIZE = 50 #50 either side
SAMPLE_SIZE = 1 / 3
pointsToStop = []

DOCUMENTS_NEEDED = 0.95
REL = 0.95

opts, args = getopt.getopt(sys.argv[1:],"hc:q:r:i:")

for opt, arg in opts:
    if opt == '-h':
        print ("-q qrel file -r run file")
    elif opt in ("-q"):
        qrel = arg
    elif opt in ("-r"):
        runData = loadRunFile(arg)
    elif opt in ("-i"):
        DOCUMENTS_NEEDED = float(arg) / 100



def setRunData(data):
    return loadRunFile(data)
    
def setDocsNeeded(docs):
    return float(docs) / 100
    
def setQrel(_qrel):
    qrel = _qrel

def runPEM(data, docsNeeded, _qrel):

    runData = data
    DOCUMENTS_NEEDED = docsNeeded
    qrel = _qrel
    
    #Create a window disribution file and a relevence index file.
    #rel index maps topics to relevent document indices
    #e.g 'CD004224 : [1, 15, 22, 37]'
    #dist contains a rate value between 1/WINDOW_SIZE * 2 and 1.
    #eg 'CD004224 : [0.31, 0.30, 0.29, 0.28]
    if os.path.isfile('test_distbute_50.pickle') and os.path.isfile('test_rel_index.pickle') :
        print('here')
        dist =  pickle.load( open( "test_distbute_50.pickle", "rb" ))
        relIndexs = pickle.load( open( "test_rel_index.pickle", "rb" ))
    
    else:
        dist, relIndexs =  calcMovingAverage(WINDOW_SIZE, qrel, runData)
        pickle.dump( dist, open( "test_distbute_50.pickle", "wb" ) )
        pickle.dump( relIndexs, open( "test_rel_index.pickle", "wb" ) )
    
    
    effortSumWeighted = 0 #total weighted effort
    totalDocuments = 0 #total documents in all topics
    recallSumWeighted = 0
    relSumWeighted = 0
    topics = 0
    
    #Loop every topic
    for x, filename in enumerate(relIndexs):
    
    
        if not HasMoreThanNDocuments(dist[filename]):
            print("Skipping: ", filename)
            continue
    
        #Normalized values between 0 and 1 for all documents in collection
        X_vals = np.linspace(0, 1, len(dist[filename]))
        topics +=1
        #get test and train
        splits = train_test_split([x for x in range(0, len(dist[filename]))], test_size = SAMPLE_SIZE)
        
        numberFound = 0
    
        #number in sample
        for i in splits[1]: 
            if i in relIndexs[filename]:
                numberFound +=1
    
        numberEstimate = numberFound / len(splits[1])
    
        #print(filename + ": Rate of Rel Document: 1 Every "  + str(numberEstimate) + " Documents in Document Collection size of " + str(len(X_vals)))
    
        if numberFound == 0:
            continue
    
        prob = 0
        numberNeededForRecall = 0
        for x in range(0, len(X_vals)):
            prob += hom_func(numberEstimate, len(X_vals), x)
    
            if prob >= DOCUMENTS_NEEDED:
                numberNeededForRecall = x
                break
       
        found = numberFound
        lookedAt = 0
        effort = SAMPLE_SIZE
        recall = numberFound / len(relIndexs[filename])
        #loop ranking set
        for x, i in enumerate(runData[filename].docsReturned):
    
            #already in split set, ignore
            if x in splits[1]:
                continue
    
            lookedAt +=1
    
            effort += 1/len(X_vals)
    
            if x in relIndexs[filename]:
                found +=1
                recall += (1 / len(relIndexs[filename]))
    
            if found >= numberNeededForRecall:
                lookedAt = x
                break
        
        if recall > REL:
            relSumWeighted += 1
            
        print("effort: ", effort, "recall: ", recall, "Relaible:", recall > REL)
        effortSumWeighted += effort * len(X_vals)
        recallSumWeighted += recall * len(X_vals)
        totalDocuments += len(X_vals)
    
    print("")
    effort = effortSumWeighted / totalDocuments
    recall = recallSumWeighted / totalDocuments
    relabi = relSumWeighted / topics
    
    print("Effort: ", effort)
    print("Recall: ", recall)
    print("Relabiltiy: ", relabi)
    
    return effort, recall, relabi
    
    


