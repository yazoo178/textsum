import numpy as np
from matplotlib import pyplot as plt
import re
import os
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF,DotProduct,Matern, RationalQuadratic, ConstantKernel as C
from sklearn.utils.extmath import softmax
from sklearn.linear_model import LinearRegression
import itertools
from scipy.optimize import curve_fit


# Define form of function going to try to fit to curve
def model_func(x, a, k):
    return a * np.exp(-k*x)


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


def findIn(score, x):
    for ind, x1 in enumerate(x):
        if score == x1:
            return ind
        
    
def process(file, name, trueFile):
    scores = []
    trueScores = []
    sampleRate = 3
    c = 0
    X_samps = []

    for line in file:
        c = c + sampleRate
        if float(line) not in scores:
            scores.append(float(line))
            X_samps.append(c)


    scores = (np.array(scores) * sampleRate).T

    for line in trueFile:
        trueScores.append(float(line))

    fig = plt.figure()
    #plt.plot(scores, markersize=10)

    #X = np.atleast_2d([x for x in range(0, len(scores))]).T
    

    scores2 = scores
    #scores2 = scores[::sampleRate]
    scores2 = np.array(scores2).reshape(len(scores2), 1)
        #scores2 = list(itertools.chain.from_iterable(itertools.repeat(q, x) for q in scores2))
    
    
    trueScores =  np.array(trueScores).reshape(len(trueScores), 1)
    X = np.atleast_2d(np.linspace(0, len(scores2), len(scores))).T

       # for i in range(len(scores2), len(scores)):
           # scores2.append(scores2[len(scores2) - 1])

        #plt.plot(scores2, '--')
    x = np.atleast_2d([x for x in range(0, len(scores2))]).T
    X = np.atleast_2d(np.linspace(0, len(scores2), len(scores))).T
    
    
    #X = np.atleast_2d([x for x in range(0, len(scores2))]).T
    #X = np.atleast_2d(X).T


    x_val_true =findIn(int(round(max(trueScores)[0] * 0.7)), trueScores) / sampleRate

    dy = 0.5 + 1.0 * np.random.random(np.array(scores2).shape)

    gp = GP()
    gp.create(x, scores2)
    y_pred, sigma = gp.predict(X)
    _X = np.atleast_2d([x for x in range(0, len(scores))]).T


    #x_val_gp = findIn(int(round(max(scores) * 0.7)), scores2) 

    #plt.plot(scores, markersize=10)

    #plt.errorbar(X.ravel(), scores2, dy, fmt='r.', label=u'Observations')

    """
    resultScoreFile = open('true_document_rates/' + name + ".csv", "w")
    resultScoreFile.write("% of Docs Looked at" + "," + "% of Docs Returned" + "," + "Number of Documents" + "," + "Total Number of Documents" + "\t" + "Sample Rate:" + str(sampleRate) + "\n")
    percentages = [x for x in range(1, 100)]


    for per in percentages:
        ind = (len(X) / 100) * per
        score = ((scores[int(ind)] / scores[-1]) * 100)
        resultScoreFile.write(str(per) + "," + str(score) + "," + str(int(ind)) + "," + str(len(scores)) + "\n")


    resultScoreFile.close()
    
    """

    p0 = (0.3,5) # starting search coefs 
    opt, pcov = curve_fit(model_func, X_samps, scores2, p0)
    #a, k = opt
    #y2 = model_func(x, a, k)

   # plt.plot(X_samps, y2, label='Fit. func: f(x) = %.3f e^{-%.3f x}' % (a,k))


    p1 = plt.plot(X_samps, scores2, c='C1', label=u'True')
    
   # y_pred = np.array([ '%.2f' % elem for elem in y_pred ])
   # y_pred_u = {}

   # for i, item in enumerate(y_pred):
      #  if item not in y_pred_u:
         #   y_pred_u[item] = i

   # _X = np.array(list(y_pred_u.values()))
   # y_pred = np.array(list(y_pred_u.keys()))

    p2 =plt.plot(X_samps, y_pred, c='b', label='Prediction GP')

    #p3 =plt.plot([x for x in range(0, len(trueScores[::sampleRate]))], trueScores[::sampleRate], c='C2', label=u'All Values')
    p3 =plt.plot([x for x in range(0, len(trueScores))], trueScores, c='C2', label=u'All Values')
    
    plt.fill(np.concatenate([X_samps, X_samps[::-1]]),
             np.concatenate([y_pred - 1.9600 * sigma,
                            (y_pred + 1.9600 * sigma)[::-1]]),
            alpha=.1, fc='g', ec='None', label='95% confidence interval')

    

    plt.xlabel('Number of Documents')
    plt.ylabel('Return Rate')
    #plt.xlim(0, len(scores))
      #  plt.title(str())
    plt.title("Sample Rate: " + str(sampleRate) + " 70% Recall: " + str(x_val_true))

    plt.legend(loc='upper right')
    plt.show()
    

for filename in os.listdir('intgrates_s_10'):
    file = open('intgrates_s_10/' + "CD008803.txt" , "r+")
    fileTrue = open('intergrates_bin/' + "CD008803.txt" , "r+")
    process(file, filename, fileTrue)
    break

#for filename in os.listdir('intergrates_bin'):
    #file = open('intergrates_bin/' + filename , "r+")
    #process(file, filename)
