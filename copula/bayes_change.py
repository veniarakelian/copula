import numpy as np
from allfrank import allfrank
from allclayton import allclayton
from allgumbel import allgumbel

def bayes_change(currentModel, u, v, q, numbrk, zita, chain):

    current = np.sort(currentModel)
    l = len(currentModel)
    L = len(u)

    R = 1/3
    ss = -1
    q_new = 0

    if np.any(current != np.zeros(shape=(l,1))):

        temp = current[current != 0]
        z = temp.shape[0]

        p = np.random.uniform(low=1, high=z+1)

        if p > 1 and p <= z:
            lower = temp[p - 2][0]
            upper = temp[p - 1][0]
            if q[p - 1][0] == 1:
                a = np.random.uniform()

                if a <= 1/2:

                    result1 = allclayton(u[lower:upper], v[lower:upper])
                    result2 = allfrank(u[lower:upper], v[lower:upper])
                    q_new = 2
                else:

                    result1 = allclayton(u[lower:upper], v[lower:upper])
                    result2 = allgumbel(u[lower:upper], v[lower:upper])
                    q_new = 3
            else:
                if q[p - 1][0] == 2:
                    a = np.random.uniform()

                    if a <= 1/2:

                        result1 = allfrank(u[lower:upper], v[lower:upper])
                        result2 = allclayton(u[lower:upper], v[lower:upper])
                        q_new = 1
                    else:

                        result1 = allfrank(u[lower:upper], v[lower:upper])
                        result2 = allgumbel(u[lower:upper], v[lower:upper])
                        q_new = 3
                else:

                    a = np.random.uniform()

                    if a <= 1/2:

                        result1 = allgumbel(u[lower:upper], v[lower:upper])
                        result2 = allfrank(u[lower:upper], v[lower:upper])
                        q_new = 2
                    else:

                        result1 = allgumbel(u[lower:upper], v[lower:upper])
                        result2 = allclayton(u[lower:upper], v[lower:upper])
                        q_new = 1

            BFu = result2["BFu"] - result1["BFu"]

            if BFu.imag:
                ss = -2
                print("Error\n")

            U2 = np.random.uniform()

            if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and BFu.imag == 0:
                new_model = new
                q[p - 1][0] = q_new
                QQ = Q
                rejected = current
                w = 37
            else:
                new_model = current
                QQ = q
                rejected = current
                w = 38
        else:
            if p > z and p != 1:
                if q[p - 1][0] == 1:
                    a = np.random.uniform()

                    if a <= 1/2:

                        result1 = allclayton(u[np.max(temp):L], v[np.max(temp):L])
                        result2 = allfrank(u[np.max(temp):L], v[np.max(temp):L])
                        q_new = 2
                        j = 0
                    else:

                        result1 = allclayton(u[np.max(temp):L], v[np.max(temp):L])
                        result2 = allgumbel(u[np.max(temp):L], v[np.max(temp):L])
                        q_new = 3
                        j = 1
                else:
                    if q[p - 1] == 2:
                        a = np.random.uniform()

                        if a <= 1/2:

                            result1 = allfrank(u[np.max(temp):L], v[np.max(temp):L])
                            result2 = allclayton(u[np.max(temp):L], v[np.max(temp):L])
                            q_new = 1
                            j = 3
                        else:

                            result1 = allfrank(u[np.max(temp):L], v[np.max(temp):L])
                            result2 = allgumbel(u[np.max(temp):L], v[np.max(temp):L])
                            q_new = 3
                            j = 4
                    else:

                        a = np.random.uniform()

                        if a <= 1/2:

                            result1 = allgumbel(u[np.max(temp):L], v[np.max(temp):L])
                            result2 = allclayton(u[np.max(temp):L], v[np.max(temp):L])
                            q_new = 1
                            j = 5
                        else:

                            result1 = allgumbel(u[np.max(temp):L], v[np.max(temp):L])
                            result2 = allfrank(u[np.max(temp):L], v[np.max(temp):L])
                            q_new = 2
                            j = 6

                BFu = result2["BFu"] - result1["BFu"]

                if BFu.imag:
                    ss = -2
                    print("Error\n")

                U2 = np.random.uniform()

                if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and BFu.imag == 0:
                    new_model = current # correct ??? 
                    q[p - 1][0] = q_new
                    QQ = Q
                    j = 7
                    QQ[p - 1:numbrk + 1][0] = q_new
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
                    if q[p - 1][0] == 1:
                        a = np.random.uniform()

                        if a <= 1/2:

                            result1 = allclayton(u[:np.min(temp)], v[:np.min(temp)])
                            result2 = allfrank(u[:np.min(temp)], v[:np.min(temp)])
                            q_new = 2
                        else:

                            result1 = allclayton(u[:np.min(temp)], v[:np.min(temp)])
                            result2 = allgumbel(u[:np.min(temp)], v[:np.min(temp)])
                            q_new = 3
                    else:
                        if q[p - 1][0] == 2:
                            a = np.random.uniform()

                            if a <= 1/2:

                                result1 = allfrank(u[:np.min(temp)], v[:np.min(temp)])
                                result2 = allclayton(u[:np.min(temp)], v[:np.min(temp)])
                                q_new = 1
                            else:

                                result1 = allfrank(u[:np.min(temp)], v[:np.min(temp)])
                                result2 = allgumbel(u[:np.min(temp)], v[:np.min(temp)])
                                q_new = 3
                        else:

                            a = np.random.uniform()

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
                        print("Error\n")

                    U2 = np.random.uniform()

                    if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and BFu.imag == 0:
                        new_model = current # correct ??? 
                        q[p - 1][0] = q_new
                        QQ = Q
                        QQ[p - 1:numbrk + 1][0] = q_new
                        rejected = current
                        w = 61
                    else:
                        new_model = current
                        QQ = q
                        rejected = current
                        w = 62

    else:
        if np.any(current == np.zeros(shape=(l, 1))):

            if q == 2 * np.ones(shape=(numbrk+1, 1)):
                a = np.random.uniform()

                if a <= 1/2:

                    result1 = allfrank(u[:L], v[:L])
                    result2 = allclayton(u[:L], v[:L])
                    q_new = 1
                else:

                    result1 = allfrank(u[:L], v[:L])
                    result2 = allgumbel(u[:L], v[:L])
                    q_new = 3
            else:
                if q == np.ones(shape=(numbrk+1, 1)):
                    a = np.random.uniform()

                    if a <= 1/2:

                        result1 = allclayton(u[:L], v[:L])
                        result2 = allfrank(u[:L], v[:L])
                        q_new = 2
                    else:

                        result1 = allclayton(u[:L], v[:L])
                        result2 = allgumbel(u[:L], v[:L])
                        q_new = 3
                else:
                    if q == 3 * np.ones(shape=(numbrk + 1, 1)):
                        a = np.random.uniform()

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
                print("Error\n")

            U2 = np.random.uniform()

            if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and BFu.imag == 0:
                new_model = current
                QQ = q_new * np.ones(shape=(numbrk+1, 1))
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

    u = np.array([

[0.939001561999887],
[0.875942811492984],
[0.550156342898422],
[0.622475086001228],
[0.587044704531417],
[0.207742292733028],
[0.301246330279491],
[0.470923348517591],
[0.230488160211559],
[0.844308792695389],
[0.194764289567049],
[0.225921780972399],
[0.170708047147859],
[0.227664297816554],
[0.435698684103899],
[0.311102286650413],
[0.923379642103244],
[0.430207391329584],
[0.184816320124136],
[0.904880968679893],
[0.979748378356085],
[0.438869973126103],
[0.111119223440599],
[0.258064695912067],
[0.408719846112552],
[0.594896074008614],
[0.262211747780845],
[0.602843089382083],
[0.711215780433683],
[0.22174673401724],
[0.117417650855806],
[0.296675873218327],
[0.318778301925882],
[0.424166759713807],
[0.507858284661118],
[0.085515797090044],
[0.262482234698333],
[0.801014622769739],
[0.029220277562146],
[0.928854139478045],
[0.730330862855453],
[0.488608973803579],
[0.578525061023439],
[0.237283579771521],
[0.458848828179931],
[0.963088539286913],
[0.546805718738968],
[0.521135830804002],
[0.231594386708524],
[0.488897743920167],
[0.096730025780867],
[0.818148553859625],
[0.817547092079286],
[0.722439592366842],
[0.149865442477967],
[0.659605252908307],
[0.518594942510538],
[0.972974554763863],
[0.648991492712356],
[0.800330575352402],
[0.45379770872692],
[0.432391503783462],
[0.825313795402046],
[0.083469814858914],
[0.133171007607162],
[0.173388613119006],
[0.390937802323736],
[0.83137974283907],
[0.80336439160244],
[0.060471179169894],
[0.399257770613576],
[0.526875830508296],
[0.416799467930787],
[0.656859890973707],
[0.627973359190104],
[0.291984079961715],
[0.43165117024872],
[0.015487125636019],
[0.984063724379154],
[0.167168409914656],
[0.106216344928664],
[0.372409740055537],
[0.198118402542975],
[0.489687638016024],
[0.339493413390758],
[0.951630464777727],
[0.920332039836564],
[0.052676997680793],
[0.737858095516997],
[0.269119426398556],
[0.422835615008808],
[0.547870901214845],
[0.942736984276934],
[0.417744104316662],
[0.983052466469856],
[0.301454948712065],
[0.701098755900926],
[0.666338851584426],
[0.539126465042857],
[0.698105520180308]
		])

    v = np.array([
[0.881634747461781],
[0.875083491128449],
[0.470601262589077],
[0.511729768801112],
[0.981814584401157],
[0.020869701490377],
[0.673290821503241],
[0.831962512146175],
[0.50255378015766],
[0.417323586796571],
[0.1312204595217],
[0.186014176516629],
[0.35118445134462],
[0.079582483421391],
[0.605733218514507],
[0.088973692406118],
[0.886074563050531],
[0.437046918860753],
[0.446552486110628],
[0.901774073469152],
[0.977870292136281],
[0.781343735855176],
[0.124519489969423],
[0.437706337006055],
[0.210617238833567],
[0.095261881994641],
[0.479362000567652],
[0.586714938790528],
[0.661833243248063],
[0.643300748256224],
[0.263868773867285],
[0.409515279570243],
[0.650514214230458],
[0.672235499825223],
[0.558977697679896],
[0.058566698020156],
[0.153625348773801],
[0.941005332387949],
[0.006672760647188],
[0.819852705344735],
[0.424227788110981],
[0.950860309304659],
[0.711937357105535],
[0.286487307601931],
[0.445581905572976],
[0.425208926518375],
[0.665175012943978],
[0.093193031185598],
[0.043488411550548],
[0.505283376069361],
[0.227507184963531],
[0.593426348429212],
[0.540873408987996],
[0.999086065787499],
[0.066117329025187],
[0.211566156517565],
[0.550523634625491],
[0.978589816775968],
[0.727543707962895],
[0.587737892692329],
[0.385138772258907],
[0.415508879634916],
[0.991208258165947],
[0.040971227900854],
[0.394504747587202],
[0.279408414897329],
[0.332103858161619],
[0.61688015474686],
[0.738024912583282],
[0.126126084381919],
[0.16781277088838],
[0.573758979379632],
[0.264631479379266],
[0.584139031179045],
[0.663034508484721],
[0.182587923335308],
[0.319021632013476],
[0.146656581292667],
[0.798957350900928],
[0.395253920095318],
[0.669444819290769],
[0.513817119258438],
[0.161242420140439],
[0.53592463777763],
[0.118846356380195],
[0.980671028364942],
[0.969421352984688],
[0.286775874548503],
[0.583445951357467],
[0.336542169020619],
[0.052468472966531],
[0.504555738562826],
[0.792671475455361],
[0.217100570981851],
[0.74065670039209],
[0.278119070042033],
[0.385786077908424],
[0.705036478103668],
[0.521169366233904],
[0.781987318512413]
		])

    currentModel = np.array([[0], [0], [0], [0], [50]])
    q = np.array([[0], [0], [0], [0], [50]])
    zita = 5
    chain = 6
    numbrk = 1

    result = bayes_change(currentModel, u, v, q, numbrk, zita, chain)

    print(result)
