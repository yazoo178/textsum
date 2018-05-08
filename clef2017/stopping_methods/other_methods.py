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
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVR





class Method:
    def create(self, x, y):
        self.method = SVR(kernel='rbf', C=1e3, gamma=0.1)
        self.method.fit(x, y.ravel())
        

    def predict(self, x):
        y_pred =  self.method.predict(x)
        return y_pred
    
def findIn(score, x):
    for ind, x1 in enumerate(x):
        if score == x1:
            return ind

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx



#a topic failed to run
def onfail(file, name, outputPath):

    file.seek(0)
    c = 0
    scores = []
    X_samps = []

    #get a file name
    fileWithOutPath = os.path.basename(file.name).split('.')[0]

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

    last = scores[-1]
    maxVal = sum(last)


    #create curve file
    y2Scores = open(outputPath + fileWithOutPath + '.txt', 'w')

    for x in range(0, len(scores)):
        y2Scores.write(str(maxVal) + "\t" + str(maxVal) + "\t" + str(maxVal) + "\n")

    y2Scores.close()
    return 1


def process(file, name, outputPath):

    scores = []
    c = 0
    X_samps = []

    
    # Read through file containing cumulative totals for rel docs
    # and create x axis vales (3, 6, 9, ...) 
    for line in file:
        c = c + sampleRate
        tmp = []
        for val in re.split(r'\t+', line):
        
            if val == "\n":
                continue
        #if float(line) not in scores:
            tmp.append(float(val) * 3)

        scores.append(np.array(tmp)) # y-axis
        X_samps.append(float(c))     # x-axis

    
    scores = np.array(scores)
    scores = np.rot90(scores)
    X_samps = np.array(X_samps)

    totalDocs = sum(([len(x) for x in scores]))
    X_vals = np.array(range(0, totalDocs))


    m = Method()

    m.create(np.array([X_samps]).reshape(len(X_samps), 1), np.array(scores[0]))

    y_1 = m.predict(X_vals.reshape(len(X_vals), 1))


    plt.plot(X_vals, y_1, c="r", label="n_estimators=300", linewidth=2)
    plt.plot(X_samps, scores[0], linewidth=2)
    plt.show()

    exit()
    return 1


        
        





opts, args = getopt.getopt(sys.argv[1:],"hc:i:m:s:q:c:j:")
method = "lin"
sampleRate = 2
qrel = 'qrel/qrel_abs_test'
int_scores_folder = 'Test_Data_Sheffield-run-2_int_scores_5/'
#true_int_scores_folder = 'intergrates_bin/' 
rate = 70
show_curve = False

for opt, arg in opts:
    if opt == '-h':
        print ("-m mode gp/lin [DEFAULT lin] -s sample rate [DEFAULT 3] -i intergration scores folder -q qrel file -c show curves [DEFAULT N] -j determines if we should skip a topic if the number of realvent documents falls below a certain percentage")
    elif opt in ("-m"):
        method = arg
    elif opt in ("-s"):
        sampleRate = int(arg)
    elif opt in ("-i"):
        int_scores_folder = arg + "/"
    elif opt in ("-q"):
        qrel = arg
    elif opt in ("-c"):
        print("Showing curve")
        show_curve = True
    elif opt in ("-j"):
        print(arg)
        jump_skip = float(arg)
      


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
fail = 0
for filename in os.listdir(int_scores_folder):

    #its a folder skip over
    if os.path.isdir(int_scores_folder + filename):
        continue

    file = open(int_scores_folder + filename , "r+")
    
    try:
        total += process(file, filename, int_scores_folder + "curve_scores/")
    except RuntimeError:
        print("Failed to generate for: "+ filename)
        fail += onfail(file, filename, int_scores_folder + "curve_scores/")
        pass
   
print("Topics created: " + str(total))
print("Topics failed: " + str(fail))
    





