from numpy.ma.extras import polyfit
print(__doc__)

# Author: Vincent Dubourg <vincent.dubourg@gmail.com>
#         Jake Vanderplas <vanderplas@astro.washington.edu>
#         Jan Hendrik Metzen <jhm@informatik.uni-bremen.de>s
# License: BSD 3 clause

import numpy as np
from matplotlib import pyplot as plt
import re
import os
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from sklearn.utils.extmath import softmax
import sys, getopt

np.random.seed(1)


class record:
    def __init__(self, qId):
        self.queryId = qId
        self.docsReturned = []

    def addDoc(self, doc):
        self.docsReturned.append(doc)

def f(x):
    """The function to predict."""
    return x * np.sin(x)





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


def calcDistirubtionTop1(testFiles, records, sample = 1):
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
            QueiresToDist[record] = []
            for z in range(0, sample):
                QueiresToDist[record].append([0] * int((len(records[record].docsReturned) / sample) + 1))
                for i, x in enumerate(records[record].docsReturned[z::sample]):
                    if x in queryIdToRelvDocs[record]:

                        QueiresToDist[record][z][i] = 1
            

            #QueiresToDist[record] =[float(x) / len(records[record].docsReturned) for x in QueiresToDist[record]]


        return QueiresToDist
                    


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

def calcRecallForTopN(N, testFiles, records):

    queryIdToRelvDocs = {}
    recallScores = {}
    with open(testFiles, encoding='utf-8') as content:
        found = False
        header = True
        qId = ""
        lastId = "Start"

        for line in content:

            tabbed = re.split('\s+', line)

            if tabbed[0] not in queryIdToRelvDocs:
                queryIdToRelvDocs[tabbed[0]] = []

            if '1' in tabbed[3].rstrip().strip():
                queryIdToRelvDocs[tabbed[0]].append(tabbed[2].rstrip().strip())
              

    for topic in records:
        i = 0
        recallScores[topic] = 0
        for returnedDoc in records[topic].docsReturned:

            if returnedDoc in queryIdToRelvDocs[topic]:
                recallScores[topic] += 1

            if i == N - 1:
                break

            i += 1

    #recallScores =  [recallScores[x] / N for x in recallScores]
    return recallScores

opts, args = getopt.getopt(sys.argv[1:],"hk:t:o:q:s:j:")
fileName = "Output/" + "Test_Data_Sheffield-run-2"
output = ""
qrel = "qrel/qrel_abs_test"
sample = 3
jump_skip = 1.0


for opt, arg in opts:
    if opt == '-h':
        print("-t the run file path -s sample size [DEFAULT 3] -q qrel file path -o output location [DEFAULT current dir]")
    elif opt in ("-t"):
        fileName = arg
    elif opt in ('-o'):
        output = arg + "/"
    elif opt in ('-q'):
        qrel = arg
    elif opt in ('-s'):
        sample = int(arg)
    elif opt in ("-j"):
        print(arg)
        jump_skip = float(arg)


#generate an output folder name from the file supplied
fullOutputPath  = output  + os.path.basename(fileName).split(".")[0]

#load the data from the results file
records = loadTestResults(fileName)

#calculate a distribution of releavent document occurences
scores = calcDistirubtionTop1(qrel, records, sample=sample)

#create a folder for the outputing the intergrated scroes
dir = fullOutputPath + "_int_scores_" + str(sample)

if not os.path.exists(dir):
    os.makedirs(dir)

for score in scores:

    if len([x for x in np.array(scores[score]).flatten() if x == 1]) / len(records[score].docsReturned) < jump_skip:
        print("skipped:" + score)
        continue
        


    f= open(dir + "/" + score + ".txt","w")
    vals = list(scores[score])
    
    # ----------------------------------------------------------------------
    #  First the noiseless case
    X = np.atleast_2d([x for x in range(0, len(vals))]).T

    intrgrated = []

    #Adjust the results to correct format
    vals = np.array(vals)
    vals = np.rot90(vals, 3)

    sums = [0] * sample

    #write data to file
    for row in vals:
        for x, val in enumerate(row):
            sums[x]+=val

        for sum in sums:
           # intrgrated.append(sum)
            f.write(str(sum) + "\t")

        f.write("\n")

    continue
    

        
    #intrgrated = softmax(np.array([intrgrated]))[0]

    #y = np.array([x / 2 for x in range(0, 10)])
    print(y)

    # Mesh the input space for evaluations of the real function, the prediction and
    # its MSE
    x = np.atleast_2d(np.linspace(0, len(vals), 1000)).T

    # Instanciate a Gaussian Process model
    kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))
    gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9)

    # Fit to data using Maximum Likelihood Estimation of the parameters
    gp.fit(X, intrgrated)


    # Make the prediction on the meshed x-axis (ask for MSE as well)
    y_pred, sigma = gp.predict(x, return_std=True)

    # Plot the function, the prediction and the 95% confidence interval based on
    # the MSE
    fig = plt.figure()
    # plt.plot(x, f(x), 'r:', label=u'$f(x) = x\,\sin(x)$')
    plt.plot(X, y, 'r.', markersize=10, label=u'Observations')
    plt.plot(x, y_pred, 'b-', label=u'Prediction')
    plt.plot(X, intrgrated, label="intergrated values")
    plt.fill(np.concatenate([x, x[::-1]]),
             np.concatenate([y_pred - 1.9600 * sigma,
                           (y_pred + 1.9600 * sigma)[::-1]]),
             alpha=.5, fc='b', ec='None', label='95% confidence interval')
  #  plt.title(str())
    plt.xlabel('$x$')
    plt.ylabel('$f(x)$')
    plt.title(score)
   # plt.ylim(0, 0.1)
    plt.legend(loc='upper right')
    plt.show()
    break

