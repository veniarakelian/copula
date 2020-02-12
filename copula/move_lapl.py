import numpy as np
from pandas import read_excel

def move_lapl(currentModel, u, v, dist, numbrk, q):

    new = np.sort(currentModel)
    sample = len(u)
    j = np.count_nonzero(currentModel == 0, axis=0)
    L = len(currentModel) - j

    current = new[new != 0]
    current = np.append(current, np.zeros(j))
    pick = np.random.randint(low=1, high=L + 1)
    b2 = current[pick - 1]
    scale = 5
    kn = np.random.randint(low=b2 - scale, high=b2 + scale + 1)
    current[pick - 1] = kn
    current[L:L + j] = 0 * np.zeros(j)
    current = np.sort(current)

    if pick == 1 and j < numbrk - 1:

        z = (np.absolute(kn - current[pick + j]) >= dist) and (kn >= dist - 1) and (sample - kn > dist) and (kn - new[pick + j - 1] != 0)

        if kn - new[pick + j - 1] > 0:
            s = q[pick]
        else:
            s = q[pick - 1]
    else:
        if pick == 1 and j == numbrk - 1:

            z = (kn >= dist - 1) and (sample - kn > dist) and (kn - new[pick + j - 1] != 0)
            if kn - new[pick + j - 1] > 0:
                s = q[pick]
            else:
                s = q[pick - 1]
        else:
            if pick == L:
                z = (np.absolute(kn - current[pick + j - 2]) >= dist) and (kn >= dist - 1) and (sample - kn > dist) and (kn - new[pick + j - 1] != 0)

                if kn - new[pick + j - 1] > 0:
                    s = q[pick]
                else:
                    s = q[pick - 1]
            else:
                z = np.absolute(kn - current[pick - 2 + j] >= dist) and (np.absolute(kn - current[pick + j] >= dist)) and (kn >= dist - 1) and (sample - kn > dist) and (kn - new[pick + j - 1] != 0)
                if kn - new[pick + j - 1] > 0:
                    s = q[pick]
                else:
                    s = q[pick - 1]

    Q = q
    new_model = np.sort(current)

    result = {"new_model": new_model, "pick": pick, "z": z, "Q": Q, "s": s}

    return result

# Test #
if __name__ == "__main__":
    df = read_excel("/home/petropoulakis/Desktop/artificial_data_iosif.xlsx", sheet_name='Sheet1')
    u = []
    v = []

    for index, row in df.iterrows():
        u.append([float(row['u'])])
        v.append([float(row['v'])])

    u = np.asarray(u, dtype=np.float32)
    v = np.asarray(v, dtype=np.float32)
    dist = 30
    numbrk = 5
    q = [2, 2, 2, 2, 2, 2]

    currentModel = np.zeros(numbrk, dtype=int)
    currentModel[4] = 250
    currentModel[3] = 150
    currentModel[2] = 100
    currentModel[1] = 5


    result = move_lapl(currentModel, u, v, dist, numbrk, q)

    print(result)
