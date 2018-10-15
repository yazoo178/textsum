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
from pathlib import Path
import math

from scipy.optimize import curve_fit

def func(rateParameter, k, n):
    n = decimal.Decimal(n)
    k = decimal.Decimal(k)
    rateParameter = decimal.Decimal(rateParameter)
    return ((((rateParameter * k) ** n) / (stirling(n)) * (decimal.Decimal(math.e) ** (-rateParameter * k))))

def stirling(n):

    return decimal.Decimal( (decimal.Decimal((math.sqrt(decimal.Decimal(2) * decimal.Decimal(math.pi) * n))) * ((n / decimal.Decimal(math.e)) ** n )))


# Define form of function going to try to fit to curve
def curve_fit_test(x, a, k):
    return  a * np.exp(-k*x)


qrel = ""
files = []
sampleRate = 1
desiredRecall = 0.7


opts, args = getopt.getopt(sys.argv[1:],"hc:i:q")

for opt, arg in opts:
    if opt == '-h':
        print ("-q qrel file, -i intgration file")
    elif opt in ("-q"):
        qrel = arg
    elif opt in ("-i"):
        files = arg.split('$')





stoppingPoints = {}

sumRecalls = []
sumEfforts = []
sumRel = []
number = 0

for k in range(1, 10):
    sumEfforts.append(0)
    sumRecalls.append(0)
    sumRel.append(0)
    

#Loop every topic
for filename in os.listdir(files[0]):

    data_folder = Path(files[0])
    file_to_open = data_folder / filename
    
    #its a folder skip over
    if os.path.isdir(file_to_open):
        continue

    number = number + 1

    for file in files:

        data_folder = Path(file)
        file_to_open = data_folder / filename
        
        fileContent = open(file_to_open, "r").readlines()
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

    for x in range(1, 10):
    
        samplePercentage = 0.1 * x
        scoresSamps = scores[0: int(len(scores) * samplePercentage)]
        X_samps = X[0: int(len(X) * samplePercentage)]
        k = len(scores)
        ns = set(scoresSamps)
        rate = scoresSamps[-1] / len(scoresSamps)
        
        opt, pcov = curve_fit(curve_fit_test, X_samps, scoresSamps , maxfev=1000)
        x_pred = curve_fit_test(opt, X_samps)

        sum = 0
        n = 1

        x_points = []
        y_points = []
        lastPoint = None

        #to avoid a recentangular looking graph, just try the points where the value is different from the last
        for x2, y in zip(X_samps, scoresSamps):
                if lastPoint != y:
                    lastPoint = y
                    x_points.append(x2)
                    y_points.append(y)


        opt, pcov = curve_fit(curve_fit_test, x_points, y_points)
        a, k = opt
        x_pred = curve_fit_test(np.array(X), a, k)

        plt.plot(X, x_pred)
        plt.show()
        continue


        while(True):

            sum+=(func(rate, k, n))
            n = n + 1
        
            if sum > 0.95:
                break
       
        pointsToStop.append(decimal.Decimal(desiredRecall) * (n - decimal.Decimal(scoresSamps[-1])))
        
    exit()
    sumRel.append(0)
    
    for x, number_to_find in enumerate(pointsToStop):
        rank = ((x + 1) * 0.1) * len(scores)
        # print(x, " ", rank, " ", end="")

        
        relevant_in_sample = scores[int(rank)]        
        for r in range(int(rank), len(scores)):
            rank = r
            if scores[r] == relevant_in_sample + int(math.ceil((number_to_find))):
                break        
        
        # rank = scores[int(((x + 1) / 10) * len(scores) +  int(interval))]
        # print(rank)

        #calculate the recall by dividing the stopping point by the last score value
        sumRecalls[x] +=  scores[int(rank)] / scores[-1]
        sumEfforts[x] += rank / len(scores)

        if scores[int(rank)] / scores[-1] >= desiredRecall:
            sumRel[x] = sumRel[x] + 1
            
#sample 10 percent, make predection 
for x in range(1, 10):
    print("Recall at:" + str(10 * x) + "%" + "::" + str(sumRecalls[x - 1] / number))
    print("Effort at:" + str(10 * x) + "%" + "::" + str(sumEfforts[x - 1] / number))
    print("Reliability at:" + str(10 * x) + "%" + "::" + str(sumRel[x - 1] / number))
    print("")



#Sample 10 every 
        
    



