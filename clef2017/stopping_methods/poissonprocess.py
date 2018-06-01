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

def nextTime(rateParameter):
    return -math.log(1.0 - random.random()) / rateParameter


qrel = ""
file = ""


opts, args = getopt.getopt(sys.argv[1:],"hc:i:q")

for opt, arg in opts:
    if opt == '-h':
        print ("-q qrel file, -i intgration file")
    elif opt in ("-q"):
        qrel = arg
    elif opt in ("-i"):
        file = arg



sampleRate = 3

for filename in os.listdir(file):
    scores = []
    X_samps = []
    c = 0

    #its a folder skip over
    if os.path.isdir(file + "\\" + filename):
        continue

    for line in open(file + "\\" + filename , "r"):
        c = c + sampleRate
        tmp = []
        for val in re.split(r'\t+', line):
            if val == "\n":
                continue

        #if float(line) not in scores:
            tmp.append(float(val))

        scores.append(np.array(tmp)) # y-axis
        X_samps.append(float(c))     # x-axis

    
    scores = np.rot90(scores)
    firstSet = scores[0]
    x_points = []
    y_points = []
    lastPoint = None

    for x, y in zip(X_samps, firstSet): 
       if lastPoint != y:
            lastPoint = y
            x_points.append(x)
            y_points.append(y)


    
    print(x_points)
    print(y_points)
    rateOfDocument = len(x_points) / len(X_samps)
    print("Estimated Rate of Document: " + str(rateOfDocument))
    

    exit()    




