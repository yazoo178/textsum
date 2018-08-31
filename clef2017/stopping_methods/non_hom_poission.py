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

#calculates a distribution accross a window
#eg how many releavent documents occur within a window of 10

def calcDistirubtion(window, testFiles, records):
    found = False
    header = True
    qId = ""
    lastId = "Start"
    queryIdToRelvDocs = {}

    with open(testFiles, encoding='utf-8') as content:
        for line in content:
            tabbed = re.split('\s+', line)

            if tabbed[0] not in queryIdToRelvDocs:
                queryIdToRelvDocs[tabbed[0]] = []

            if '1' in tabbed[3].rstrip().strip():
                queryIdToRelvDocs[tabbed[0]].append(tabbed[2].rstrip().strip())


        QueiresToDist = {}
        for record in records:
            
            QueiresToDist[record] = {}
            for index in range(0, len(records[record].docsReturned)):
                vals = []
                deceptor = 0
                QueiresToDist[record][records[record].docsReturned[index]] = 0
                for x in range(0 - window, window + 1):
                    
                    newIndex = index + x
                    if newIndex < 0 or newIndex >= len(records[record].docsReturned):
                        deceptor+=1
                        continue

                    else:
                        if records[record].docsReturned[newIndex] in queryIdToRelvDocs[record]:
                            QueiresToDist[record][records[record].docsReturned[index]] +=1


                QueiresToDist[record][records[record].docsReturned[index]] = (QueiresToDist[record][records[record].docsReturned[index]]) / ((window * 2) + 1 - deceptor)

    return QueiresToDist



#see notes from Mark
def non_hom_func(a, k, r, n, l):
    n = decimal.Decimal(n)
    k = decimal.Decimal(k)
    a = decimal.Decimal(a)
    r = decimal.Decimal(r)
    l = decimal.Decimal(l)

    return ((((a / k) * math.exp(k * n) - l) ** r) / math.factorial(r)) * math.exp(-(a/k) *(math.exp(k * n) - l))



def stirling(n):
    return decimal.Decimal( (decimal.Decimal((math.sqrt(decimal.Decimal(2) * decimal.Decimal(math.pi) * n))) * ((n / decimal.Decimal(math.e)) ** n )))


# Define form of function going to try to fit to curve
def func_fit(x, a, k):
    return  a * np.exp(k*x)


qrel = ""
files = []
sampleRate = 1
runData = None

opts, args = getopt.getopt(sys.argv[1:],"hc:i:q:r:")

for opt, arg in opts:
    if opt == '-h':
        print ("-q qrel file, -i intgration file")
    elif opt in ("-q"):
        qrel = arg
    elif opt in ("-i"):
        files = arg.split('$')
    elif opt in ("-r"):
        runData = loadTestResults(arg)


if os.path.isfile('distbute_10.pickle'):
    dist =  pickle.load( open( "distbute_10.pickle", "rb" ))
else:
    dist =  calcDistirubtion(10, qrel, runData)
    pickle.dump( dist, open( "distbute_10.pickle", "wb" ) )




stoppingPoints = {}

sumRecalls = []
sumEfforts = []
number = 0

for k in range(1, 10):
    sumEfforts.append(0)
    sumRecalls.append(0)

#Loop every topic
for filename in os.listdir(files[0]):


    #its a folder skip over
    if os.path.isdir(files[0] + "\\" + filename):
        continue

    number = number + 1

    for file in files:
        fileContent = open(file + "\\" + filename , "r").readlines()
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

    pointsToStop = []
    X_vals = np.array(range(0, len(scores)))



    #loop from 10 to 100%
    for x in range(1, 10):
    
        samplePercentage = 0.1 * x
        scoresSamps = scores[0: int(len(scores) * samplePercentage)]
        X_samps = X[0: int(len(X) * samplePercentage)]


        x_points = []
        y_points = []
        lastPoint = None

        #to avoid a recentangular looking graph, just try the points where the value is different from the last
        for x2, y in zip(X_samps, scoresSamps):
                if lastPoint != y:
                    lastPoint = y
                    x_points.append(x2)
                    y_points.append(y)


        #rate distirubtion array
        x_distr = []

        #get the distribution for each point
        for index in x_points:

            docElementId = runData[filename.split('.')[0]].docsReturned[int(index)]
            x_distr.append(dist[filename.split('.')[0]][docElementId])

        x_points = x_distr

        print(x_points)
        print(y_points)

        #attempt to fit curve
        opt, pcov = curve_fit(func_fit, x_points, y_points, maxfev=1000)
        a, k = opt
        y2 = func_fit(X_vals, a, k)



        plt.plot(X_vals, y2)
        plt.show()




        break
    
    break



