from __future__ import division 
import numpy as np
from itertools import combinations

def kill(currentModel, numbrk, q):

    current = np.sort(currentModel)
    j = np.count_nonzero(current == 0, axis=0)
    L = len(current) - j
    l = len(current)
    
    kn = np.random.randint(low=1, high=L + 1)
    current[kn + j - 1] = 0
    newModel = np.sort(current)
    Kn = kn + j
    w = np.random.uniform(low=np.nextafter(0.0, 1.0))
    Q = q[:]

    if(Kn >= numbrk and L != 1):
        if(q[kn - 1] != q[kn]):
            if(w <= 1.0/2):
                Q[kn - 1: numbrk + 1] = q[kn] * np.ones(shape=(numbrk + 2 - kn))
            else:
                Q[kn - 1: numbrk + 1] = q[kn - 1] * np.ones(shape=(numbrk + 2 - kn))

        else:
            Q[kn - 1: numbrk + 1] = q[kn - 1] * np.ones(shape=(numbrk + 2 - kn))

        s = np.concatenate((np.asarray([q[kn - 1]]), np.asarray([q[kn]]), np.asarray([Q[kn]])), axis=0)

    else:
        if(Kn == numbrk and L == 1):
            if q[0] != q[1]:
                Q = q[:]
            else:
                if(w <= 1.0/2):
                    Q = q[0] * np.ones(shape=(numbrk + 1))
                else:
                    Q = q[1] * np.ones(shape=(numbrk + 1))

            s = np.concatenate((np.asarray([q[0]]), np.asarray([q[1]]), np.asarray([Q[0]])), axis=0)

        else:
            Q = np.delete(Q, kn - 1)

            if q[kn] != q[kn - 1]:
                if w <= 1.0/2:
                    Q[kn - 1] = q[kn]
                else:
                    Q[kn - 1] = q[kn - 1]
            else:
                Q[kn - 1] = q[kn - 1]

            Q = np.append(Q, q[l])
            s = np.concatenate((np.asarray([q[kn - 1]]), np.asarray([q[kn]]), np.asarray([Q[kn - 1]])), axis=0)

    result = {"newModel": newModel, "Kn": Kn, "s": s, "Q": Q, "q": q}

    return result

# Test #
if __name__ == "__main__":

    numbrk = 5
    q = [1, 2, 2, 3, 3, 3]
    currentModel = np.zeros(numbrk, dtype=int)
    currentModel[2] = 100
    currentModel[3] = 180
    currentModel[4] = 250    

    result = kill(currentModel, numbrk, q)

    print(result)
