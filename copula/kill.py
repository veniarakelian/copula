import numpy as np
from itertools import combinations

def kill(currentModel, numbrk, q):

    current = np.sort(currentModel)
    j = np.count_nonzero(currentModel == 0)
    L = len(currentModel) - j
    l = len(currentModel)

    kn = np.random.randint(low=0, high=L - 1)

    currentModel[kn + j - 1:] = 0
    newModel = np.sort(currentModel)
    Kn = kn + j
    w = np.random.uniform()
    Q = q

    if(Kn >= numbrk and L != 1):
        if(q[kn - 1][0] != q[kn][0]):
            if(w <= 1/2):
                Q[kn - 1: numbrk + 1] = q[kn]
            else:
                Q[kn - 1: numbrk + 1] = q[kn - 1]
        else:
            Q[kn - 1: numbrk + 1] = q[kn - 1]

        s = np.concatenate((q[kn - 1], Q[kn]), axis=0)

    else:
        if(Kn == numbrk and L == 1):
            if(q[0][0] != q[1][0]):
                Q = q
            else:
                if(w <= 1/2):
                    Q = q[0][0] * np.ones(shape=(numbrk + 1,1))
                else:
                    Q = q[1][0] * np.ones(shape=(numbrk + 1,1))

            s = np.concatenate((q[0], q[1], Q[0]), axis=0)

        else:
            temp = Q[kn - 1]
            Q[kn - 1] = []
            if q[kn][0] != q[kn - 1][0]:
                if w <= 1/2:
                    Q[kn - 1] = q[kn]
                else:
                    Q[kn - 1] = q[kn - 1]
            else:
                Q[kn - 1] = q[kn - 1]

            Q[l] = q[l]
            s = np.concatenate((q[kn - 1], q[kn], Q[kn - 1]), axis=0)

    result = {"newModel": newModel, "Kn": Kn, "s": s, "Q": Q, "q": q}

    return result

# Test #
if __name__ == "__main__":

    numbrk = 5
    q = np.ones(numbrk + 1)
    currentModel = np.zeros(numbrk)

    result = kill(currentModel, numbrk, q)

    print(result)
