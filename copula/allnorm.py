from __future__ import division 
from scipy.stats import norm
from pandas import read_excel
import numpy as np

# Transform to normal distribution #
def allnorm(x, y):

    sample = len(x)

    # Estimate norm parameters #
    phat1 = norm.fit(x, loc=0, scale=1)
    meanx = phat1[0]
    sigmax = phat1[1]

    phat2 = norm.fit(y, loc=0, scale=1)
    meany = phat2[0]
    sigmay = phat2[1]

    # Save frequent  calculations #
    x_minus_mean_x = x - meanx
    y_minus_mean_y = y - meany
    sigmax_pow_3 = sigmax ** 3
    sigmax_pow_2 = sigmax ** 2
    sigmay_pow_3 = sigmay ** 3
    sigmay_pow_2 = sigmay ** 2
    minus_sample = -sample

    # Calculate hessian matrix of log-likelihood #
    hes_normx = np.array([[minus_sample / (sigmax_pow_2), -2*np.sum(x_minus_mean_x) / (sigmax_pow_3)],
                           [-2*np.sum(x_minus_mean_x) / (sigmax_pow_3), (sample / (sigmax_pow_2)) - (3*np.sum((x_minus_mean_x)**2) / (sigmax**4))]
                          ])

    hes_normy = np.array([[minus_sample / (sigmay_pow_2), -2*np.sum(y_minus_mean_y) / (sigmay_pow_3)],
                           [-2*np.sum(x - meany) / (sigmay_pow_3), (sample / (sigmay_pow_2)) - (3*np.sum((y_minus_mean_y)**2) / sigmay**4)]
                          ])

    # Calculate cumulative of x and y #
    u = norm.cdf(x_minus_mean_x / sigmax, loc=0, scale=1)
    v = norm.cdf(y_minus_mean_y / sigmay, loc=0, scale=1)

    # Fix output #
    zeros_tmp = np.zeros((2, 2))

    new_hes_normx = np.concatenate((hes_normx, zeros_tmp), axis=1)
    new_hes_normy = np.concatenate((zeros_tmp, hes_normy), axis=1)

    hes_norm = np.concatenate((new_hes_normx, new_hes_normy), axis=0)

    sigma = [sigmax, sigmay, meanx, meany]


    # Fix overflow #
    for i in range(len(u)):
        if u[i] == 1:
            u[i] = 0.99999999 
        if v[i] == 1:
            v[i] = 0.99999999 

    result = {"sigma": sigma,
              "hes_norm": hes_norm,
              "u": u, "v": v
              }

    return result

# Test #
if __name__ == "__main__":

    df = read_excel("/home/petropoulakis/Desktop/artificial_data.xlsx", sheet_name='Sheet1')
    x = []
    y = []

    for index, row in df.iterrows():
        x.append([float(row['x'])])
        y.append([float(row['y'])])

    result = allnorm(x, y)

    print(result['sigma'])
    print(result['hes_norm'])
    print(result['u'][:5])
    print(result['v'][:5])
