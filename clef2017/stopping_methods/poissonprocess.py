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
#-i C:\Users\william\Documents\TextSum\clef2017\stopping_methods\Test_Data_Sheffield-run-2_int_scores_3$C:\Users\william\Documents\TextSum\clef2017\stopping_methods\B-rank-cost_int_scores_3$C:\Users\william\Documents\TextSum\clef2017\stopping_methods\run-2_int_scores_3$C:\Users\william\Documents\TextSum\clef2017\stopping_methods\run-1_int_scores_3$C:\Users\william\Documents\TextSum\clef2017\stopping_methods\run_fulltext_test_int_scores_3 -q C:\Users\william\Documents\TextSum\clef2017\qrel\qrel_abs_test


def nextTime(rateParameter):
    return -math.log(1.0 - random.random()) / rateParameter

def func(rate, x):
    return math.exp(-rate * x)


qrel = ""
files = []


opts, args = getopt.getopt(sys.argv[1:],"hc:i:q")

for opt, arg in opts:
    if opt == '-h':
        print ("-q qrel file, -i intgration file")
    elif opt in ("-q"):
        qrel = arg
    elif opt in ("-i"):
        files = arg.split('$')


sampleRate = 3
showtimeLine = True
showAllAtEnd = True
allPoints = []
labels =[]

#Loop every topic
for filename in os.listdir(files[0]):

    plots = []
    #its a folder skip over
    if os.path.isdir(files[0] + "\\" + filename):
        continue


    #all documents in sample
    for percentage in np.linspace(1, 1, 1):

        dist = 1
        plt.title("Topic Distributions")

        #loop every file in input paremter
        for file in files:

            #read file into memory
            scores = []
            X_samps = []
            c = 0
            fileContent = open(file + "\\" + filename , "r").readlines()

            for line in fileContent[0:int(len(fileContent) * percentage)]:
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
            
            #crates a sample distrubtion of data in following format:
            #x: 3, 18, 56, 91, 200, etc
            #y: 1, 2, 3, 4, 5, 6
            lastPoint = None
            for x, y in zip(X_samps, firstSet): 
                if lastPoint != y:
                    lastPoint = y
                    x_points.append(x)
                    y_points.append(y)


            #rate of documents parameter
            rateOfDocument = len(x_points) / len(X_samps)
            print("Estimated Rate of Document: " + str(rateOfDocument))
            allPoints.append(x_points)
            labels.append(filename)


            if showAllAtEnd:
                continue

            if showtimeLine:
                plt.ylim([0,10])
                plt.ylabel("Runs")
                plt.xlabel('Number of Documents in Rankings')
                plt.scatter(x_points, [dist for x in x_points], s=40, label=file.split('\\')[-1])
                dist = dist + 1
                plt.legend()

            else:
                plt.title(filename)
                x = np.linspace(0, len(fileContent) * sampleRate, len(fileContent) * sampleRate)
                y = np.array([func(rateOfDocument, X) for X in x])
                plt.plot(x, y, label=file.split('\\')[-1])
                plt.legend()

        if not showAllAtEnd:
            plt.show()


for count, element in enumerate(allPoints):

    #plt.ylim([0,10])
    plt.ylabel("Topics")
    plt.xlabel('Document Ranking')
    plt.scatter(element, [count for x in element], s=20, label=labels[count])
    plt.legend()

  
plt.show()

   




