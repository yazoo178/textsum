# Code from https://blog.dominodatalab.com/fitting-gaussian-process-models-python/

import numpy as np

def exponential_cov(x, y, params):
    return params[0] * np.exp( -0.5 * params[1] * np.subtract.outer(x, y)**2)

# Plot a band representing one standard deviation from the mean

θ = [1, 10]
σ_0 = exponential_cov(0, 0, θ)
xpts = np.arange(-3, 3, step=0.01)
plt.errorbar(xpts, np.zeros(len(xpts)), yerr=σ_0, capsize=0)
# plt.show()

# Sample point from unconditional Gaussian
x = [1.]
y = [np.random.normal(scale=σ_0)]

# Define confidence band and visualise
σ_1 = exponential_cov(x, x, θ)

def predict(x, data, kernel, params, sigma, t):
    k = [kernel(x, y, params) for y in data]
    Sinv = np.linalg.inv(sigma)
    y_pred = np.dot(k, Sinv).dot(t)
    sigma_new = kernel(x, x, params) - np.dot(k, Sinv).dot(k)
    return y_pred, sigma_new

# Make predictions based on single point

x_pred = np.linspace(-3, 3, 1000)
predictions = [predict(i, x, exponential_cov, θ, σ_1, y) for i in x_pred]
y_pred, sigmas = np.transpose(predictions)

# Visualise single point predictions
# plt.errorbar(x_pred, y_pred, yerr=sigmas, capsize=0)
# plt.plot(x, y, "ro")

# Function to define conditional on multi-variate Gaussian distribution
def conditional(x_new, x, y, params):

    B = exponential_cov(x_new, x, params)
    C = exponential_cov(x, x, params)
    A = exponential_cov(x_new, x_new, params)

    mu = np.linalg.inv(C).dot(B.T).T.dot(y)
    sigma = A - B.dot(np.linalg.inv(C).dot(B.T))

    return(mu.squeeze(), sigma.squeeze())

# Sample another point (constrained on the first point)
m, s = conditional([-0.7], x, y, θ)
y2 = np.random.normal(m, s)

x.append(-0.7)
y.append(y2)

# Make predicitons based on two points and visualise
# σ_2 = exponential_cov(x, x, θ)
# predictions = [predict(i, x, exponential_cov, θ, σ_2, y) for i in x_pred]

# y_pred, sigmas = np.transpose(predictions)
# plt.errorbar(x_pred, y_pred, yerr=sigmas, capsize=0)
# plt.plot(x, y, "ro")

# Sample several points
x_more = [-2.1, -1.5, 0.3, 1.8, 2.5]
mu, s = conditional(x_more, x, y, θ)
y_more = np.random.multivariate_normal(mu, s)

x += x_more
y += y_more.tolist()

σ_new = exponential_cov(x, x, θ)
predictions = [predict(i, x, exponential_cov, θ, σ_new, y) for i in x_pred]

y_pred, sigmas = np.transpose(predictions)
plt.errorbar(x_pred, y_pred, yerr=sigmas, capsize=0)
plt.plot(x, y, "ro")


plt.show()
