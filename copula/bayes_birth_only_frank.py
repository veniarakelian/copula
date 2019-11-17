import numpy as np
from allfrank import allfrank
from allclayton import allclayton

def bayes_birth_only_frank(currentModel, newModel, kn, u, v, s, q, Q, zita, chain):

    current = np.sort(currentModel)
    new = np.sort(newModel)
    # Check function no purpose ? #

    t2 = new[new != 0]
    min_new = np.argmax(t2)
    max_new = np.argmax(t2)
    L = len(u)
    l = len(current)
    #thetastart = [1.4, 0.05, 0.05]
    ss = -1
    R = 1/2

    if not np.any(0, current):

        if(s[1] == 2 and s[2] == 2):
            result1 = allfrank(u[:, max_new], v[:, max_new])
            result2 = allfrank(u[max_new + 1, L], v[max_new: L])
            R = R * 3
        else:
            if(s[1] == 1 and s[2] == 2):
                result1 = allclayton(u[:, max_new], v[:, max_new])
                result2 = allfrank(u[max_new + 1, L], v[max_new: L])
            else:
                if(s[1] == 2 and s[2] == 3):
                    result1 = allfrank(u[:, max_new], v[:, max_new])
                    result2 = allclayton(u[max_new + 1, L], v[max_new: L])
                    R = R * 3/2
                else:
                    if(s[1] == 3 and s[2] == 2):
                        result1 = allfrank(u[:, max_new], v[:, max_new])
                        #result2 = allgumbel(u[max_new + 1, L], v[max_new: L])
                        R = R * 3/2
                    else:
                        if(s[1] == 3 and s[2] == 2):
                            #result1 = allgumbel(u[:, max_new], v[:, max_new])
                            result2 = allfrank(u[max_new + 1, L], v[max_new: L])
                            R = R * 3/2

        resultOld = allfrank(u, v)

        BFu = result1["BFu"] + result2["BFu"] - resultOld["BFu"]

        if BFu.imag:
            ss = -2
            print("Error\n")

        U2 = np.random.uniform()

        if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and BFu.imag == 0:
            new_model = new
            rejected = current
            QQ = Q
            w = 37
        else:
            new_model = current
            rejected = new
            QQ = q
            w = 38

    else:
        # bayes_birth_frank
        print("")

    result = {"new_model": new_model, "rejected": rejected, "w": w, "QQ": QQ, "ss": ss}

    return result
