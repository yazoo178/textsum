import numpy as np
from matplotlib import pyplot as plt
import re
import os
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from sklearn.utils.extmath import softmax
import itertools




class GP:


    def create(self, x, y):
        dy = 0.5 + 1.0 * np.random.random(np.array(y).shape)
        kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))
        self.gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9)
        self.gp.fit(x, y.ravel())
        

    def predict(self, x):
        y_pred, sigma = self.gp.predict(x, return_std=True)
        return y_pred, sigma

    
def process(file, name):
    scores = []

    for line in file:
        scores.append(float(line))

    fig = plt.figure()
    #plt.plot(scores, markersize=10)

    #X = np.atleast_2d([x for x in range(0, len(scores))]).T
    sampleRate = 10


    scores2 = scores[::sampleRate]
    scores2 = np.array(scores2).reshape(len(scores2), 1)
        #scores2 = list(itertools.chain.from_iterable(itertools.repeat(q, x) for q in scores2))
    

       # for i in range(len(scores2), len(scores)):
           # scores2.append(scores2[len(scores2) - 1])

        #plt.plot(scores2, '--')
    x = np.atleast_2d([x for x in range(0, len(scores2))]).T
    X = np.atleast_2d(np.linspace(0, len(scores2), len(scores))).T
    
    
    #X = np.atleast_2d([x for x in range(0, len(scores2))]).T
    #X = np.atleast_2d(X).T


    dy = 0.5 + 1.0 * np.random.random(np.array(scores2).shape)

    gp = GP()
    gp.create(x, scores2)
    y_pred, sigma = gp.predict(X)
    _X = np.atleast_2d([x for x in range(0, len(scores))]).T


    #plt.plot(scores, markersize=10)

    #plt.errorbar(X.ravel(), scores2, dy, fmt='r.', label=u'Observations')

    
    resultScoreFile = open('true_document_rates/' + name + ".csv", "w")
    resultScoreFile.write("% of Docs Looked at" + "," + "% of Docs Returned" + "," + "Number of Documents" + "," + "Total Number of Documents" + "\t" + "Sample Rate:" + str(sampleRate) + "\n")
    percentages = [x for x in range(1, 100)]


    for per in percentages:
        ind = (len(X) / 100) * per
        score = ((scores[int(ind)] / scores[-1]) * 100)
        resultScoreFile.write(str(per) + "," + str(score) + "," + str(int(ind)) + "," + str(len(scores)) + "\n")


    resultScoreFile.close()
    
    """
    plt.plot(_X, scores, 'C1', label=u'True')
    
    plt.plot(_X, y_pred, 'b-', label=u'Prediction GP')

    plt.fill(np.concatenate([_X, _X[::-1]]),
             np.concatenate([y_pred - 1.9600 * sigma,
                            (y_pred + 1.9600 * sigma)[::-1]]),
             alpha=.1, fc='g', ec='None', label='95% confidence interval')

    

    

    plt.xlabel('Number of Documents')
    plt.ylabel('Return Rate')
    plt.xlim(0, len(scores))
      #  plt.title(str())
    plt.title(scores)

    plt.legend(loc='upper right')
    plt.show()
    """


for filename in os.listdir('intergrates_bin'):
    file = open('intergrates_bin/' + filename , "r+")
    process(file, filename)
