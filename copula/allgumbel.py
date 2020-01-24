from scipy.stats import norm, expon
from scipy.optimize import minimize
from scipy.linalg import det, inv
from math import pi
import numpy as np
from allnorm import allnorm
from copulalib import Copula
from pandas import read_excel

np.set_printoptions(precision=20)

def allgumbel(x, y):

    sample = len(x)

    # Convert to normall #
    result = allnorm(x, y)

    u = result["u"]
    v = result["v"]
    sigma = result["sigma"]
    hes_norm = result["hes_norm"]

    lu = -np.log(u)
    lv = -np.log(v)
    
    # x - mean, y - mean #
    xbar = x - sigma[2]
    ybar = y - sigma[3]

    # Calculate theta #
    theta = Copula(x.flatten(),y.flatten(), family='gumbel').theta
    theta = 2.711597926774898
    # Find logLikelihood of theta #
    cop1 = logLikelihood(theta, lu, lv, sample, sigma, xbar, ybar, u, v) 

    # Calculate hessian of log-copula's density #
    hes = -np.sum(2 * (theta **(-3)) * np.log(lu ** theta + lv ** theta) - np.multiply((-2 * (theta ** (-2))) * (((lu ** theta) + (lv ** theta)) ** (-1)), np.multiply(lu ** theta, np.log(lu)) + np.multiply(lv ** theta, np.log(lv))) - np.multiply((((lu ** theta) + (lv ** theta)) ** (-2)) * (-2 + (1/theta)), ((np.multiply(lu ** theta, np.log(lu)) + np.multiply(lv ** theta, np.log(lv))) ** 2)) + (theta ** (-3))* np.multiply((2*((lu ** theta) + (lv * theta))) **(-1 + (1/theta)), (theta * (np.multiply(lu ** theta, np.log(lu)) + np.multiply(lv ** theta, np.log(lv)))) - np.multiply(((lu ** theta) + (lv ** theta)), np.log((lu ** theta) + (lv ** theta)))) + (theta ** (-4))*(np.multiply(np.multiply(((lu ** theta) + (lv * theta)) ** (-2 + (1/theta)), (theta * (np.multiply(lu ** theta, np.log(lu)) + np.multiply(lv ** theta, np.log(lv)))) - np.multiply(((lu ** theta) + (lv ** theta)), np.log((lu ** theta) + (lv ** theta)))), ((-1 + theta) * theta) * (np.multiply(lu ** theta, np.log(lu)) + np.multiply(lv ** theta, np.log(lv))) + np.multiply(((lu ** theta) + (lv ** theta)), np.log((lu ** theta) + (lv ** theta))))) + np.multiply((-2 + (1/theta)) * (((lu ** theta) + (lv ** theta)) ** (-1)), np.multiply(lu ** theta, np.log(lu ** 2)) + np.multiply(lv ** theta, np.log(lu ** 2))) + (theta ** (-2)) * (np.multiply((((lu ** theta) + (lv ** theta)) ** (-1 + (1/theta))), -theta *(np.multiply(lu ** theta, np.log(lu ** 2)) + np.multiply(lv ** theta, np.log(lv ** 2))) + np.multiply(np.log((lu ** theta) + (lv ** theta)),   np.multiply(lu ** theta, np.log(lu)) + np.multiply(lv ** theta, np.log(lv))))) -np.divide(((np.multiply(np.multiply(theta *(lu ** theta), ((lu ** theta) + (lv ** theta)) ** (1/theta)), np.log(lu)) -np.multiply(((lu ** theta) + (lv ** theta)) ** (1 + (1/theta)), np.log((lu ** theta) + (lv ** theta))) + theta*(theta * ((lu ** theta) + (lv ** theta)) + np.multiply(np.multiply(((lu ** theta) + (lv ** theta)) ** (1/theta),lv ** theta), np.log(lv)))) ** (-2)),  np.multiply((theta ** 4) * ( -1 + theta + (((lu ** theta) + (lv ** theta)) ** (1/theta))), ((lu ** theta) + (lv ** theta)) ** 2)) + np.divide(np.multiply((((lu ** theta) + (lv ** theta)) ** (-2 + (1/theta))), np.multiply(np.multiply(np.multiply((theta ** 2) * (lu ** theta), (lu ** theta) + (lv ** theta)), np.log(lu ** 2)) + np.multiply((((lu ** theta) + (lv ** theta)) ** 2),  np.log((lu ** theta) + (lv ** theta)) ** 2) + np.multiply(np.multiply((theta ** 2) * (lv ** theta), np.log(lv)), -2 *((lu ** theta) + (lv ** theta)) + np.multiply((lu ** theta) + (lv ** theta), np.log(lv))) + np.multiply(np.multiply(2 * theta * ((lu ** theta) + (lv ** theta)), np.log((lu ** theta) + (lv ** theta))),(lu ** theta) + (lv ** theta) -(np.multiply(lv ** theta, np.log(lv)))) -np.multiply(2 * theta * (lu ** theta), np.log(lu)), np.multiply((lu ** theta) + (lv ** theta), np.log((lu ** theta) + (lv ** theta))) + theta * (((lu ** theta) + (lv ** theta)) + np.multiply((-1 + theta) * (lv ** theta), np.log(lv))))), (theta ** 4) * (-1 + theta + (((lu ** theta) + (lv ** theta)) ** (1/theta)))))
    print(hes)
    hes_cop = - hes

    s = -sample / hes_cop
    hes_prior_cop = -1 / (s ** 2)

    log_prior = np.log(norm.pdf(theta, loc=0, scale=s)) + np.log(expon.pdf(sigma[0], scale=1)) + np.log(expon.pdf(sigma[1], scale=1))
    BF = 1
    BFu = cop1 + log_prior + 0.5 * np.log(-1/(det(hes_norm) * (hes_cop - hes_prior_cop)))
    hes = det(hes_norm) * (hes_cop - hes_prior_cop)

    result = {"theta": theta, "cop1": cop1, "hes": hes, "hes_prior_cor": hes_prior_cop, "BF": BF, "BFu": BFu}

    return result

# Log-likelihood #
def logLikelihood(theta, lu, lv, sample, sigma, xbar, ybar, u, v):

    lLikelihood = np.sum(np.log(np.exp((-(lu ** theta + lv ** theta) ** (1.0/theta))))) - np.sum(np.log(u) + np.log(v)) + ((-2 + (1.0/theta)) * np.sum(np.log((lu ** theta) + (lv ** theta)))) + ((theta - 1) * np.sum(np.log(lu) + np.log(lv))) + np.sum(np.log((theta - 1) + np.power((lu ** theta) + (lv ** theta), 1.0/theta))) - (0.5 * sample * np.log(2* pi * (sigma[0] ** 2))) - (0.5 * np.sum(xbar ** 2) / (sigma[0] ** 2)) - (0.5 * sample * np.log(2* pi * (sigma[1] ** 2))) - (0.5 * np.sum(ybar ** 2) / (sigma[1] ** 2))
    
    return lLikelihood

# Test #
if __name__ == "__main__":
    df = read_excel("/home/petropoulakis/Desktop/artificial_data_iosif.xlsx", sheet_name='Sheet1')
    x = []
    y = []

    for index, row in df.iterrows():
        x.append([float(row['x'])])
        y.append([float(row['y'])])

    x = np.asarray(x, dtype=np.float32)
    y = np.asarray(y, dtype=np.float32)

    result = allgumbel(x, y)

    print(result)
