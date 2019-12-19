import numpy as np
from scipy.stats import mode

def favoredmodel(current_model, QQ):

    n = current_model.shape[1]
    m = current_model.shape[0]
    kcum = np.zeros(shape=(n, 1))

    for i in range(n):
        j = np.count_nonzero(current_model[:i] == 0, axis=0)[0]
        kcum[i][0] = m - j

    maxNumBreaks = mode(kcum, axis = 0).mode

    z = 0
    for i in range(n):

        j = np.count_nonzero(current_model[:i] == 0, axis=0)[0]
        if m - j == maxNumBreaks:
            z += 1
            Q[:z] = QQ[:i]
            favor[:z] = current_model[:i]

    result = {"kcum": kcum, "Q": Q, "favor": favor}

    return result

if __name__ == "__main__":

    current_model = np.array([[0], [1], [2], [3]])
    QQ = 5

    result = favoredmodel(current_model, QQ)

    print(result)
