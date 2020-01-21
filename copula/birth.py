import numpy as np
from itertools import combinations
from pandas import read_excel
from numpy.linalg import inv

def birth(currentModel, u, dist, numbrk, q):

    sample = len(u)
    j = np.count_nonzero(currentModel == 0)
    L = len(currentModel) - j
    new = np.sort(currentModel)

    k = np.random.uniform(low=dist, high=sample - dist + 1)
    w = np.random.uniform()

    k = 290

    if j < numbrk and not np.all(np.any(np.absolute(k * np.ones(shape=(L+j)) - new)  <= dist * np.ones(shape=(L+j,1)))):
        z = 1
        kn = k
        new[j - 1] = kn
        bir = np.sort(new)
        j2 = np.count_nonzero(new == 0)
        d = np.argwhere(bir == kn) + 1
        d = int(d)
        t2 = currentModel[np.sort(currentModel) != 0]

        if kn > np.max(t2):

            Q = np.ones(numbrk + 1)
            Q[:numbrk - j2 - 1] = q[:numbrk - j2 - 1]
            temp = [comb for comb in combinations([1, 2, 3], 2)]
            j = 0
            G = 0

            while j < 3 and G == 0:

                if np.all(temp[j] != np.ones(shape=(1,2)) * q[:numbrk - j2 - 1]):
                    G = 1
                    del temp[j]

                j += 1

            a = np.random.uniform()
            row = np.random.randint(low=1 , high=3)

            row = 2
            a = 0.26
            if a < float(1)/3:
                Q[numbrk - j2 - 1:numbrk - j2 + 1] = list(temp[row - 1])
            else:
                if a >= 1/3 and a < 2/3:
                    Q[numbrk - j2 - 1: numbrk - j2 + 1] = np.fliplr(temp[row:]).H
                else:
                    if a >= 2/3:
                        Q[numbrk - j2 - 1: numbrk - j2 + 1] = np.ones(shape=(2,1)) * q[numbrk - j2][0]

            Q[d - j2:numbrk + 1] = Q[d - j2]
            s = np.concatenate((np.asarray([q[numbrk - j2 - 1]]), Q[numbrk - j2 - 1: numbrk - j2 + 1]), axis=0)
        else:
            if kn < np.min(t2):
                Q = np.zeros(shape=(numbrk + 1, 1))
                Q[2:numbrk + 1] = q[1:numbrk]
                temp = [comb for comb in combinations([1, 2, 3], 2)]
                j = 0
                G = 0

                while j < 3 and G == 0:
                    if np.all(temp[j:] != np.ones(shape=(1,2)) * q[0]):
                        G = 1
                        temp[j:] = []

                    j += 1

                a = np.random.uniform()
                row = np.random.uniform(low=1 , high=2)

                if a < 1/3:
                    Q[:2] = temp[row:].H
                else:
                    if a >= 1/3 and a < 2/3:
                        Q[:2] = np.fliplr(temp[row:]).H
                    else:
                        if a >= 2/3:
                            Q[:2] = np.ones(shape=(2,1)) * q[1][0]

                s = np.concatenate((q[0], Q[:2]), axis=0)

            else:
                Q[:d - j2 - 1] = q[:d - j2 - 1]
                temp = [comb for comb in combinations([1, 2, 3], 2)]

                j = 0
                G = 0
                while j < 3 and G == 0:
                    if np.all(temp[j:] != np.ones(shape=(1,2)) * q[d - j2]):
                        G = 1
                        temp[j:] = []

                    j += 1

                a = np.random.uniform()
                row = np.random.uniform(low=1 , high=2)

                if a < 1/3:
                    Q[d - j2 - 1:d - j2 + 1] = temp[row:].H
                else:
                    if a >= 1/3 and a < 2/3:
                        Q[d - j2 - 1:d - j2 + 1] = np.fliplr(temp[row:]).H
                    else:
                        if a >= 2/3:
                            Q[d - j2 - 1:d - j2 + 1] = np.ones(shape=(2,1)) * q[d - j2][0]

                Q[d - j2 + 1: numbrk + 1] = q[d - j2:numbrk]
                s = np.concatenate((q[d - j2 - 1], Q[d - j2 - 1:d - j2 + 1]), axis=0)

    elif j == numbrk and not np.all(np.any(np.absolute(k * np.ones(shape=(L+j,1)) - new), axis=0) <= dist* np.ones(shape=(L+j,1))):
        z = 1
        kn = k
        new[j][0] = kn
        bir = np.sort(new)
        temp = [comb for comb in combinations([1, 2, 3], 2)]
        j = 0
        G = 0

        while j < 3 and G == 0:
            if np.all(temp[j:] != np.ones(shape=(1,2)) * q[0]):
                G = 1
                temp[j:] = []

            j += 1

        a = np.random.uniform()
        row = np.random.uniform(low=1 , high=2)

        if a < 2/3:
            d = np.random.uniform()
            if d < 1/2:
                Q[0][0] = temp[row][0]
                Q[:numbrk + 1] = np.ones(shape=(numbrk,1))  * temp([row][1])
            else:
                Q[0][0] = temp[row][1]
                Q[:numbrk + 1] = np.ones(shape=(numbrk,1))  * temp([row][0])
        else:
            Q = q

        s = np.concatenate((q[0], Q[:2]), axis=0)

    elif np.all(np.any(np.absolute(k * np.ones(shape=(L+j,1)) - new), axis=0) <= dist* np.ones(shape=(L+j,1))):
        z = -3
        bir = currentModel
        kn = k
        Q = q
        s = 0

    result = {"bir": bir, "kn": kn, "s": s, "Q": Q, "q": q, "z": z}


    return result

# Test #
if __name__ == "__main__":

    df = read_excel("/home/petropoulakis/Desktop/artificial_data_iosif.xlsx", sheet_name='Sheet1') #, header=None)

    u = []

    for index, row in df.iterrows():
        u.append([float(row['u'])])

    u = np.asarray(u, dtype=np.float32)

    dist = 30
    numbrk = 5
    currentModel = np.zeros(numbrk)
    currentModel[numbrk - 1] = 50
    q = np.ones(numbrk + 1)

    result = birth(currentModel, u, dist, numbrk, q)

    print(result)
