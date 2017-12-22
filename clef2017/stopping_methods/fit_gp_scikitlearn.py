from sklearn import gaussian_process, datasets
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel
import numpy as np
import matplotlib.pylab as plt


kernel = ConstantKernel() + Matern(length_scale=2, nu=3/2) + WhiteKernel(noise_level=1)

# !! Need to provide some data here
x, y, coef = datasets.make_regression(n_samples=100, n_features=1,
                                      n_informative=1, noise=5,
                                      coef=True, random_state=0)

X = x.reshape(-1, 1)


gp = gaussian_process.GaussianProcessRegressor(kernel=kernel)
gp.fit(X, y)

# gaussian_process.GaussianProcessRegressor(alpha=1e-10, copy_X_train=True,
#                          kernel=1**2 + Matern(length_scale=2, nu=1.5) + WhiteKernel(noise_level=1),
#                          n_restarts_optimizer=0, normalize_y=False,
#                          optimizer='fmin_l_bfgs_b', random_state=None)


x_pred = np.linspace(-6, 6).reshape(-1,1)
y_pred, sigma = gp.predict(x_pred, return_std=True)

# Plot the output
plt.plot(x, y, "ro")
plt.plot(x_pred, y_pred, "bx")
plt.errorbar(x_pred, y_pred, yerr=sigma, capsize=0)
# plt.fill(np.concatenate([x_pred, x_pred[::-1]]),
#          np.concatenate([y_pred - 1.9600 * sigma,
#                         (y_pred + 1.9600 * sigma)[::-1]]),
#          alpha=.5, fc='b', ec='None', label='95% confidence interval')


plt.show()
