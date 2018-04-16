import numpy as np
import matplotlib
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

def findIn(score, x):
	for ind, x1 in enumerate(x):
		if score == x1:
			return ind

def find_nearest(array,value):
	idx = (np.abs(array-value)).argmin()
	return idx


y_p = []
y_lower = []
y_upper = []

for curveScore in open("curve_scores/CD010023.txt", 'r+'):
	vals = curveScore.split('\t')
	y_p.append(float(vals[0]))
	y_lower.append(float(vals[1]))
	y_upper.append(float(vals[2]))	
	
print(y_p)

y_p = np.array(y_p)

plt.xlabel("Total number of documents for query", fontsize=16)
plt.ylabel("Estimated number of releavent documents", fontsize=16)

x_sam_val = find_nearest(y_p, max(y_p) * (70 / 100))
index = findIn(x_sam_val, range(0, len(y_p)))


plt.title('CD010023')
plt.scatter(np.array([int(x_sam_val)]), np.array([y_p[x_sam_val]]), c='black', label='Estimated 70% recall point', s = 40)
plt.plot(range(0, len(y_p)), y_p, label="Sample 3")
plt.plot(range(0, len(y_p)), y_lower, '--', c='g', label='Lower CI 95%')
plt.plot(range(0, len(y_p)), y_upper, '--', c='g', label='Upper CI 95%')
plt.legend(loc='lower right', fontsize=14)
plt.show()