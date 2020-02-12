import numpy as np
from allgumbel import allgumbel
from pandas import read_excel

def bayes_move_gumbel(currentModel, newModel, kn, u, v, q, zita, chain):

    current = np.sort(currentModel)
    new = np.sort(newModel)

    t1 = current[current != 0]
    t2 = new[new != 0]

    min_old = int(np.min(t1))
    max_old = int(np.max(t1))
    min_new = int(np.min(t2))
    max_new = int(np.max(t2))
    L = len(u)
    l = len(current)

    s = -1
    R = 1.0

    # Initialize variables #
    if min_new < min_old and max_old != min_old:
        result1 = allgumbel(u[:min_new], v[:min_new])
        result2 = allgumbel(u[min_new: t1[1]], v[min_new:t1[1]])
        resultOld1 = allgumbel(u[:min_old], v[:min_old])
        resultOld2 = allgumbel(u[min_old:t1[1]], v[min_old:t1[1]])

        BFu = result1["BFu"] + result2["BFu"] - resultOld1["BFu"] - resultOld2["BFu"]
        if BFu.imag:
            s = -2
            print("error\n")

        U2 = np.random.uniform(low=np.nextafter(0.0, 1.0))

        if (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and not BFu.imag:
            new_model = new
            rejected = current
            w = 1
        else:
            new_model = current
            rejected = new
            w = 2

    else:
        if min_new > min_old and max_old != min_old:
            result1 = allgumbel(u[:min_new], v[:min_new])
            result2 = allgumbel(u[min_new:t1[1]], v[min_new:t1[1]])
            resultOld1 = allgumbel(u[:min_old], v[:min_old])
            resultOld2 = allgumbel(u[min_old:t1[1]], v[min_old:t1[1]])

            BFu = result1["BFu"] + result2["BFu"] - resultOld1["BFu"] - resultOld2["BFu"]
            if BFu.imag:
                s = -2
                print("error")

            U2 = np.random.uniform(low=np.nextafter(0.0, 1.0))

            if (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and not BFu.imag:
                new_model = new
                rejected = current
                w = 3
            else:
                new_model = current
                rejected = new
                w = 4

        elif (min_new < min_old or max_new > max_old) and max_old == min_old:
            result1 = allgumbel(u[:t2[0]], v[:t2[0]])
            result2 = allgumbel(u[t2[0]:L], v[t2[0]:L])
            resultOld1 = allgumbel(u[:t1[0]], v[:t1[0]])
            resultOld2 = allgumbel(u[t1[0]:L], v[t1[0]:L])

            BFu = result1["BFu"] + result2["BFu"] - resultOld1["BFu"] - resultOld2["BFu"]
            if BFu.imag:
                s = -2
                print("error")

            U2 = np.random.uniform(low=np.nextafter(0.0, 1.0))

            if (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and not BFu.imag:
                new_model = new
                rejected = current
                w = 5
            else:
                new_model = current
                rejected = new
                w = 6

        elif max_new > max_old and max_old != min_old:
            result1 = allgumbel(u[t1[kn - 2] - 1:max_new], v[t1[kn - 2] - 1:max_new])
            result2 = allgumbel(u[max_new:L], v[max_new:L])
            resultOld1 = allgumbel(u[t1[kn - 2] - 1:t1[kn - 1]], v[t1[kn - 2] -1:t1[kn - 1]])
            resultOld2 = allgumbel(u[t1[kn - 1]:L], v[t1[kn - 1]:L])

            BFu = result1["BFu"] + result2["BFu"] - resultOld1["BFu"] - resultOld2["BFu"]
            if BFu.imag:
                s = -2
                print("error")

            U2 = np.random.uniform(low=np.nextafter(0.0, 1.0))

            if (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and not BFu.imag:
                new_model = new
                rejected = current
                w = 7
            else:
                new_model = current
                rejected = new
                w = 8

        elif max_new < max_old and max_old != min_old:
            result1 = allgumbel(u[t1[kn - 2] - 1:max_new], v[t1[kn - 2] - 1:max_new])
            result2 = allgumbel(u[max_new: L], v[max_new:L])
            resultOld1 = allgumbel(u[t1[kn - 2] - 1:t1[kn - 1]], v[t1[kn - 2] - 1:t1[kn - 1]])
            resultOld2 = allgumbel(u[t1[kn - 1]:L], v[t1[kn - 1]: L])

            BFu = result1["BFu"] + result2["BFu"] - resultOld1["BFu"] - resultOld2["BFu"]
            if BFu.imag:
                s = -2
                print("error")

            U2 = np.random.uniform(low=np.nextafter(0.0, 1.0))

            if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and not BFu.imag:
                new_model = new
                rejected = current
                w = 9
            else:
                new_model = current
                rejected = new
                w = 10

        elif min_new == min_old and max_old == max_old:
            result1 = allgumbel(u[t2[kn - 2] - 1:t2[kn - 1]], v[t2[kn - 2] - 1:t2[kn - 1]])
            result2 = allgumbel(u[t2[kn - 1]:t2[kn]], v[t2[kn - 1]:t2[kn]])
            resultOld1 = allgumbel(u[t1[kn - 2] - 1:t1[kn - 1]], v[t1[kn - 2] - 1:t1[kn - 1]])
            resultOld2 = allgumbel(u[t1[kn - 1]:t1[kn]], v[t1[kn  - 1]:t1[kn]])

            BFu = result1["BFu"] + result2["BFu"] - resultOld1["BFu"] - resultOld2["BFu"]
            if BFu.imag:
                s = -2
                print("error")

            U2 = np.random.uniform(low=np.nextafter(0.0, 1.0))

            if (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and not BFu.imag:
                new_model = new
                rejected = current
                w = 11
            else:
                new_model = current
                rejected = new
                w = 12

    QQ = q

    result = {"new_model": new_model, "rejected": rejected, "w": w, "QQ": QQ, "s": s}

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
    kn = 2
    q = [1, 2, 2, 3, 3, 3]
    zita = 1
    chain = 1

    currentModel = np.zeros(numbrk, dtype=int)
    currentModel[4] = 250
    currentModel[3] = 180
    currentModel[2] = 100

    newModel = np.zeros(numbrk, dtype=int)
    newModel[1] = 101 
    newModel[2] = 137
    newModel[3] = 180
    newModel[4] = 240

    result = bayes_move_gumbel(currentModel, newModel, kn, u, v, q, zita, chain)

    print(result)
