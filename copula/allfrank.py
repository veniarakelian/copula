from scipy.stats import norm, expon
from scipy.optimize import minimize
from scipy.linalg import det, inv
from math import pi
import numpy as np
import allnorm

def allfrank(x, y):

    sample = len(x)

    # Convert to normall #
    result = allnorm(x, y)

    # x - mean, y - mean #
    xbar = x - result["sigma"][2]
    ybar = y - result["sigma"][3]

    # Calculate theta #
    minimizeArgs = {"sample": sample, "sigma": sigma, "xbar": xbar, "ybar": ybar, "u": u, "v": v}
    theta = minimize(logLikelihood, args=minimizeArgs, method='Nelder-Mead')
    theta = theta.x[0]

    # Find logLikelihood of theta #
    cop1 = logLikelihood(sample, sigma, xbar, ybar, u, v, theta)

    # Calculate hessian of log-copula's density #
    hes_cop = (-sample / (theta ** 2)) - (sample * np.exp(-theta) / ((2 - np.exp(-theta)) ** 2)) + 2 * np.sum(np.div(((-np.exp(-theta)) - (np.dot((u + v) ** 2,   np.exp(-theta * (u+v)))) + (np.dot(u ** 2, np.exp(-theta * u))) + (np.dot(v ** 2, np.exp(-theta * v)))), np.exp(-theta) - 1 + np.dot(np.exp(-theta * u) - 1, np.exp(-theta*v) - 1))) + 2 * np.sum((np.div(((-np.exp(-theta)) + (np.dot(u + v,   np.exp(-theta * (u+v)))) - (np.dot(u, np.exp(-theta * u))) - (np.dot(v, np.exp(-theta * v)))), np.exp(-theta) - 1 + np.dot(np.exp(-theta * u) - 1, np.exp((-theta*v) - 1)))) ** 2)

    s = -sample / hes_cop
    hes_prior_cop = -1 / (s ** 2)

    if norm.pdf(theta, loc=0, scale=s) != 0:
        log_prior = np.log(norm.pdf(theta, loc=0, scale=s)) + np.log(expon.pdf(result["sigma"][0], loc=1)) + np.log(np.expon.pdf(result["sigma"][1], loc=1))
        BFu = cop1 + log_prior + 0.5 * np.log(-inv(det(hes_norm) * (hes_cop - hes_prior_cop)))
        hes = det(hes_norm) * (hes_cop - hes_prior_cop)
    else:
        theta = 0
        cop1 = 0
        log_prior = np.log(10 **(-300)) + np.log(expon.pdf(result["sigma"][0], loc=1)) + np.log(expon.pdf(result["sigma"][1], loc=1))
        BFu = cop1 = log_prior + 0.5 * np.log(inv(hes_norm))
        hes = det(hes_norm)

    BF = 1

    result = {"theta": theta, "cop1": cop1, "hes": hes, "hes_prior_cor": hes_prior_cop, "BF": BF, "BFu": BFu}

# Log-likelihood #
def logLikelihood(sample, sigma, xbar, ybar, u, v, theta):

    lLikelihood = (0.5 * sample * np.log(theta ** 2)) + (0.5 * sample * np.log((1 - np.exp(-theta)) ** 2)) - (theta * np.sum(u + v)) - (np.sum(np.log((np.exp(-theta) - 1 +  np.dot(np.exp(-theta*u) - 1, np.exp(-theta*v) - 1)) ** 2))) - (0.5 * sample * np.log(2 * pi * (sigma[0] ** 2))) - (0.5 * np.sum(xbar ** 2) / (sigma[0] ** 2)) - (0.5 * sample * np.log(2 * pi * (sigma[1] ** 2))) - (0.5 * np.sum(ybar ** 2) / (sigma[1] ** 2))

    return lLikelihood


