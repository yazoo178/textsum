import numpy as np
from matplotlib import pyplot as plt
import re
import os
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from sklearn.utils.extmath import softmax


file = open('intgrates/' + "CD009925.txt" , "r+")
scores = []


for line in file:
    scores.append(float(line))

fig = plt.figure()
plt.plot(scores, markersize=10)

p = np.atleast_2d(np.linspace(0, len(scores), 1000)).T
X = np.atleast_2d([x for x in range(0, len(scores))]).T

for x in range(2, 10):

    scores2 = scores[::x] 

    for i in range(len(scores2), len(scores)):
        scores2.append(scores2[len(scores2) - 1])

    plt.plot(scores2, markersize=10)

X = np.atleast_2d([x for x in range(0, len(scores))]).T

    # plt.plot(x, f(x), 'r:', label=u'$f(x) = x\,\sin(x)$')
kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))
gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9)
gp.fit(X, scores)

y_pred, sigma = gp.predict(p, return_std=True)


plt.plot(scores2, markersize=10)

plt.xlabel('Number of Documents')
plt.ylabel('Return Rate')

  #  plt.title(str())
plt.title(scores)

plt.legend(loc='upper right')
plt.show()