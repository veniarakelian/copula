from scipy.stats import norm
import numpy as np

# TODO fminsearch + indeterminacy #

def allnorm(x, y):
    sample = len(x)

    # Estimate norm parameters #
    phat1 = norm.fit(x, loc=0, scale=1)
    meanx = phat1[0]
    sigmax = phat1[1]

    phat2 = norm.fit(y, loc=0, scale=1)
    meany = phat2[0]
    sigmay = phat2[1]

    # Calculate hessian matrix of log-likelihood #
    hess_normx = np.array([[-sample / (sigmax**2), -2*np.sum(x - meanx) / (sigmax**3)],
                           [-2*np.sum(x - meanx) / (sigmax**3), (sample / (sigmax**2)) - (3*np.sum((x - meanx)**2) / (sigmax**4))]
                          ])

    hess_normy = np.array([[-sample / (sigmay**2), -2*np.sum(y - meany) / (sigmay**3)],
                           [-2*np.sum(x - meany) / (sigmay**3), (sample / (sigmay**2)) - (3*np.sum((y - meany)**2) / sigmay**4)]
                          ])


    u = norm.cdf((x - meanx) / sigmax, loc=0, scale=1)
    v = norm.cdf((y - meany) / sigmay, loc=0, scale=1)

    # Fix output #
    zeros_tmp = np.zeros((2, 2))

    new_hess_normx = np.concatenate((hess_normx, zeros_tmp), axis=1)
    new_hess_normy = np.concatenate((zeros_tmp, hess_normy), axis=1)

    hess_norm = np.concatenate((new_hess_normx, new_hess_normy), axis=0)

    sigma = [sigmax, sigmay, meanx, meany]

    result = {"sigma": sigma,
              "hess_norm": hess_norm,
              "u": u, "v": v
              }

    return result

# Test #
if __name__ == "__main__":
    x = np.array([[5], [6]])
    y = np.array([[1], [1]])

    result = allnorm(x, y)

    print("[ALLNORM]\n")
    print("sigma\n", result["sigma"])
    print("hess_norm\n", result["hess_norm"])
    print("u\n", result["u"])
    print("v\n", result["v"])
