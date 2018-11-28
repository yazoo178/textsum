
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
from scipy.optimize import curve_fit, least_squares
from scipy.stats import chisquare
from scipy.special import expit
from scipy.stats.distributions import  t
from sklearn.metrics import mean_squared_error

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
from sklearn.metrics import r2_score

dat =  pickle.load( open("testsse.pickle", "rb" ))
plt.plot(dat[0], label='10% Sample')
plt.plot(dat[1], label='20% Sample')
plt.plot(dat[2], label='30% Sample')
plt.plot(dat[3], label='40% Sample')
plt.legend(loc='best')
plt.xlabel("Window Sample Size")
plt.ylabel("Summed MSE over topics")
plt.show()
exit()



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


def calcMovingAverage(window, testFiles, records):

    queryIdToRelvDocs = {}
    distb = {}

    with open(testFiles, encoding='utf-8') as content:
        for line in content:
            tabbed = re.split('\s+', line)

            if tabbed[0] not in queryIdToRelvDocs:
                queryIdToRelvDocs[tabbed[0]] = []

            if '1' in tabbed[3].rstrip().strip():
                queryIdToRelvDocs[tabbed[0]].append(tabbed[2].rstrip().strip())



    for record in records:
        distb[record] = []
        
        for x in range(0, len(records[record].docsReturned)):

            start = x - window
            end = x + window
            relCount = 0

            if start < 0:
                windowSet = records[record].docsReturned[0:end]

            elif end >= len(records[record].docsReturned):
                windowSet = records[record].docsReturned[start:len(records[record].docsReturned) -1]

            else:
                windowSet = records[record].docsReturned[start:end]


            for element in windowSet:
                if element in queryIdToRelvDocs[record]:
                    relCount += 1

        
            extraMass = 1 / len(windowSet)

            distb[record].append( (relCount / len(windowSet)) + extraMass)


    return distb
        
                



#see notes from Mark

#a c0
#k c1
#r rth document

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


# Define form of function going to try to fit to curve
def func_fit(x, a, k):
    return  a * np.exp(k*x)


qrel = ""
files = []
sampleRate = 1
runData = None
desiredRecall = 0.6
loadedSamples = []
scoreAvg = []

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


for x in range(1, 101):
    name = "distbute_" + str(x) + ".pickle"
    dist =  pickle.load( open(name, "rb" ))
    loadedSamples.append(dist)



stoppingPoints = {}

sumRecalls = 0
sumEfforts = 0
sumRel = 0
number = 0
skip = 0



for scoreIndex, dist in enumerate(loadedSamples):

    scoreAvg.append({})

    #Loop every topic
    for x, filename in enumerate(os.listdir(files[0])):

        print(filename)

        #windows/mac/linux general way for loading file    
        data_folder = Path(files[0])
        file_to_open = data_folder / filename
    
        #its a folder skip over
        if os.path.isdir(file_to_open):
            continue


        #particpants in the clef 2017 task
        #by default files will contain only sheffield run 2
        for file in files:
        
            data_folder = Path(file)
            file_to_open = data_folder / filename
            fileContent = open(file_to_open , "r").readlines()

            #Load file into memory. c will is the current file element index
            #and will be updated based upon the sampling method
            #X will contain a value of the total number of relavent documents found at a given
            #index e.g 1,1,1,2,2,3,3,3,3,3,3,3,3,4,4...
        
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
        for x in range(10, 90, 10):



            #Take percentage cut
            samplePercentage = 0.01 * x
            scoresSamps = scores[0: int(len(scores) * samplePercentage)]
            X_samps = X[0: int(len(X) * samplePercentage)]


            x_points = []
            y_points = []
            lastPoint = None

            #to avoid a recentangular looking graph, just try the points where the value is different from the last
            for x2, y in zip(X_samps, scoresSamps):
                    if lastPoint != y:
                        lastPoint = y
                        x_points.append(x2 - 1)
                        y_points.append(y)



            #Make sure we have atleast two rel document
            if len(x_points) < 2:
                continue

            #rate distirubtion array
            x_distr = []

            #get the distribution for each point
            for index in x_points:

                #docElementId = runData[filename.split('.')[0]].docsReturned[int(index)]
                x_distr.append(dist[filename.split('.')[0]][int(index)])


    

            k = -0.01
            a = 0.2
            guess = (a, k)
            #attempt to fit curve

            opt, pcov = curve_fit(func_fit, x_points, x_distr, guess, maxfev=1000)
            a, k = opt

            pred = func_fit(X_vals, a, k)
            testSamps = []

            for y in x_points:
                testSamps.append(pred[int(y)])

            if str(x) in scoreAvg:
                scoreAvg[scoreIndex][str(x)] += mean_squared_error(np.array(x_distr), np.array(testSamps))

            else:
                scoreAvg[scoreIndex][str(x)] = mean_squared_error(np.array(x_distr), np.array(testSamps))




tens= []
twens = []
thir = []
fors = []

for x, scoreIndex in enumerate(scoreAvg):

    tens.append(scoreAvg[x]["10"])
    twens.append(scoreAvg[x]["20"])
    thir.append(scoreAvg[x]["30"])
    fors.append(scoreAvg[x]["40"])




pickle.dump([tens,twens,thir,fors], open( "testsse.pickle", "wb" ) )
plt.plot(tens)
plt.plot(twens)
plt.plot(thir)
plt.plot(fors)
plt.show()

    


