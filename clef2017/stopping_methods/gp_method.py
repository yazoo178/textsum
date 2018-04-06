﻿import numpy as np
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

class GP:
    def create(self, x, y):
        dy = 0.5 + 1.0 * np.random.random(np.array(y).shape)
        kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))


        #gp_kernel = ExpSineSquared(1.0, 5.0, periodicity_bounds=(1e-2, 1e1)) \
        #+ C(1.0, (1e-3, 1e3))

        ##C(1.0, (1e-3, 1e3)) 
        self.gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9)
        self.gp.fit(x, y.ravel())
        

    def predict(self, x):
        y_pred, sigma = self.gp.predict(x, return_std=True)
        return y_pred, sigma




def model_func(x, a, k, c):
    return a * np.exp(-k*x) + c

def func(x, a, b):
    'nonlinear function in a and b to fit to data'
    return a * x / (b + x)

def other_func(x, a, k, n):
    'nonlinear function in a and b to fit to data'
    return n - a * np.exp(-k*x)

    
def findIn(score, x):
    for ind, x1 in enumerate(x):
        if score == x1:
            return ind

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx




def process(file, name, outputPath):

    scores = []
    
    #trueScores = []
    c = 0
    X_samps = []

   # scores_5 = []
   # X_samps_5 = []

    
    
    # Read through file containing cumulative totals for rel docs
    # and create x axis vales (3, 6, 9, ...) 
    for line in file:
        c = c + sampleRate
        tmp = []
        for val in re.split(r'\t+', line):
        
            if val == "\n":
                continue
        #if float(line) not in scores:
            tmp.append(float(val) * sampleRate)

        scores.append(np.array(tmp)) # y-axis
        X_samps.append(float(c))     # x-axis


    # Read in cumulative total for true scores
   # for line in trueFile:
        #trueScores.append(float(line))



    #recallFile.write(str(len(trueScores)) + ",")
    #recallFile.write(str(max(trueScores)) + ",")

    #x_val_true =findIn(int(round(max(trueScores) * (rate / 100))), trueScores)
    #recallFile.write(str(x_val_true) + ",")
    
    scores = np.array(scores)
    scores = np.rot90(scores)
    X_samps = np.array(X_samps)


   # x = np.atleast_2d([float(x) for x in range(0, len(trueScores))]).T
   # trueScores = np.array(trueScores)
   # x = np.array(x).ravel()
    
   # scores_5 = np.array(scores_5)
   # X_samps_5 = np.array(X_samps_5)
   # plt.plot(x, trueScores)
   # plt.scatter([x_val_true], [int(round(max(trueScores) * (rate / 100)))], s=60, c='r')
  #  plt.annotate(str(rate) + "%" + "recall", xy=(x_val_true, int(round(max(trueScores) * (rate / 100)))), xytext=(20,20), bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
   #     arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
            
      
    totalDocs = sum(([len(x) for x in scores]))

    for i, scoreSet in enumerate(scores):


        alpha = 0.05 # 95% confidence interval = 100*(1-alpha)

        #get a file name
        fileWithOutPath = os.path.basename(file.name).split('.')[0]

        #x axis array of points 0 to total number of documents for topic
        X_vals = np.array(range(0, totalDocs))


        if method == "gp":

            gp = GP()
            gp.create(np.array([X_samps]).reshape(len(X_samps), 1), np.array(scoreSet))
            y2, sigma = gp.predict(X_vals.reshape(len(X_vals), 1))
            #_X = np.atleast_2d([x for x in range(0, len(scores))]).T


            #create new gp file
            y2Scores = open(outputPath + fileWithOutPath + '.txt', 'w')

            #write gp to file
            for item in y2:
                y2Scores.write("%s\n" % item)

            y2Scores.close()

            if not show_curve:
                return 0



            plt.plot(X_vals, y2)
            # plt.fill(np.concatenate([x_pred, x_pred[::-1]]),
            #          np.concatenate([y_pred - 1.9600 * sigma,
            #                         (y_pred + 1.9600 * sigma)[::-1]]),
            #          alpha=.5, fc='b', ec='None', label='95% confidence interval')


            plt.show()

        else:

            # Fit curve using sampled data
            opt, pcov = curve_fit(other_func, X_samps, scoreSet, maxfev=1000)
            a, k, n = opt
            # Fit estimated curve onto compete range and save to file
            # y2 = other_func(X_samps, a, k, n)
            

            y2 = other_func(X_vals, a, k, n)
            n = len(y2)    # number of data points
            p = len(opt) # number of parameters
            dof = max(0, n - p) # number of degrees of freedom


            tval = t.ppf(1.0-alpha/2., dof) 
            c = 'g'

            #create curve file
            y2Scores = open(outputPath + fileWithOutPath + '.txt', 'w')

            #write curve to file
            for item in y2:
                y2Scores.write("%s\n" % item)

            y2Scores.close()

            if not show_curve:
                return 0
        
            lower = []
            upper = []
 
            for p,var in zip(opt, np.diag(pcov)):
                sigma = var**0.5
                lower.append(p - sigma*tval)
                upper.append(p + sigma*tval)

            yfit = other_func(X_vals, *lower)
            plt.plot(X_vals,yfit,'--', color=c)
            yfit = other_func(X_vals, *upper)
            plt.plot(X_vals,yfit,'--', label='CI 95%', color=c)

            plt.plot(X_vals, y2, label=u'Sample - ' + str(sampleRate))


            plt.fill(np.concatenate([X_vals, X_vals[::-1]]),
                 np.concatenate([y2 - 1.9500 * sigma,
                                (y2 + 1.9500 * sigma)[::-1]]),
                alpha=.1, fc='g', ec='None')

            plt.xlabel("Total number of documents for query", fontsize=16)
            plt.ylabel("Estimated number of releavent documents", fontsize=16)
            plt.legend(loc='lower right', fontsize=16)
            plt.title(fileWithOutPath, fontsize=16)
            plt.show()
        
            
            break

    return 0





opts, args = getopt.getopt(sys.argv[1:],"hc:i:m:s:q:c")
method = "lin"
sampleRate = 3
qrel = 'qrel/qrel_abs_test'
int_scores_folder = 'Test_Data_Sheffield-run-2_int_scores_5/'
#true_int_scores_folder = 'intergrates_bin/' 
rate = 70
show_curve = False


for opt, arg in opts:
    if opt == '-h':
        print ("-m mode gp/lin [DEFAULT lin] -s sample rate [DEFAULT 3] -i intergration scores folder -q qrel file -c show curves [DEFAULT N]")
    elif opt in ("-m"):
        method = arg
    elif opt in ("-s"):
        sampleRate = int(arg)
    elif opt in ("-i"):
        int_scores_folder = arg + "/"
    elif opt in ("-q"):
        qrel = arg
    elif opt in ("-c"):
        show_curve = True



print("Method :" + method)

if not os.path.exists(int_scores_folder + "curve_scores/"):
    os.makedirs(int_scores_folder + "curve_scores/")

queryIdToRelvDocs = {}
with open(qrel, encoding='utf-8') as content:
    for line in content:
        tabbed = re.split('\s+', line)

        if tabbed[0] not in queryIdToRelvDocs:
            queryIdToRelvDocs[tabbed[0]] = []

        if '1' in tabbed[3].rstrip().strip():
            queryIdToRelvDocs[tabbed[0]].append(1)

        else:
            queryIdToRelvDocs[tabbed[0]].append(0)


total = 0
sucess = 0
for filename in os.listdir(int_scores_folder):

    #its a folder skip over
    if os.path.isdir(int_scores_folder + filename):
        continue

    file = open(int_scores_folder + filename , "r+")
    
    try:
        total += process(file, filename, int_scores_folder + "curve_scores/")
        sucess += 1
    except RuntimeError:
        pass
   
print(total / sucess)

    





      #  fileWithOutPath = os.path.basename(file.name).split('.')[0]

      #  count = 0
       # for in_score in X_samps - 1:
            
       #     if in_score > x_val_true:
        #        break
#
        #    if queryIdToRelvDocs[fileWithOutPath][int(in_score)] == 1:
        #        count = count + 1

                ###
