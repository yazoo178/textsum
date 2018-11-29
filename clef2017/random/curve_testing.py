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

out_pdf = 'C:\\Users\\william\\Documents\\graphs.pdf'
pdf = matplotlib.backends.backend_pdf.PdfPages(out_pdf)

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

        
            #extraMass = 1 / len(windowSet)
            extraMass = 0

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
desiredRecall = 0.6
failedTopics = []
useCutOffOnFail = True
degree = 5

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
        #loadrun(arg, qrel)


if os.path.isfile('distbute_50.pickle'):
    dist =  pickle.load( open( "distbute_50.pickle", "rb" ))
else:
    dist =  calcMovingAverage(50, qrel, runData)
    pickle.dump( dist, open( "distbute_50.pickle", "wb" ) )





#Loop every topic
for x, filename in enumerate((os.listdir(files[0]))):

    fig = plt.figure(figsize=(10, 10)) # inches
    print(filename)
    #filename = 'CD009519.txt'

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
    X_vals = np.array(range(1, len(scores)))
    

    #loop from 10 to 100%
    for x in range(100, 110, 10):

        #Take percentage cut
        samplePercentage = 0.01 * x
        scoresSamps = scores[0: int(len(scores) * samplePercentage)]
        X_samps = X[0: int(len(X) * samplePercentage)]


        x_points = []
        y_points = []
        lastPoint = None

        #get the true rel docs
        for x2, y in zip(X_samps, scoresSamps):
                if lastPoint != y:
                    lastPoint = y
                    x_points.append(x2 - 1)
                    y_points.append(y)



        #rate distirubtion array
        x_distr = []

        #get the distribution for each point
        for index in x_points:
            #docElementId = runData[filename.split('.')[0]].docsReturned[int(index)]
            x_distr.append(dist[filename.split('.')[0]][int(index)])


        k = 0.01
        a = 0.2

        guess = (a, k)

        opt, pcov = curve_fit(func_fit, x_points, x_distr, guess, maxfev=10000)

        z5 = polyfit(X_vals, dist[filename.split('.')[0]], degree)
        p5 = poly1d(z5)
        x_poly = p5(X_vals)

        #opt, pcov = curve_fit(func_fit, X_vals, dist[filename.split('.')[0]], guess, maxfev=10000)
        opt[1] = - abs(opt[1])
        pred = func_fit(X_vals, opt[0], opt[1])

        plt.scatter(X_vals, dist[filename.split('.')[0]])
        plt.scatter(x_points, x_distr, color='red')
        plt.plot(X_vals, pred, color='green' )
        plt.plot(X_vals, x_poly, color='black' )
        plt.title(filename.split('.')[0])
        plt.legend(['Curve Fit', 'Poly Fit ' +str(degree) + " Degree", 'Documents' ,'Relavant Documents'])

        #plt.scatter(x_distr, x_points)
        #plt.show()
        pdf.savefig(fig)

pdf.close()
    

   



