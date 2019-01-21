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
from BaseRules import *


def non_hom_func(a, k, n, r):
    n = decimal.Decimal(n)
    k = decimal.Decimal(k)
    a = decimal.Decimal(a)
    r = decimal.Decimal(r)
    
    partOne = (((a / k) * ((decimal.Decimal(math.e) **(k * n)) - 1))**r) / stirling(r)

    try:
        
        partTwo = decimal.Decimal(math.e) **(-(a/k * ((decimal.Decimal( math.e) **(k * n) - 1))))
    except Error:
        raise Exception ('Cannot Compute, value too small')
    

    return decimal.Decimal(partOne * partTwo)



def stirling(n):
    return decimal.Decimal( (decimal.Decimal((math.sqrt(decimal.Decimal(2) * decimal.Decimal(math.pi) * n))) * ((n / decimal.Decimal(math.e)) ** n )))

# Ex function
def func_fit(x, a, k):
    return  a * np.exp(k*x)


qrel = ""
files = []

SAMPLE_RATE = 1
DES_RECALL = 0.7 #Desired Recall
DEGREE = 5 #Poly degree
WINDOW_SIZE = 50 #50 either side

pointsToStop = []

opts, args = getopt.getopt(sys.argv[1:],"hc:q:r:")

for opt, arg in opts:
    if opt == '-h':
        print ("-q qrel file -r run file")
    elif opt in ("-q"):
        qrel = arg
    elif opt in ("-r"):
        print(opt)
        runData = loadRunFile(arg)


#Create a window disribution file and a relevence index file.
#rel index maps topics to relevent document indices
#e.g 'CD004224 : [1, 15, 22, 37]'
#dist contains a rate value between 1/WINDOW_SIZE * 2 and 1.
#eg 'CD004224 : [0.31, 0.30, 0.29, 0.28]
if os.path.isfile('distbute_50.pickle') and os.path.isfile('rel_index.pickle') :
    dist =  pickle.load( open( "distbute_50.pickle", "rb" ))
    relIndexs = pickle.load( open( "rel_index.pickle", "rb" ))

else:
    dist, relIndexs =  calcMovingAverage(WINDOW_SIZE, qrel, runData)
    pickle.dump( dist, open( "distbute_50.pickle", "wb" ) )
    pickle.dump( relIndexs, open( "rel_index.pickle", "wb" ) )


#Loop every topic
for x, filename in enumerate(relIndexs):

    #filename = 'CD012019'
    print(filename)

    #print(filename)

    if not HasMoreThanNDocuments(dist[filename]):
        print("Skipping: ", filename)
        continue


    #fig = plt.figure(figsize=(10, 10)) # inches

    #Normalized values between 0 and 1 for all documents in collection
    X_vals = np.linspace(0, 1, len(dist[filename]))

    #loop from 10 to 100%
    for x in range(50, 110, 10):

        #Take percentage cut
        samplePercentage = 0.01 * x

        #Releavent Document Indexes. Real Values e.g [0, 15, 32, 71]
        x_points = relIndexs[filename][0: int(len( relIndexs[filename]) * samplePercentage)]

        #Rates at indexes relevant documents only
        y_distr = [dist[filename][x] for x in x_points]

        #Normalize x values between 0 and 1 for each index point. Relevent documents only
        x_points_norms = [X_vals[x] for x in x_points]

        #non rel y dist
        y_distr_non_rel = dist[filename][0:int(len( dist[filename]) * samplePercentage)]

        #non rel x points
        x_points_non_rel = X_vals[0:int(len( dist[filename]) * samplePercentage)]

        #a = 0.01, k = 0.02
        guess = (0.01, 0.2)

        #fit curve using relevent documents and rates only
        opt, pcov = curve_fit(func_fit, x_points, y_distr, guess, maxfev=10000)


        sum = 0
        n = 1

        while(True):

            try:
                sum+=non_hom_func(opt[0], opt[1], len(X_vals) , n) 
                n = n + 1

            except:
                n = len(X_vals)
                break

            if sum > 0.95:
                break

            if n >= len(X_vals):
                break


        #Check if the estimated number of documents is greater than the documents we have actually found
        if n * DES_RECALL <= len(x_points):
            pointsToStop.append(decimal.Decimal(DES_RECALL) * (n - x_points[-1]))
            break

        print(pointsToStop)



print(pointsToStop)
    

   




