from __future__ import division 
import numpy as np
from allclayton import allclayton
from allgumbel import allgumbel
from allfrank import allfrank
from pandas import read_excel
from bayes_birth_gumbel import *

def bayes_birth_only_gumbel(currentModel, newModel, kn, u, v, s, q, Q, zita, chain):

    current = np.sort(currentModel)
    new = np.sort(newModel)

    t2 = new[new != 0]
    min_new = np.min(t2)
    max_new = np.max(t2)
    L = len(u)
    l = len(current)

    ss = -1
    R = 1/2

    if not np.any(current):

        if(s[1] == 3 and s[2] == 3):
            result1 = allgumbel(u[:max_new], v[:max_new])
            result2 = allgumbel(u[max_new:L], v[max_new:L])
            R = R * 3
        else:
            if(s[1] == 1 and s[2] == 3):
                result1 = allclayton(u[:max_new], v[:max_new])
                result2 = allgumbel(u[max_new:L], v[max_new:L])
                R = R * 3/2
            else:
                if(s[1] == 3 and s[2] == 1):
                    result1 = allgumbel(u[:max_new], v[:max_new])
                    result2 = allclayton(u[max_new:L], v[max_new:L])
                    R = R * 3/2
                else:
                    if(s[1] == 2 and s[2] == 3):
                        result1 = allfrank(u[:max_new], v[:max_new])
                        result2 = allgumbel(u[max_new:L], v[max_new:L])
                        R = R * 3/2
                    else:
                        if(s[1] == 3 and s[2] == 2):
                            result1 = allgumbel(u[:max_new], v[:max_new])
                            result2 = allfrank(u[max_new:L], v[max_new:L])
                            R = R * 3/2

        resultOld = allgumbel(u, v)

        BFu = result1["BFu"] + result2["BFu"] - resultOld["BFu"]
        
        if BFu.imag:
            ss = -2

        U2 = np.random.uniform(low=np.nextafter(0.0, 1.0))
        if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and not BFu.imag:
            new_model = new
            rejected = current
            QQ = Q
            w = 35
        else:
            new_model = current
            rejected = new
            QQ = q
            w = 36

        result = {"new_model": new_model, "rejected": rejected, "w": w, "QQ": QQ, "ss": ss}
    else:
        result =  bayes_birth_gumbel(currentModel, newModel, kn, u, v, s, q, Q, zita, chain)

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
    s = [2, 3, 2]
    q = [1, 2, 2, 3, 3, 3]
    Q = [ 1, 2, 3, 2, 3, 3]
    zita = 1
    chain = 1

    currentModel = np.zeros(numbrk, dtype=int)

    newModel = np.zeros(numbrk, dtype=int)
    newModel[1] = 99
    newModel[2] = 137
    newModel[3] = 180
    newModel[4] = 250

    result = bayes_birth_only_gumbel(currentModel, newModel, kn, u, v, s, q, Q, zita, chain)

    print(result)
