from __future__ import division 
from scipy.stats import norm, expon
from scipy.linalg import det, inv
from allnorm import allnorm
from pandas import read_excel
from copulae import ClaytonCopula
import numpy as np
from math import pi

def allclayton(x, y, thetaInit=1.4):
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
    data = []
    for i in range(len(u)):
        data.append([u[i][0], v[i][0]])
   
    data = np.array(data)
    cop = ClaytonCopula(theta=thetaInit)
    cop.fit(data)
    theta = cop.params  
    
    # Save frequent calculations #
    v_pow_minus_theta = v ** (-theta)
    u_pow_minus_theta = u ** (-theta)
    minus_sample = -sample

    # Find logLikelihood of theta #
    cop1 = (sample * np.log(1 + theta)) - ((theta + 1) * np.sum(np.log(u * v)))  - ((np.sum(np.log((u ** (-theta)) +  (v ** (-theta)) -1))) * (2 + (1/theta))) - (0.5 * sample * np.log(2 * pi * (sigma[0] ** 2))) - (0.5 * np.sum(xbar ** 2) / (sigma[0] ** 2)) - (0.5 * sample * np.log(2 * pi * (sigma[1] ** 2))) - (0.5 * np.sum(ybar ** 2) / (sigma[1] ** 2))
    
    # Calculate hessian of log-copula's density #
    hes_cop = (minus_sample / ((theta + 1)**2)) -2 * (theta ** (-3) * np.sum(np.log(u_pow_minus_theta + v_pow_minus_theta - 1))) - 2*(theta ** (-2)) * np.sum(np.divide(np.multiply(np.log(u), u_pow_minus_theta) +  np.multiply(np.log(v), v_pow_minus_theta),u_pow_minus_theta + v_pow_minus_theta - 1)) - (2 + (1/theta))*np.sum(np.divide(np.multiply(np.multiply(np.log(u) ** 2, u ** (-theta)) + np.multiply(np.log(v) ** 2, v_pow_minus_theta), u_pow_minus_theta + v_pow_minus_theta - 1) - ((np.multiply((u_pow_minus_theta), np.log(u)) + np.multiply((v_pow_minus_theta), np.log(v)))** 2), (((u ** (-theta))  + (v ** (-theta)) - 1) ** 2)))

    s = minus_sample / hes_cop
    hes_prior_cop = -1 / (s ** 2)
    # Opou loc valame scale apo ton deutero log kai meta.
    log_prior = np.log(norm.pdf(theta, loc=0, scale=s)) + np.log(expon.pdf(sigma[0], scale=1)) + np.log(expon.pdf(sigma[1], scale=1))
    BF = 1
    # Vgazoume to inv kai vazoume -1/
    BFu = cop1 + log_prior + 0.5 * np.log(-1/(det(hes_norm) * (hes_cop - hes_prior_cop)))
    hes = det(hes_norm) * (hes_cop - hes_prior_cop)

    if theta < 10**(-5):
        theta = 0
        cop1 = 0
        BFu = cop1 + log_prior + 0.5 * np.log(-det(np.matmul(hes_norm, hes_cop - hes_prior_cop)))

    result = {"theta": theta, "cop1": cop1, "hes": hes, "hes_prior_cor": hes_prior_cop, "BF": BF, "BFu": BFu}

    return result

# Test #
if __name__ == "__main__":
    df = read_excel("/home/petropoulakis/Desktop/artificial_data.xlsx", sheet_name='Sheet1')
    x = []
    y = []

    for index, row in df.iterrows():
        x.append([float(row['x'])])
        y.append([float(row['y'])])

    x = np.asarray(x, dtype=np.float32)
    y = np.asarray(y, dtype=np.float32)

    result = allclayton(x, y)

    print(result)
