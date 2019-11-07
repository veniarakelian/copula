from scipy.stats import norm
from math import pi
import numpy as np

def allfrank(x, y):

    sample = len(x)

    result = allnorm(x, y)

    xbar = x - result["sigma"][2]
    ybar = y - result["sigma"][3]

# Log-likelihood #
def logLikelihood(sample, sigma, xbar, ybar, u, v, theta):

    lLikelihood = 0.5 * sample * np.log(theta ** 2) +
                  0.5 * sample * np.log((1 - np.exp(-theta)) ** 2) -
                  theta * np.sum(u + v) -
                  np.sum(np.log((np.exp(-theta) - 1 +  np.dot(((np.exp(-theta*u) - 1)), np.exp(-theta*v) - 1)) ** 2)) +
                  0.5 * sample * np.log(2 * pi * (sigma[0] ** 2)) - 
                  0.5 * np.sum(xbar ** 2) / (sigma[0] ** 2) -
                  0.5 * sample * np.log(2 * pi * (sigma[1] ** 2)) - 
                  0.5 * np.sum(ybar ** 2) / (sigma[1] ** 2)

    return lLikelihood


