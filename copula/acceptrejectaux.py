import numpy as np
from bayesfactor import bayesfactor

def acceptrejectaux(currentModel1, currentModel2, QQ1, QQ2, x, y, chain, zita):

    brks1 = currentModel1[currentModel1 != 0]
    brks2 = currentModel2[currentModel2 != 0]
    brks1 = brks1.astype(int)
    brks2 = brks2.astype(int)

    BFu1 = 0
    BFu2 = 0
    proposal1 = 0
    proposal2 = 0

    if brks1.shape[0] !=  0:
        for i in range(len(brks1) - 1):
            temp1 = bayesfactor(x[currentModel1[brks1[i]] - 1:currentModel1[brks1[i+1]]], y[currentModel1[brks1[i]]:currentModel1[brks1[i+1]]], QQ1[i])
            BFu1 = BFu1 + temp1

        BFu1 = BFu1 + bayesfactor(x[:currentModel1[brks1[0]]], y[:currentModel1[brks1[0]]], QQ1[0]) + bayesfactor(x[currentModel1[brks1[-1]] - 1:len(x)], y[currentModel1[brks1[-1]] - 1:len(y)], QQ1[-1])
    else:
        BFu1 = bayesfactor(x, y, QQ1[0])

    if brks2.shape[0] !=  0:
        for i in range(len(brks2) - 1):
            temp2 = bayesfactor(x[currentModel2[brks2[i]] - 1:currentModel2[brks2[i+1]]], y[currentModel2[brks2[i]]:currentModel2[brks2[i+1]]], QQ2[i])
            BFu2 = BFu2 + temp2

        BFu2 = BFu1 + bayesfactor(x[:currentModel2[brks2[0]]], y[:currentModel2[brks2[0]]], QQ2[0]) + bayesfactor(x[currentModel2[brks2[-1]] - 1:len(x)], y[currentModel2[brks2[-1]] - 1:len(y)], QQ2[-1])
    else:
        BFu2 = bayesfactor(x, y, QQ2[0])

    u = np.random.uniform(low=np.nextafter(0.0, 1.0))

    if np.log(u) < min(0, (1 - zita**(chain-1))*(BFu2-BFu1)):
       currentModel = currentModel2
       QQ = QQ2
       accept = 1
    else:
       currentModel = currentModel1
       QQ = QQ1
       accept = 0

    result = {"currentModel": currentModel, "QQ": QQ, "accept": accept}

    return result
