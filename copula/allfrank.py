from scipy.stats import norm, expon
from scipy.optimize import minimize
from scipy.linalg import det, inv
from math import pi
import numpy as np
from allnorm import allnorm

def allfrank(x, y):

    sample = len(x)

    # Convert to normall #
    result = allnorm(x, y)

    u = result["u"]
    v = result["v"]
    sigma = result["sigma"]

    # x - mean, y - mean #
    xbar = x - sigma[2]
    ybar = y - sigma[3]

    # Calculate theta #
    minimizeArgs = (sample, sigma, xbar, ybar, u, v)
    res = minimize(logLikelihood, x0 = 0, args=minimizeArgs, method='Nelder-Mead')
    theta = res.x[0]

    # Find logLikelihood of theta #
    cop1 = logLikelihood(theta, sample, sigma, xbar, ybar, u, v)

    # Calculate hessian of log-copula's density #
    hes_cop = (-sample / (theta ** 2)) - (sample * np.exp(-theta) / ((2 - np.exp(-theta)) ** 2)) + 2 * np.sum(np.div(((-np.exp(-theta)) - (np.dot((u + v) ** 2,   np.exp(-theta * (u+v)))) + (np.dot(u ** 2, np.exp(-theta * u))) + (np.dot(v ** 2, np.exp(-theta * v)))), np.exp(-theta) - 1 + np.dot(np.exp(-theta * u) - 1, np.exp(-theta*v) - 1))) + 2 * np.sum((np.div(((-np.exp(-theta)) + (np.dot(u + v,   np.exp(-theta * (u+v)))) - (np.dot(u, np.exp(-theta * u))) - (np.dot(v, np.exp(-theta * v)))), np.exp(-theta) - 1 + np.dot(np.exp(-theta * u) - 1, np.exp((-theta*v) - 1)))) ** 2)

    s = -sample / hes_cop
    hes_prior_cop = -1 / (s ** 2)

    if norm.pdf(theta, loc=0, scale=s) != 0:
        log_prior = np.log(norm.pdf(theta, loc=0, scale=s)) + np.log(expon.pdf(sigma[0], loc=1)) + np.log(np.expon.pdf(sigma[1], loc=1))
        BFu = cop1 + log_prior + 0.5 * np.log(-inv(det(hes_norm) * (hes_cop - hes_prior_cop)))
        hes = det(hes_norm) * (hes_cop - hes_prior_cop)
    else:
        theta = 0
        cop1 = 0
        log_prior = np.log(10 **(-300)) + np.log(expon.pdf(sigma[0], loc=1)) + np.log(expon.pdf(sigma[1], loc=1))
        BFu = cop1 = log_prior + 0.5 * np.log(inv(hes_norm))
        hes = det(hes_norm)

    BF = 1

    result = {"theta": theta, "cop1": cop1, "hes": hes, "hes_prior_cor": hes_prior_cop, "BF": BF, "BFu": BFu}

# Log-likelihood #
def logLikelihood(theta, sample, sigma, xbar, ybar, u, v):

    lLikelihood = (0.5 * sample * np.log(theta ** 2)) + (0.5 * sample * np.log((1 - np.exp(-theta)) ** 2)) - (theta * np.sum(u + v)) - (np.sum(np.log((np.exp(-theta) - 1 +  np.dot(np.exp(-theta*u) - 1, np.exp(-theta*v) - 1)) ** 2))) - (0.5 * sample * np.log(2 * pi * (sigma[0] ** 2))) - (0.5 * np.sum(xbar ** 2) / (sigma[0] ** 2)) - (0.5 * sample * np.log(2 * pi * (sigma[1] ** 2))) - (0.5 * np.sum(ybar ** 2) / (sigma[1] ** 2))

    return lLikelihood

# Test #
if __name__ == "__main__":

    # Mean of x: 0 + sigma: 0.1 #
    x = np.array([[0.02408731], [-0.01143883], [-0.05187822],  [0.02934885], [-0.01896763], [-0.1215414],
                  [0.1308636],  [-0.00410573], [-0.02659866], [-0.03115632],  [0.04915726],  [0.17748823],
                  [-0.17470189], [-0.03623728],  [0.20036427], [-0.04309518], [-0.12871291],  [0.11440636],
                  [-0.10981895], [-0.12949878],  [0.04235601], [-0.02640793],  [0.04188305], [-0.07620245],
                  [0.10796665], [-0.10832592], [-0.05327015], [-0.02708483],  [0.07881769],  [0.10335654]
                  ])

    y = np.array([[1], [1]])

    result = allfrank(x, y)

    print(result)
