from __future__ import division 
import numpy as np
from allfrank import allfrank
from allclayton import allclayton
from allgumbel import allgumbel
from pandas import read_excel

def bayes_kill_max_clay(currentModel, newModel, kn, u, v, s, q, Q, zita, chain):

    current = np.sort(currentModel)
    new = np.sort(newModel)

    t1 = current[current != 0]
    min_old = np.min(t1)
    max_old = np.max(t1)
    L = len(u)
    l = len(new)
    ss = -1
    R = 3/4
 
    if np.any(new):

        t2 = new[new != 0]
        min_new = np.min(t2)
        max_new = np.max(t2)

        if min_old < min_new:
            if(s[1] == 1 and s[2] == 1):
                result1 = allclayton(u[:min_old], v[:min_old])
                result2 = allclayton(u[min_old:min_new], v[min_old:min_new])
                R = R * 1/3
            else:
                if(s[1] == 1 and s[2] == 2):
                    result1 = allclayton(u[:min_old], v[:min_old])
                    result2 = allfrank(u[min_old:min_new], v[min_old:min_new])
                    R = R * 2/3
                else:
                    if(s[1] == 2 and s[2] == 1):
                        result1 = allfrank(u[:min_old], v[:min_old])
                        result2 = allclayton(u[min_old:min_new], v[min_old:min_new])
                        R = R * 2/3
                    else:
                        if(s[1] == 3 and s[2] == 1):
                            result1 = allgumbel(u[:min_old], v[:min_old])
                            result2 = allclayton(u[min_old:min_new], v[min_old:min_new])
                            R = R * 2/3
                        else:
                            if(s[1] == 1 and s[2] == 3):
                                result2 = allclayton(u[:min_old], v[:min_old])
                                result1 = allgumbel(u[min_old:min_new], v[min_old:min_new])
                                R = R * 2/3

            resultOld = allclayton(u[:min_new], v[:min_new])

            BFu = resultOld["BFu"] - result1["BFu"] - result2["BFu"]

            if BFu.imag:
                ss = -2
                print("Error\n")

            U2 = np.random.uniform(low=np.nextafter(0.0, 1.0))

            if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and not BFu.imag:
                new_model = new
                rejected = current
                QQ = Q
                w = 13
            else:
                new_model = current
                rejected = new
                QQ = q
                w = 14

	else:
            if max_new < max_old and max_new != 0:
                if(s[1] == 1 and s[2] == 1):
                    result1 = allclayton(u[max_new - 1:max_old], v[max_new -  1:max_old])
                    result2 = allclayton(u[max_old:L], v[max_old:L])
                    R = R * 1/3
                else:
                    if(s[1] == 2 and s[2] == 1):
                        result2 = allfrank(u[max_new - 1:max_old], v[max_new - 1:max_old])
                        result1 = allclayton(u[max_old:L], v[max_old:L])
                        R = R * 2/3
                    else:
                        if(s[1] == 1 and s[2] == 2):
                            result2 = allclayton(u[max_new - 1:max_old], v[max_new - 1:max_old])
                            result1 = allfrank(u[max_old:L], v[max_old:L])
                            R = R * 2/3
                        else:
                            if(s[1] == 1 and s[2] == 3):
                                result2 = allclayton(u[max_new - 1:max_old], v[max_new - 1:max_old])
                                result1 = allgumbel(u[max_old:L], v[max_old:L])
                                R = R * 2/3
                            else:
                                if(s[1] == 3 and s[2] == 1):
                                    result1 = allgumbel(u[max_new - 1:max_old], v[max_new - 1:max_old])
                                    result2 = allclayton(u[max_old:L], v[max_old:L])
                                    R = R * 2/3

                resultOld = allclayton(u[max_new - 1:L], v[max_new - 1:L])

                BFu = resultOld["BFu"] - result1["BFu"] - result2["BFu"]

                if BFu.imag:
                    ss = -2
                    print("Error\n")
            
                U2 = np.random.uniform(low=np.nextafter(0.0, 1.0))

                if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and not BFu.imag:
                    new_model = new
                    rejected = current
                    QQ = Q
                    w = 15
                else:
                    new_model = current
                    rejected = new
                    QQ = q
                    w = 16
            else:
                place = kn
                if(s[1] == 1 and s[2] == 1):
                    result1 = allclayton(u[current[place - 2] - 1:current[place - 1]], v[current[place - 2] - 1:current[place - 1]])
                    result2 = allclayton(u[current[place - 1]:current[place]], v[current[place - 1]:current[place]])
                    R = R * 1/3
                else:
                    if(s[1] == 1 and s[2] == 2):
                        result1 = allclayton(u[current[place - 2] - 1:current[place - 1]], v[current[place - 2] - 1:current[place - 1]])
                        result2 = allfrank(u[current[place - 1]:current[place]], v[current[place - 1]:current[place]])
                        R = R * 2/3
                    else:
                        if(s[1] == 2 and s[2] == 1):
                            result1 = allfrank(u[current[place - 2] - 1:current[place - 1]], v[current[place - 2] - 1:current[place - 1]])
                            result2 = allclayton(u[current[place - 1]:current[place]], v[current[place - 1]:current[place]])
                            R = R * 2/3
                        else:
                            if(s[1] == 3 and s[2] == 1):
                                result1 = allgumbel(u[current[place - 2] - 1:current[place - 1]], v[current[place - 2] - 1:current[place - 1]])
                                result2 = allclayton(u[current[place - 1]:current[place]], v[current[place - 1]:current[place]])
                                R = R * 2/3
                            else:
                                if(s[1] == 1 and s[2] == 3):
                                    result1 = allclayton(u[current[place - 2] - 1:current[place - 1]], v[current[place - 2] - 1:current[place - 1]])
                                    result2 = allgumbel(u[current[place - 1]:current[place]], v[current[place - 1]:current[place]])
                                    R = R * 2/3

                resultOld = allclayton(u[current[place - 2] - 1:current[place - 1]], v[current[place - 2] - 1:current[place - 1]])

                BFu = resultOld["BFu"] - result1["BFu"] - result2["BFu"]

                if BFu.imag:
                    ss = -2
                    print("Error\n")

                U2 = np.random.uniform(low=np.nextafter(0.0, 1.0))

                if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and not BFu.imag:
                    new_model = new
                    rejected = current
                    QQ = Q
                    w = 17
                else:
                    new_model = current
                    rejected = new
                    QQ = q
                    w = 18

    else:
        if not np.any(new):
            R = 2

            if(s[1] == 1 and s[2] == 1):
                result1 = allclayton(u[:max_old], v[:max_old])
                result2 = allclayton(u[max_old:L], v[max_old:L])
                R = R * 1/3
            else:
                if(s[1] == 1 and s[2] == 2):
                    result1 = allclayton(u[:max_old], v[:max_old])
                    result2 = allfrank(u[max_old:L], v[max_old:L])
                    R = R * 2/3
                else:
                    if(s[1] == 2 and s[2] == 1):
                        result1 = allfrank(u[:max_old], v[:max_old])
                        result2 = allclayton(u[max_old:L], v[max_old:L])
                        R = R * 2/3
                    else:
                        if(s[1] == 1 and s[2] == 3):
                            result1 = allclayton(u[:max_old], v[:max_old])
                            result2 = allgumbel(u[max_old:L], v[max_old:L])
                            R = R * 2/3
                        else:
                            if(s[1] == 3 and s[2] == 1):
                                result2 = allgumbel(u[:max_old], v[:max_old])
                                result1 = allclayton(u[max_old:L], v[max_old:L])
                                R = R * 2/3

            resultOld = allclayton(u, v)

            BFu = resultOld["BFu"] - result1["BFu"] - result2["BFu"]

            if BFu.imag:
                ss = -2
                print("Error\n")

            U2 = np.random.uniform(low=np.nextafter(0.0, 1.0))

            if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and BFu.imag == 0:
                new_model = new
                rejected = current
                QQ = Q
                w = 19
            else:
                new_model = current
                rejected = new
                QQ = q
                w = 20

    result = {"new_model": new_model, "rejected": rejected, "w": w, "QQ": QQ, "ss": ss}

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

    numbrk = 5

    currentModel = np.zeros(numbrk, dtype=int)
    currentModel[2] = 100
    currentModel[3] = 180
    currentModel[4] = 250

    newModel = np.zeros(numbrk, dtype=int)
    
    kn = 4
    s = [2, 1, 2]
    q = [1, 2, 2, 3, 3, 3]
    Q = [1, 2, 3, 2, 3, 3]
    zita = 1
    chain = 1

    result = bayes_kill_max_clay(currentModel, newModel, kn, u, v, s, q, Q, zita, chain)

    print(result)
