from scipy.stats import norm
import numpy as np

# Test comment

# TODO fminsearch + indeterminacy #

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

    # Calculate hessian matrix of log-likelihood #
    hes_normx = np.array([[-sample / (sigmax**2), -2*np.sum(x - meanx) / (sigmax**3)],
                           [-2*np.sum(x - meanx) / (sigmax**3), (sample / (sigmax**2)) - (3*np.sum((x - meanx)**2) / (sigmax**4))]
                          ])

    hes_normy = np.array([[-sample / (sigmay**2), -2*np.sum(y - meany) / (sigmay**3)],
                           [-2*np.sum(x - meany) / (sigmay**3), (sample / (sigmay**2)) - (3*np.sum((y - meany)**2) / sigmay**4)]
                          ])

    # Calculate cumulative of x and y #
    u = norm.cdf((x - meanx) / sigmax, loc=0, scale=1)
    v = norm.cdf((y - meany) / sigmay, loc=0, scale=1)

    # Fix output #
    zeros_tmp = np.zeros((2, 2))

    new_hes_normx = np.concatenate((hes_normx, zeros_tmp), axis=1)
    new_hes_normy = np.concatenate((zeros_tmp, hes_normy), axis=1)

    hes_norm = np.concatenate((new_hes_normx, new_hes_normy), axis=0)

    sigma = [sigmax, sigmay, meanx, meany]

    result = {"sigma": sigma,
              "hes_norm": hes_norm,
              "u": u, "v": v
              }

    return result

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

    result = allnorm(x, y)

    print("[ALLNORM]\n")
    print("sigma\n", result["sigma"])
    print("hess_norm\n", result["hes_norm"])
    print("u\n", result["u"])
    print("v\n", result["v"])
