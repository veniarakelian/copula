import numpy as np
from allclayton import allclayton
from allgumbel import allgumbel
from pandas import read_excel
from allfrank import allfrank

def bayes_birth_only_frank(currentModel, newModel, kn, u, v, s, q, Q, zita, chain):

    current = np.sort(currentModel)
    new = np.sort(newModel)

    t2 = new[new != 0]
    min_new = np.min(t2)
    max_new = np.max(t2)
    L = len(u)
    l = len(current)

    ss = -1
    R = 1/2

    if not np.all(current):

        if(s[1] == 2 and s[2] == 2):
            result1 = allfrank(u[:max_new], v[:max_new])
            result2 = allfrank(u[max_new:L], v[max_new:L])
            R = R * 3
        else:
            if(s[1] == 1 and s[2] == 2):
                result1 = allclayton(u[:max_new], v[:max_new])
                result2 = allfrank(u[max_new:L], v[max_new:L])
                R = R * 3/2
            else:
                if(s[1] == 2 and s[2] == 1):
                    result1 = allfrank(u[:max_new], v[:max_new])
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

        result = {"new_model": new_model, "rejected": rejected, "w": w, "QQ": QQ, "ss": ss}
    else:
        result =  bayes_birth_frank(currentModel, newModel, kn, u, v, s, q, Q, zita, chain)

    return result

# Test #
if __name__ == "__main__":

    df = read_excel("/home/petropoulakis/Desktop/xy.xlsx", sheet_name='Sheet1', header=None)

    u = []
    v = []

    for index, row in df.iterrows():
        u.append([row[0]])
        v.append([row[1]])

    u = np.asarray(u, dtype=np.float32)
    v = np.asarray(v, dtype=np.float32)

    chain = 1
    numbrk = 5

    currentModel = np.zeros(numbrk)
    currentModel[numbrk - 1] = 50

    newModel = np.array([[0], [0], [0], [0], [45]])
    kn =
    s = [1, 2, 3, 4]
    q =
    Q = 6
    zita = 0.8

    result = bayes_birth_only_frank(currentModel, newModel, kn, u, v, s, q, Q, zita, chain)

    print(result)
