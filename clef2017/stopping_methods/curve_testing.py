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


out_pdf = 'C:\\Users\\william\\Documents\\graphs.pdf'
pdf = matplotlib.backends.backend_pdf.PdfPages(out_pdf)

# Ex function
def func_fit(x, a, k):
    return  a * np.exp(k*x)


qrel = ""
files = []

SAMPLE_RATE = 1
DES_RECALL = 0.6 #Desired Recall
DEGREE = 5 #Poly degree
WINDOW_SIZE = 50 #50 either side

opts, args = getopt.getopt(sys.argv[1:],"hc:q:r:")

for opt, arg in opts:
    if opt == '-h':
        print ("-q qrel file -r run file")
    elif opt in ("-q"):
        qrel = arg
    elif opt in ("-r"):
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

    print(filename)

    #fig = plt.figure(figsize=(10, 10)) # inches

    #Normalized values between 0 and 1 for all documents in collection
    X_vals = np.linspace(0, 1, len(dist[filename]))

    #loop from 10 to 100%
    for x in range(50, 110, 10):

        fig = plt.figure(figsize=(10, 10)) # inches

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
        opt, pcov = curve_fit(func_fit, x_points_non_rel, y_distr_non_rel, guess, maxfev=10000)

        z5 = polyfit(X_vals, dist[filename], DEGREE)
        p5 = poly1d(z5)
        x_poly = p5(X_vals)

        #predict everything
        pred = func_fit(X_vals, opt[0], opt[1])     

        #Plot all true document rates
        plt.scatter(X_vals, dist[filename])

        #plot all relevent document rates
        plt.scatter(x_points_norms, y_distr, color='red')

        #plot exp curve predictions
        plt.plot(X_vals, pred, color='green' )

        #plot poly curve prediction
        plt.plot(X_vals, x_poly, color='black' )


        plt.title(filename.split('.')[0])
        plt.legend(['Curve Fit', 'Poly Fit ' +str(DEGREE) + " Degree", 'Documents' ,'Relavant Documents'])
        plt.xlabel('Document Collection. Size: ' + str(len(X_vals)))
        plt.ylabel('Rel Document Rate Scale: ' + str((1 / (WINDOW_SIZE * 2))) + " - " + "1.0")


        pdf.savefig(fig)

    exit()

pdf.close()
    

   



