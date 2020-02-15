from __future__ import division 
import numpy as np
from allfrank import allfrank
from allclayton import allclayton
from allgumbel import allgumbel
from bayes_birth_only_clay import *
from pandas import read_excel

def bayes_birth_clay(currentModel, newModel, kn, u, v, s, q, Q, zita, chain):

    current = np.sort(currentModel)
    new = np.sort(newModel)


    current = current.astype(int)
    new = new.astype(int)
    # Find index of last occurrence of 0 #
    j2 = np.count_nonzero(new == 0, axis=0)
    t2 = new[new != 0]
    min_new = int(np.min(t2))
    max_new = int(np.max(t2))
    L = len(u)
    l = len(current)

    ss = -1

    if j2 == 0:
        R = 4.0/3
    else:
        R = 1

    if np.any(current):
        t1 = current[current != 0]
        min_old = int(np.min(t1))
        max_old = int(np.max(t1))
        if min_new < min_old:
            if(s[1] == 1 and s[2] == 1):
                result1 = allclayton(u[:min_new], v[:min_new])
                result2 = allclayton(u[min_new:min_old], v[min_new:min_old])
                R = R * 3
            else:
                if(s[1] == 1 and s[2] == 2):
                    result1 = allclayton(u[:min_new], v[:min_new])
                    result2 = allfrank(u[min_new:min_old], v[min_new:min_old])
                    R = R * 3.0/2
                else:
                    if(s[1] == 2 and s[2] == 1):
                        result1 = allfrank(u[:min_new], v[:min_new])
                        result2 = allclayton(u[min_new:min_old], v[min_new:min_old])
                        R = R * 3.0/2
                    else:
                        if(s[1] == 1 and s[2] == 3):
                            result1 = allclayton(u[:min_new], v[:min_new])
                            result2 = allgumbel(u[min_new:min_old], v[min_new:min_old])
                            R = R * 3.0/2
                        else:
                            if(s[1] == 3 and s[2] == 1):
                                result1 = allgumbel(u[:min_new], v[:min_new])
                                result2 = allclayton(u[min_new:min_old], v[min_new:min_old])
                                R = R * 3.0/2

            resultOld = allclayton(u[:min_old], v[:min_old])

            BFu = result1["BFu"] + result2["BFu"] - resultOld["BFu"]
            if BFu.imag:
                ss = -2
                print("Error\n")

            U2 = np.random.uniform(low=np.nextafter(0.0, 1.0))

            if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and not BFu.imag:
                new_model = new
                rejected = current
                QQ = Q
                w = 29
            else:
                new_model = current
                rejected = new
                QQ = q
                w = 30

        else:
            if max_new > max_old and max_old != 0:
                if(s[1] == 1 and s[2] == 1):
                    result1 = allclayton(u[max_old - 1:max_new], v[max_old - 1:max_new])
                    result2 = allclayton(u[max_new:L], v[max_new:L])
                    R = R * 3
                else:
                    if(s[1] == 1 and s[2] == 2):
                        result1 = allclayton(u[max_old - 1:max_new], v[max_old - 1:max_new])
                        result2 = allfrank(u[max_new:L], v[max_new:L])
                        R = R * 3.0/2
                    else:
                        if(s[1] == 2 and s[2] == 1):
                            result1 = allfrank(u[max_old - 1:max_new], v[max_old - 1:max_new])
                            result2 = allclayton(u[max_new:L], v[max_new:L])
                            R = R * 3.0/2
                        else:
                            if(s[1] == 1 and s[2] == 3):
                                result1 = allclayton(u[max_old - 1:max_new], v[max_old - 1:max_new])
                                result2 = allgumbel(u[max_new:L], v[max_new:L])
                                R = R * 3.0/2
                            else:
                                if(s[1] == 3 and s[2] == 1):
                                    result1 = allgumbel(u[max_old:max_new], v[max_old:max_new])
                                    result2 = allclayton(u[max_new:L], v[max_new:L])
                                    R = R * 3.0/2

                resultOld = allclayton(u[max_old - 1:L], v[max_old - 1:L])

                BFu = result1["BFu"] + result2["BFu"] - resultOld["BFu"]

                if BFu.imag:
                    ss = -2
                    print("Error\n")

                U2 = np.random.uniform(low=np.nextafter(0.0, 1.0))

                if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and not BFu.imag:
                    new_model = new
                    rejected = current
                    QQ = Q
                    w = 31
                else:
                    new_model = current
                    rejected = new
                    QQ = q
                    w = 32

            else:
                place = np.where(new == kn)[0][0] + 1
               
                place = int(place)

                if(s[1] == 1 and s[2] == 1):
                    result1 = allclayton(u[new[place - 2]:new[place - 1] + 1], v[new[place - 2]:new[place - 1] + 1])
                    result2 = allclayton(u[new[place - 1]:new[place] + 1], v[new[place - 1]:new[place] + 1])
                    R = R * 3
                else:
                    if(s[1] == 1 and s[2] == 2):
                        result1 = allclayton(u[new[place - 2]:new[place - 1] + 1], v[new[place - 2]:new[place - 1] + 1])
                        result2 = allfrank(u[new[place - 1]:new[place] + 1], v[new[place - 1]:new[place] + 1])
                        R = R * 3.0/2
                    else:
                        if(s[1] == 2 and s[2] == 1):
                            result1 = allfrank(u[new[place - 2]:new[place - 1] + 1], v[new[place - 2]:new[place - 1] + 1])
                            result2 = allclayton(u[new[place - 1]:new[place] + 1], v[new[place - 1]:new[place] + 1])
                            R = R * 3.0/2
                        else:
                            if(s[1] == 1 and s[2] == 3):
                                result1 = allclayton(u[new[place - 2]:new[place - 1] + 1], v[new[place - 2]:new[place - 1] + 1])
                                result2 = allgumbel(u[new[place - 1]:new[place] + 1], v[new[place - 1]:new[place] + 1])
                                R = R * 3.0/2
                            else:
                                if(s[1] == 3 and s[2] == 1):
                                    result1 = allgumbel(u[new[place - 2]:new[place - 1] + 1], v[new[place - 2]:new[place - 1] + 1])
                                    result2 = allclayton(u[new[place - 1]:new[place] + 1], v[new[place - 1]:new[place] + 1])
                                    R = R * 3.0/2

                resultOld = allclayton(u[new[place - 2]:new[place] + 1], v[new[place - 2]:new[place] + 1])

                BFu = result1["BFu"] + result2["BFu"] - resultOld["BFu"]
                if BFu.imag:
                    ss = -2
                    print("Error\n")
                
                U2 = np.random.uniform(low=np.nextafter(0.0, 1.0))
                if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and not BFu.imag:
                    new_model = new
                    rejected = current
                    QQ = Q
                    w = 33
                else:
                    new_model = current
                    rejected = new
                    QQ = q
                    w = 34

        result = {"new_model": new_model, "rejected": rejected, "w": w, "QQ": QQ, "ss": ss}

    else:
        result = bayes_birth_only_frank(currentModel, newModel, kn, u, v, s, q, Q, zita, chain)


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
    kn = 137
    s = [2, 1, 3]
    q = [1, 2, 2, 3, 3, 3]
    Q = [ 1, 2, 3, 2, 3, 3]
    zita = 1
    chain = 1

    currentModel = np.zeros(numbrk, dtype=int)
    currentModel[2] = 100
    currentModel[3] = 180
    currentModel[4] = 250

    newModel = np.zeros(numbrk, dtype=int)
    newModel[1] = 101
    newModel[2] = 137
    newModel[3] = 180
    newModel[4] = 250

    result = bayes_birth_clay(currentModel, newModel, kn, u, v, s, q, Q, zita, chain)

    print(result)
