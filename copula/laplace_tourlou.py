from __future__ import division
import numpy as np
from bayes_change import bayes_change
from birth import birth
from bayes_birth_frank import bayes_birth_frank
from bayes_birth_gumbel import bayes_birth_gumbel
from bayes_birth_clay import bayes_birth_clay
from bayes_birth_only_frank import bayes_birth_only_frank
from bayes_birth_only_gumbel import bayes_birth_only_gumbel
from bayes_birth_only_clay import bayes_birth_only_clay
from kill import kill
from bayes_kill_frank import bayes_kill_frank
from bayes_kill_gumbel import bayes_kill_gumbel
from bayes_kill_clay import bayes_kill_clay
from move_lapl import move_lapl
from bayes_move_clay import bayes_move_clay
from bayes_move_frank import bayes_move_frank
from bayes_move_gumbel import bayes_move_gumbel
from pandas import read_excel

def laplace_tourlou(currentModel, u, v, numbrk, dist, q, zita, chain):
    
    LENGTH = len(currentModel)
    j = np.count_nonzero(currentModel == 0, axis=0)
    
    new_model = np.zeros(numbrk,dtype=int)
    rejected = new_model
    w = 1
    QQ = np.zeros(numbrk + 1,dtype=int)
    ss = 1
    
    if LENGTH == numbrk and (0 < j) and (j < numbrk):

        l = len(currentModel) - j
        p1 = 1/4
        p2 = 2/4
        p3 = 3/4

        P = np.random.uniform(low=np.nextafter(0.0, 1.0))

        if P <= p1:
            result = birth(currentModel, u, dist, numbrk, q)

            if result["z"] == 1:
                if result["s"][0] == 1:
                    result = bayes_birth_clay(currentModel, result["bir"], result["kn"], u, v, result["s"], result["q"], result["Q"], zita, chain)
                else:
                    if result["s"][0] == 2:
                        result = bayes_birth_frank(currentModel, result["bir"], result["kn"], u, v, result["s"], result["q"], result["Q"], zita, chain)
                    else:
                        if result["s"][0] == 3:
                            result = bayes_birth_gumbel(currentModel, result["bir"], result["kn"], u, v, result["s"], result["q"], result["Q"], zita, chain)
                new_model = result["new_model"]
                rejected = result["rejected"]
                QQ = result["QQ"]
                w = result["w"]
                ss = result["ss"]
            else:
                new_model = np.sort(currentModel)
                rejected = np.sort(currentModel)
                QQ = q
                w = result["z"]
                ss = -3

            w = 0.1
        else:

            if P > p1 and P <= p2:
                result = kill(currentModel, numbrk, q)

                if result["s"][2] == 1:
                    result = bayes_kill_clay(currentModel, result["newModel"], result["Kn"], u, v, result["s"], result["q"], result["Q"], zita, chain)
                else:
                    if result["s"][2] == 2:
                        result = bayes_kill_frank(currentModel, result["newModel"], result["Kn"], u, v, result["s"], result["q"], result["Q"], zita, chain)
                    else:
                        if result["s"][2] == 3:
                            result = bayes_kill_gumbel(currentModel, result["newModel"], result["Kn"], u, v, result["s"], result["q"], result["Q"], zita, chain)

                new_model = result["new_model"]
                rejected = result["rejected"]
                QQ = result["QQ"]
                w = result["w"]
                ss = result["ss"]
                W = 0.2

            else:
                if P > p2 and P <= p3:
                    result = move_lapl(currentModel, u, v, dist, numbrk, q)
                    if result["z"] == 1:
                        if result["s"] == 1:
                            result = bayes_move_clay(currentModel, result["new_model"], result["pick"], u, v, result["Q"], zita, chain)
                        else:
                            if result["s"] == 2:
                                result = bayes_move_frank(currentModel, result["new_model"], result["pick"], u, v, result["Q"], zita, chain)
                            else:
                                if result["s"] == 3:
                                    result = bayes_move_gumbel(currentModel, result["new_model"], result["pick"], u, v, result["Q"], zita, chain)

                        new_model = result["new_model"]
                        rejected = result["rejected"]
                        QQ = result["QQ"]
                        w = result["w"]
                        ss = result["s"]
                    else:
                        new_model = np.sort(currentModel)
                        rejected = np.sort(result["new_model"])
                        QQ = q
                        w = result["z"]
                        ss = -3
                    W = 0.3
                else:
                    if P > p3:
                        
                        result = bayes_change(currentModel, u, v, q, numbrk, zita, chain)
                        new_model = result["new_model"]
                        rejected = result["rejected"]
                        QQ = result["QQ"]
                        w = result["w"]
                        ss = result["ss"]
                        W = 0.4

    else:
        if LENGTH == numbrk and j == 0:
            L = len(currentModel) - j
            p1 = 1/3
            p2 = 2/3
        
            P = np.random.uniform(low=np.nextafter(0.0, 1.0))

            if P <= p1:
                result = kill(currentModel, numbrk, q)

                if result["s"][2] == 1:
                    result = bayes_kill_clay(currentModel, result["newModel"], result["Kn"], u, v, result["s"], result["q"], result["Q"], zita, chain)
                else:
                    if result["s"][2] == 2:
                        result = bayes_kill_frank(currentModel, result["newModel"], result["Kn"], u, v, result["s"], result["q"], result["Q"], zita, chain)
                    else:
                        if result["s"][2] == 3:
                            result = bayes_kill_gumbel(currentModel, result["newModel"], result["Kn"], u, v, result["s"], result["q"], result["Q"], zita, chain)

                new_model = result["new_model"]
                rejected = result["rejected"]
                QQ = result["QQ"]
                w = result["w"]
                ss = result["ss"]

                W = 0.5

            else:
                if P > p1 and P <= p2:
                    result = move_lapl(currentModel, u, v, dist, numbrk, q)
                    if result["z"] == 1:
                        if result["s"] == 1:
                            result = bayes_move_clay(currentModel, result["new_model"], result["pick"], u, v, result["Q"], zita, chain)
                        else:
                            if result["s"] == 2:
                                result = bayes_move_frank(currentModel, result["new_model"], result["pick"], u, v, result["Q"], zita, chain)
                            else:
                                if result["s"] == 3:
                                    result = bayes_move_gumbel(currentModel, result["new_model"], result["pick"], u, v, result["Q"], zita, chain)

                        new_model = result["new_model"]
                        rejected = result["rejected"]
                        QQ = result["QQ"]
                        w = result["w"]
                        ss = result["s"]

                    else:

                        new_model = np.sort(currentModel)
                        rejected = np.sort(result["new_model"])
                        QQ = q
                        w = -5
                        ss = -3

                    W = 0.6

                else:
                    if P > p2:
                        result = bayes_change(currentModel, u, v, result["q"], numbrk, zita, chain)
                        new_model = result["new_model"]
                        rejected = result["rejected"]
                        QQ = result["QQ"]
                        w = result["w"]
                        ss = result["ss"]
                        W = 0.7

        else:
            if LENGTH == numbrk and j == numbrk:
                L = len(currentModel) - j
                p1 = 1/2
                P = np.random.uniform(low=np.nextafter(0.0, 1.0))
                
                if P <= p1:
                    result = birth(currentModel, u, dist, numbrk, q)
                    if result["z"] == 1:
                        if result["s"][0] == 1:
                            result = bayes_birth_only_clay(currentModel, result["bir"], result["kn"], u, v, result["s"], result["q"], result["Q"], zita, chain)
                        else:
                            if result["s"][0] == 2:
                                result = bayes_birth_only_frank(currentModel, result["bir"], result["kn"], u, v, result["s"], result["q"], result["Q"], zita, chain)
                            else:
                                if result["s"][0] == 3:
                                    result = bayes_birth_only_gumbel(currentModel, result["bir"], result["kn"], u, v, result["s"], result["q"], result["Q"], zita, chain)

                        new_model = result["new_model"]
                        rejected = result["rejected"]
                        QQ = result["QQ"]
                        w = result["w"]
                        ss = result["ss"]

                    else:
                        
                        new_model = np.sort(currentModel)
                        rejected = np.sort(currentModel)
                        QQ = q
                        w = result["z"]
                        ss = -3

                    W = 0.8

                else:
                    
                    result = bayes_change(currentModel, u, v, q, numbrk, zita, chain)
                    new_model = result["new_model"]
                    rejected = result["rejected"]
                    QQ = result["QQ"]
                    w = result["w"]
                    ss = result["ss"]
                    W = 0.9

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
    dist = 30
    numbrk = 5
    q = [1, 2, 2, 3, 3, 3]
    zita = 1
    chain = 1

    currentModel = np.zeros(numbrk, dtype=int)
    currentModel[0] = 100

    result = laplace_tourlou(currentModel, u, v, numbrk, dist, q, zita, chain)

    print(result)
