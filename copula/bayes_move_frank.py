import numpy as np
from allfrank import allfrank

def bayes_move_frank(currentModel, newModel, kn, u, v, s, q, Q, zita, chain):

    current = np.sort(currentModel)
    new = np.sort(newModel)
    # Check function no purpose ? #

    t1 = new[current != 0]
    t2 = new[new != 0]
    min_old = np.argmax(t1)
    max_old = np.argmax(t1)
    min_new = np.argmax(t2)
    max_new = np.argmax(t2)
    L = len(u)
    l = len(current)
    #thetastart = [1.4, 0.05, 0.05]
    ss = -1
    R = 1

    if min_new < min_old and max_old != min_old:
        result1 = allfrank(u[:, min_new], v[:, min_new])
        result2 = allfrank(u[min_new + 1, t1[1]], v[min_new + 1, t1[1]])
        resultOld1 = allfrank(u[:, min_old], v[:, min_old])
        resultOld2 = allfrank(u[min_old + 1, t1[1]], v[min_old + 1, t1[1]])

        BFu = result1["BFu"] + result2["BFu"] - resultOld1["BFu"] - resultOld2["BFu"]
        if  BFu.imag:
            s = -2
            print("error")

        U2 = np.random.uniform()

        if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and BFu.imag == 0:
            new_model = new
            rejected = current
            w = 1
        else:
            new_model = current
            rejected = new
            w = 2

    else:
        if min_new > min_old and max_old != min_old:
            result1 = allfrank(u[:, min_new], v[:, min_new])
            result2 = allfrank(u[min_new + 1, t1[1]], v[min_new + 1, t1[1]])
            resultOld1 = allfrank(u[:, min_old], v[:, min_old])
            resultOld2 = allfrank(u[min_old + 1, t1[1]], v[min_old + 1, t1[1]])

            BFu = result1["BFu"] + result2["BFu"] - resultOld1["BFu"] - resultOld2["BFu"]
            if  BFu.imag:
                s = -2
                print("error")

            U2 = np.random.uniform()

            if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and BFu.imag == 0:
                new_model = new
                rejected = current
                w = 3
            else:
                new_model = current
                rejected = new
                w = 4

        elif (min_new < min_old or max_new > max_old) and max_old != min_old:
            result1 = allfrank(u[:, t2], v[:, t2])
            result2 = allfrank(u[t2 + 1, L], v[t2 + 1, L])
            resultOld1 = allfrank(u[:, t1], v[:, t1])
            resultOld2 = allfrank(u[t1 + 1, L], v[t1 + 1, L])

            BFu = result1["BFu"] + result2["BFu"] - resultOld1["BFu"] - resultOld2["BFu"]
            if  BFu.imag:
                s = -2
                print("error")

            U2 = np.random.uniform()

            if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and BFu.imag == 0:
                new_model = new
                rejected = current
                w = 5
            else:
                new_model = current
                rejected = new
                w = 6

        elif max_new > max_old and max_old != min_old:
            result1 = allfrank(u[t1[kn - 1], max_new], v[t1[kn - 1], max_new])
            result2 = allfrank(u[max_new + 1, L], v[max_new + 1, L])
            resultOld1 = allfrank(u[t1[kn - 1], t1[kn]], v[t1[kn - 1], t1[kn]])
            resultOld2 = allfrank(u[t1[kn] + 1, L], v[t1[kn]+ 1, L])

            BFu = result1["BFu"] + result2["BFu"] - resultOld1["BFu"] - resultOld2["BFu"]
            if  BFu.imag:
                s = -2
                print("error")

            U2 = np.random.uniform()

            if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and BFu.imag == 0:
                new_model = new
                rejected = current
                w = 7
            else:
                new_model = current
                rejected = new
                w = 8

        elif max_new < max_old and max_old != min_old:
            result1 = allfrank(u[t1[kn - 1], max_new], v[t1[kn - 1], max_new])
            result2 = allfrank(u[max_new + 1, L], v[max_new + 1, L])
            resultOld1 = allfrank(u[t1[kn - 1], t1[kn]], v[t1[kn - 1], t1[kn]])
            resultOld2 = allfrank(u[t1[kn] + 1, L], v[t1[kn]+ 1, L])

            BFu = result1["BFu"] + result2["BFu"] - resultOld1["BFu"] - resultOld2["BFu"]
            if  BFu.imag:
                s = -2
                print("error")

            U2 = np.random.uniform()

            if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and BFu.imag == 0:
                new_model = new
                rejected = current
                w = 9
            else:
                new_model = current
                rejected = new
                w = 10

        elif min_new == min_old and max_old == min_old:
            result1 = allfrank(u[t2[kn - 1], max_new], v[t2[kn - 1], max_new])
            result2 = allfrank(u[t2[kn], t2[kn + 1]], v[t2[kn], t2[kn + 1]])
            resultOld1 = allfrank(u[t1[kn - 1], t1[kn]], v[t1[kn - 1], t1[kn]])
            resultOld2 = allfrank(u[t1[kn], t1[kn + 1] + 1], v[t1[kn], t1[kn + 1] + 1])

            BFu = result1["BFu"] + result2["BFu"] - resultOld1["BFu"] - resultOld2["BFu"]
            if  BFu.imag:
                s = -2
                print("error")

            U2 = np.random.uniform()

            if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and BFu.imag == 0:
                new_model = new
                rejected = current
                w = 11
            else:
                new_model = current
                rejected = new
                w = 12

    QQ = q
 
    result = {"new_model": new_model, "rejected": rejected, "w": w, "QQ": QQ, "ss": ss}

    return result

