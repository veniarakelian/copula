from scipy.stats import norm, expon
from scipy.optimize import minimize
from scipy.linalg import det, inv
from math import pi
import numpy as np
from allnorm import allnorm

def allclayton(x, y):

    sample = len(x)

    # Convert to normall #
    result = allnorm(x, y)

    u = result["u"]
    v = result["v"]
    sigma = result["sigma"]
    hes_norm = result["hes_norm"]

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
    hes_cop = (-sample / ((theta + 1)**2)) - (-2 * (theta ** (-3) * np.sum(np.log((u **(-theta)) + (v ** (-theta)) - 1))) - 2*(theta ** (-2)) * np.sum(np.divide(np.multiply(np.log(u), u **(-theta)) +  np.multiply(np.log(v), v **(-theta)), (u **(-theta)) + (v ** (-theta))  - 1))

    s = -sample / hes_cop
    hes_prior_cop = -1 / (s ** 2)

    if norm.pdf(theta, loc=0, scale=s) != 0:
        log_prior = np.log(norm.pdf(theta, loc=0, scale=s)) + np.log(expon.pdf(sigma[0], loc=1)) + np.log(expon.pdf(sigma[1], loc=1))
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

    return result

# Log-likelihood #
def logLikelihood(theta, sample, sigma, xbar, ybar, u, v):

    lLikelihood =  (sample * np.log(1 + theta)) - ((theta + 1) * np.sum(np.log(u ** v)))  - ((np.sum(np.log((u ** (-theta)) +  (v ** (-theta)) -1))) * (2 + (1/theta))) - (0.5 * sample * np.log(2 * pi * (sigma[0] ** 2))) - (0.5 * np.sum(xbar ** 2) / (sigma[0] ** 2)) - (0.5 * sample * np.log(2 * pi * (sigma[1] ** 2))) - (0.5 * np.sum(ybar ** 2) / (sigma[1] ** 2))

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

    y = np.array([[0.02408731], [-0.01143883], [-0.05187822],  [0.02934885], [-0.01896763], [-0.1215414],
                  [0.1308636],  [-0.00410573], [-0.02659866], [-0.03115632],  [0.04915726],  [0.17748823],
                  [-0.17470189], [-0.03623728],  [0.20036427], [-0.04309518], [-0.12871291],  [0.11440636],
                  [-0.10981895], [-0.12949878],  [0.04235601], [-0.02640793],  [0.04188305], [-0.07620245],
                  [0.10796665], [-0.10832592], [-0.05327015], [-0.02708483],  [0.07881769],  [0.10335654]
                  ])

    result = allfrank(x, y)

    print(result)
