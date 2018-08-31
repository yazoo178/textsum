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

def func(rateParameter, k, n):
    n = decimal.Decimal(n)
    k = decimal.Decimal(k)
    rateParameter = decimal.Decimal(rateParameter)
    return ((((rateParameter * k) ** n) / (stirling(n)) * (decimal.Decimal(math.e) ** (-rateParameter * k))))

def stirling(n):

    return decimal.Decimal( (decimal.Decimal((math.sqrt(decimal.Decimal(2) * decimal.Decimal(math.pi) * n))) * ((n / decimal.Decimal(math.e)) ** n )))


# Define form of function going to try to fit to curve
def curve_fit(x, a, k):
    return  a * np.exp(-k*x)


qrel = ""
files = []
sampleRate = 1

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

    for x in range(1, 10):
    
        samplePercentage = 0.1 * x
        scoresSamps = scores[0: int(len(scores) * samplePercentage)]
        X_samps = X[0: int(len(X) * samplePercentage)]
        k = len(scores)
        ns = set(scoresSamps)
        rate = scoresSamps[-1] / len(scoresSamps)

        sum = 0
        n = 1
        while(True):

            sum+=(func(rate, k, n))
            n = n + 1
        
            if sum > 0.95:
                break

        
        pointsToStop.append(decimal.Decimal(0.7) * (n - decimal.Decimal(scoresSamps[-1])))
        


    for x, interval in enumerate(pointsToStop):
        point = scores[int(((x + 1) / 10) * len(scores) +  int(interval))]
        sumRecalls[x] +=  point / scores[-1]
        sumEfforts[x] += ((int(((x + 1) / 10) * len(scores) +  int(interval))) / len(scores))

        #print("Recall: " + str(point / scores[-1]))
        #print("Effort: " + str((int(((x + 1) / 10) * len(scores) +  int(interval))) / len(scores)))
    


for x in range(1, 10):
    print("Recall at:" + str(10 * x) + "%" + "::" + str(sumRecalls[x - 1] / number))
    print("Effort at:" + str(10 * x) + "%" + "::" + str(sumEfforts[x - 1] / number))
    print("")



        
    



