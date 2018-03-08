import numpy as np
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

class GP:
    def create(self, x, y):
        dy = 0.5 + 1.0 * np.random.random(np.array(y).shape)
        kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))

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




def process(file, name, trueFile, file5, recallFile):

    scores = []
    trueScores = []
    sampleRate = 3
    c = 0
    X_samps = []

    scores_5 = []
    X_samps_5 = []

    
    

    for line in file:
        c = c + sampleRate
        tmp = []
        for val in re.split(r'\t+', line):
        
            if val == "\n":
                continue
        #if float(line) not in scores:
            tmp.append(float(val) * sampleRate)

        scores.append(np.array(tmp))
        X_samps.append(float(c))


    c = 0
    for line in file5:
        c = c + 5

        #if float(line) not in scores:
        scores_5.append(float(line))
        X_samps_5.append(float(c))


    for line in trueFile:
        trueScores.append(float(line))



    #recallFile.write(str(len(trueScores)) + ",")
    #recallFile.write(str(max(trueScores)) + ",")

    x_val_true =findIn(int(round(max(trueScores) * (rate / 100))), trueScores)
    #recallFile.write(str(x_val_true) + ",")
    
    scores = np.array(scores)
    scores = np.rot90(scores)
    X_samps = np.array(X_samps)


    x = np.atleast_2d([float(x) for x in range(0, len(trueScores))]).T
    trueScores = np.array(trueScores)
    x = np.array(x).ravel()
    
    scores_5 = np.array(scores_5)
    X_samps_5 = np.array(X_samps_5)
    plt.plot(x, trueScores)

    


    for i, scoreSet in enumerate(scores):


        opt, pcov = curve_fit(other_func, X_samps, scoreSet, maxfev=1000)
        a, k, n = opt
        y2 = other_func(X_samps, a, k, n)
        
        x_sam_val = find_nearest(y2, max(y2) * (rate / 100))
        #recallFile.write(str(x_sam_val) + ",")
        score = ((len(trueScores) - x_sam_val) / sampleRate) / x_val_true


        recallFile.write(str(x_sam_val >= x_val_true) + ",")
        recallFile.write(str(1 - (x_sam_val / len(y2))) + ",")
        recallFile.write(str(score))


        alpha = 0.05 # 95% confidence interval = 100*(1-alpha)

        n = len(y2)    # number of data points
        p = len(opt) # number of parameters

        dof = max(0, n - p) # number of degrees of freedom

        # student-t value for the dof and confidence level

        tval = t.ppf(1.0-alpha/2., dof) 
        c = 'g'

        lower = []
        upper = []
        for p,var in zip(opt, np.diag(pcov)):
            sigma = var**0.5
            lower.append(p - sigma*tval)
            upper.append(p + sigma*tval)

        yfit = other_func(X_samps, *lower)
        plt.plot(X_samps,yfit,'--', color=c)
        yfit = other_func(X_samps, *upper)
        plt.plot(X_samps,yfit,'--', label='CI 95%', color=c)

        plt.plot(X_samps, y2, label=u'Sample 3 - ' + str(i))


        plt.fill(np.concatenate([X_samps, X_samps[::-1]]),
             np.concatenate([y2 - 1.9500 * sigma,
                            (y2 + 1.9500 * sigma)[::-1]]),
            alpha=.1, fc='g', ec='None', label='95% confidence interval')

        break

    


  #  gp = GP()
    #gp.create(x, scores)
   # y_pred, sigma = gp.predict(X)
   # _X = np.atleast_2d([x for x in range(0, len(scores))]).T

    opt, pcov = curve_fit(other_func, x, trueScores)
    a, k, n = opt
    y1 = other_func(x, a, k, n)

    plt.plot(x, y1, label=u'True')
    

    #p1 = plt.plot(X_samps, scores, c='C1', label=u'True')


 



    opt, pcov = curve_fit(other_func, X_samps_5, scores_5)
    a, k, n = opt
    y3 = other_func(X_samps_5, a, k, n)
    

    #p1 = plt.plot(X_samps_5, y3, c='b', label=u'Sample 5')




    plt.legend(loc='lower right')
    plt.show()
    return score

rate = 70

recallFile = open("recall_file_" + str(rate) + ".csv" , "w")
#recallFile.write("Topic Name,Total Number of Documents, Number of Releavent Documents, Observations for " + str(rate) + "% Recall, Observations for " + str(rate) + "% Recall Sample_1 1/3, Observations for " + str(rate) + " Recall Sample_2 2/3, Observations for " + str(rate) + "% Recall Sample_3 3/3 \n")
recallFile.write("Topic Name, 70% Recall, Recall, Effort \n")

sum = 0
sucess = 0
for filename in os.listdir('intgrates_s_10'):
    #filename = 'CD008803.txt'
    recallFile.write(filename + ",")

    file = open('intgrates_s_3/' + filename , "r+")
    file5 = open('intgrates_s_5/' + filename , "r+")
    fileTrue = open('intergrates_bin/' + filename , "r+")
    
    
    
    try:
        sum += process(file, filename, fileTrue, file5, recallFile)
        sucess += 1
    except RuntimeError:
        pass

    recallFile.write("\n")
   
  
recallFile.close()
print(sum / sucess)

    