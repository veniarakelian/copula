from __future__ import division 
from scipy.stats import norm, expon
from scipy.linalg import det, inv
from allnorm import allnorm
from pandas import read_excel
from copulae import FrankCopula
import numpy as np
from math import pi

def allfrank(x, y, thetaInit=1.4):

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


    data = []
    for i in range(len(u)):
        data.append([u[i][0], v[i][0]])
   
    data = np.array(data)
    cop = FrankCopula(theta=thetaInit)
    cop.fit(data)
    theta = cop.params
    
    # Save frequent calculations #
    minus_sample = -sample
    u_plus_v = u + v
    exp_of_minus_theta = np.exp(-theta)
    exp_of_minus_theta_mult_v = np.exp(-theta * v)
    exp_of_minus_theta_mult_u = np.exp(-theta * u)

    # Find logLikelihood of theta #
    cop1 = (0.5 * sample * np.log(theta ** 2)) + (0.5 * sample * np.log((1 - exp_of_minus_theta) ** 2)) - (theta * np.sum(u + v)) - (np.sum(np.log((exp_of_minus_theta - 1 +  np.multiply(np.exp(-theta*u) - 1, np.exp(-theta*v) - 1)) ** 2))) - (0.5 * sample * np.log(2 * pi * (sigma[0] ** 2))) - (0.5 * np.sum(xbar ** 2) / (sigma[0] ** 2)) - (0.5 * sample * np.log(2 * pi * (sigma[1] ** 2))) - (0.5 * np.sum(ybar ** 2) / (sigma[1] ** 2))

    # Calculate hessian of log-copula's density #
    hes_cop = (minus_sample / (theta ** 2)) - (sample * exp_of_minus_theta / ((2 - exp_of_minus_theta) ** 2)) + 2 * np.sum(np.divide(((-exp_of_minus_theta) - (np.multiply((u_plus_v) ** 2, np.exp(-theta * (u_plus_v)))) + (np.multiply(u ** 2, exp_of_minus_theta_mult_u)) + (np.multiply(v ** 2, exp_of_minus_theta_mult_v))), exp_of_minus_theta - 1 + np.multiply(exp_of_minus_theta_mult_u - 1, exp_of_minus_theta_mult_v - 1))) + 2 * np.sum((np.divide(((-exp_of_minus_theta) + (np.multiply(u_plus_v, np.exp(-theta * (u_plus_v)))) - (np.multiply(u, exp_of_minus_theta_mult_u)) - (np.multiply(v, exp_of_minus_theta_mult_v))), exp_of_minus_theta - 1 + np.multiply(exp_of_minus_theta_mult_u - 1, np.exp((-theta*v) - 1)))) ** 2)

    s = minus_sample / hes_cop
    hes_prior_cop = -1 / (s ** 2)

    if norm.pdf(theta, loc=0, scale=s) != 0:
        log_prior = np.log(norm.pdf(theta, loc=0, scale=s)) + np.log(expon.pdf(sigma[0], scale=1)) + np.log(expon.pdf(sigma[1], scale=1))
        BFu = cop1 + log_prior + 0.5 * np.log(-1/(det(hes_norm) * (hes_cop - hes_prior_cop)))
        hes = det(hes_norm) * (hes_cop - hes_prior_cop)
    else:
        theta = 0
        cop1 = 0
        log_prior = np.log(10 **(-300)) + np.log(expon.pdf(sigma[0], scale=1)) + np.log(expon.pdf(sigma[1], scale=1))
        BFu = cop1 = log_prior + 0.5 * np.log(inv(hes_norm))
        hes = det(hes_norm)

    BF = 1

    result = {"theta": theta, "cop1": cop1, "hes": hes, "hes_prior_cor": hes_prior_cop, "BF": BF, "BFu": BFu}

    return result

# Test #
if __name__ == "__main__":
    df = read_excel("../data/artificial_data.xlsx", sheet_name='Sheet1')
    x = []
    y = []

    for index, row in df.iterrows():
        x.append([float(row['x'])])
        y.append([float(row['y'])])

    x = np.asarray(x, dtype=np.float32)
    y = np.asarray(y, dtype=np.float32)

    result = allfrank(x, y)

    print(result)
