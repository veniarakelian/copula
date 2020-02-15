from __future__ import division 
import numpy as np
from allfrank import allfrank
from allclayton import allclayton
from allgumbel import allgumbel
from pandas import read_excel

def bayes_change(currentModel, u, v, q, numbrk, zita, chain):

    current = np.sort(currentModel)
    l = len(currentModel)
    L = len(u)

    R = 1/3
    ss = -1
    q_new = 0
    
    if np.count_nonzero(current) != 0:

        temp = current[current != 0]
        z = temp.shape[0]
        p = np.random.randint(low=1, high=z+2)
        
        if p > 1 and p <= z:
            lower = temp[p - 2]
            upper = temp[p - 1]

            if q[p - 1] == 1:
                a = np.random.uniform(low=np.nextafter(0.0, 1.0))

                if a <= 1/2:

                    result1 = allclayton(u[lower - 1:upper], v[lower - 1:upper])
                    result2 = allfrank(u[lower - 1:upper], v[lower - 1:upper])
                    q_new = 2
                else:

                    result1 = allclayton(u[lower - 1:upper], v[lower - 1:upper])
                    result2 = allgumbel(u[lower - 1:upper], v[lower - 1:upper])
                    q_new = 3
            else:
                if q[p - 1] == 2:
                    a = np.random.uniform(low=np.nextafter(0.0, 1.0))

                    if a <= 1/2:

                        result1 = allfrank(u[lower - 1:upper], v[lower - 1:upper])
                        result2 = allclayton(u[lower - 1:upper], v[lower - 1:upper])
                        q_new = 1
                    else:

                        result1 = allfrank(u[lower - 1:upper], v[lower - 1:upper])
                        result2 = allgumbel(u[lower - 1:upper], v[lower - 1:upper])
                        q_new = 3
                else:

                    a = np.random.uniform(low=np.nextafter(0.0, 1.0))

                    if a <= 1/2:

                        result1 = allgumbel(u[lower - 1:upper], v[lower - 1:upper])
                        result2 = allfrank(u[lower - 1:upper], v[lower - 1:upper])
                        q_new = 2
                    else:

                        result1 = allgumbel(u[lower - 1:upper], v[lower - 1:upper])
                        result2 = allclayton(u[lower - 1:upper], v[lower - 1:upper])
                        q_new = 1

            BFu = result2["BFu"] - result1["BFu"]

            if BFu.imag:
                ss = -2

            U2 = np.random.uniform(low=np.nextafter(0.0, 1.0))

            if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and not BFu.imag:
                new_model = current
                q[p - 1] = q_new
                QQ = q
                rejected = current
                w = 37
            else:
                new_model = current
                QQ = q
                rejected = current
                w = 38
        else:
            if p > z and p != 1:
                if q[p - 1] == 1:
                    a = np.random.uniform(low=np.nextafter(0.0, 1.0))

                    if a <= 1/2:

                        result1 = allclayton(u[np.max(temp) - 1:L], v[np.max(temp) - 1:L])
                        result2 = allfrank(u[np.max(temp) - 1:L], v[np.max(temp) - 1:L])
                        q_new = 2
                        j = 0
                    else:

                        result1 = allclayton(u[np.max(temp) - 1:L], v[np.max(temp) - 1:L])
                        result2 = allgumbel(u[np.max(temp) - 1:L], v[np.max(temp) - 1:L])
                        q_new = 3
                        j = 1
                else:
                    if q[p - 1] == 2:
                        a = np.random.uniform(low=np.nextafter(0.0, 1.0))

                        if a <= 1/2:

                            result1 = allfrank(u[np.max(temp) - 1:L], v[np.max(temp) - 1:L])
                            result2 = allclayton(u[np.max(temp) - 1:L], v[np.max(temp) - 1:L])
                            q_new = 1
                            j = 3
                        else:

                            result1 = allfrank(u[np.max(temp) - 1:L], v[np.max(temp) - 1:L])
                            result2 = allgumbel(u[np.max(temp) - 1:L], v[np.max(temp) - 1:L])
                            q_new = 3
                            j = 4
                    else:

                        a = np.random.uniform(low=np.nextafter(0.0, 1.0))

                        if a <= 1/2:

                            result1 = allgumbel(u[np.max(temp) - 1:L], v[np.max(temp) - 1:L])
                            result2 = allclayton(u[np.max(temp) - 1:L], v[np.max(temp) - 1:L])
                            q_new = 1
                            j = 5
                        else:

                            result1 = allgumbel(u[np.max(temp) - 1:L], v[np.max(temp) - 1:L])
                            result2 = allfrank(u[np.max(temp) - 1:L], v[np.max(temp) - 1:L])
                            q_new = 2
                            j = 6

                BFu = result2["BFu"] - result1["BFu"]

                if BFu.imag:
                    ss = -2

                U2 = np.random.uniform(low=np.nextafter(0.0, 1.0))

                if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and not BFu.imag:
                    new_model = current
                    q[p - 1] = q_new
                    QQ = q
                    j = 7
                    QQ[p - 1:numbrk + 1] = q_new * np.ones(numbrk + 1 - (p - 1), dtype=int)
                    rejected = current
                    w = 41
                else:
                    new_model = current
                    QQ = q
                    j = 8
                    rejected = current
                    w = 42
            else:

                if p == 1:
                    if q[p - 1] == 1:
                        a = np.random.uniform(low=np.nextafter(0.0, 1.0))
                        if a <= 1/2:
                            
                            result1 = allclayton(u[:np.min(temp)], v[:np.min(temp)])
                            result2 = allfrank(u[:np.min(temp)], v[:np.min(temp)])
                            q_new = 2
                        else:

                            result1 = allclayton(u[:np.min(temp)], v[:np.min(temp)])
                            result2 = allgumbel(u[:np.min(temp)], v[:np.min(temp)])
                            q_new = 3
                    else:
                        if q[p - 1] == 2:
                            a = np.random.uniform(low=np.nextafter(0.0, 1.0))

                            if a <= 1/2:

                                result1 = allfrank(u[:np.min(temp)], v[:np.min(temp)])
                                result2 = allclayton(u[:np.min(temp)], v[:np.min(temp)])
                                q_new = 1
                            else:

                                result1 = allfrank(u[:np.min(temp)], v[:np.min(temp)])
                                result2 = allgumbel(u[:np.min(temp)], v[:np.min(temp)])
                                q_new = 3
                        else:

                            a = np.random.uniform(low=np.nextafter(0.0, 1.0))

                            if a <= 1/2:

                                result1 = allgumbel(u[:np.min(temp)], v[:np.min(temp)])
                                result2 = allclayton(u[:np.min(temp)], v[:np.min(temp)])
                                q_new = 1
                            else:

                                result1 = allgumbel(u[:np.min(temp)], v[:np.min(temp)])
                                result2 = allfrank(u[:np.min(temp)], v[:np.min(temp)])
                                q_new = 2

                    BFu = result2["BFu"] - result1["BFu"]

                    if BFu.imag:
                        ss = -2

                    U2 = np.random.uniform(low=np.nextafter(0.0, 1.0))

                    if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and not BFu.imag:
                        new_model = current 
                        q[p - 1] = q_new
                        QQ = q
                        QQ[p - 1:numbrk + 1] = q_new * np.ones(numbrk + 1 - (p - 1), dtype=int)
                        rejected = current
                        w = 61
                    else:
                        new_model = current
                        QQ = q
                        rejected = current
                        w = 62

    else:
        if np.count_nonzero(current == 0) != 0:

            if (q == 2 * np.ones(numbrk+1)).all():
                a = np.random.uniform(low=np.nextafter(0.0, 1.0))

                if a <= 1/2:

                    result1 = allfrank(u[:L], v[:L])
                    result2 = allclayton(u[:L], v[:L])
                    q_new = 1
                else:

                    result1 = allfrank(u[:L], v[:L])
                    result2 = allgumbel(u[:L], v[:L])
                    q_new = 3
            else:
                if (q == np.ones(numbrk+1)).all():
                    a = np.random.uniform(low=np.nextafter(0.0, 1.0))

                    if a <= 1/2:

                        result1 = allclayton(u[:L], v[:L])
                        result2 = allfrank(u[:L], v[:L])
                        q_new = 2
                    else:

                        result1 = allclayton(u[:L], v[:L])
                        result2 = allgumbel(u[:L], v[:L])
                        q_new = 3
                else:
                    if (q == 3 * np.ones(numbrk+1)).all():
                        a = np.random.uniform(low=np.nextafter(0.0, 1.0))

                        if a <= 1/2:

                            result1 = allgumbel(u[:L], v[:L])
                            result2 = allfrank(u[:L], v[:L])
                            q_new = 2
                        else:

                            result1 = allgumbel(u[:L], v[:L])
                            result2 = allclayton(u[:L], v[:L])
                            q_new = 1

            BFu = result2["BFu"] - result1["BFu"]

            if BFu.imag:
                ss = -2

            U2 = np.random.uniform(low=np.nextafter(0.0, 1.0))

            if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and not BFu.imag:
                new_model = current
                QQ = q_new * np.ones(numbrk+1, dtype=int)
                rejected = current
                w = 49
            else:
                new_model = current
                QQ = q
                rejected = current
                w = 50
    
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
    q = [2, 2, 2, 2, 2, 2]
    zita = 1
    chain = 1

    currentModel = np.zeros(numbrk, dtype=int)
    currentModel[4] = 250
    currentModel[3] = 100

    result = bayes_change(currentModel, u, v, q, numbrk, zita, chain)

    print(result)
