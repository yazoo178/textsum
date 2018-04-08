import numpy as np
import scipy as sp
import pylab as pb
import os
import sys
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings("ignore")


def multiquadratic_kernel(x, y, s, c):
    k = s**2*(np.subtract.outer(x,y)**2 + c**2)**0.5
    
    return k

T = np.linspace(0, 10, 400).reshape(400,)

#compute the covariance matrices
K = multiquadratic_kernel(T, T, 1, 0.5)


g = np.random.multivariate_normal(np.zeros(400), K)
for r in range(30):
    print(g)
    f = np.random.multivariate_normal(g, K)
    plt.plot(T, f, 'b', linewidth=1, label='$f(t)$' if r==0 else None, alpha=0.2)
plt.title('Draws from a Multiquadratic Kernel')
plt.xlabel('Input (x)')
plt.ylabel('Output (f(x))')
plt.show()