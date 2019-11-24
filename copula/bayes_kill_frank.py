import numpy as np
from allfrank import allfrank
from allclayton import allclayton

def bayes_kill_frank(currentModel, newModel, kn, u, v, s, q, Q, zita, chain):

    current = np.sort(currentModel)
    new = np.sort(newModel)

    t1 = new[new != 0]
    min_old = np.min(t1)
    max_old = np.max(t1)
    L = len(u)
    l = len(new)
    ss = -1

    if np.all(new):

        R = 1
        t2 = new[new != 0]
        min_new = np.min(t2)
        max_new = np.max(t2)

        if min_old < min_new:
            if(s[1] == 2 and s[2] == 2):
                result1 = allfrank(u[:min_old], v[:min_old])
                result2 = allfrank(u[min_old:min_new], v[min_old:min_new])
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
                        if(s[1] == 3 and s[2] == 2):
                            #result1 = allgumbel(u[:min_old], v[:min_old])
                            result2 = allfrank(u[min_old:min_new], v[min_old:min_new])
                            R = R * 2/3
                        else:
                            if(s[1] == 2 and s[2] == 3):
                                result2 = allfrank(u[:min_old], v[:min_old])
                                #result1 = allgumbel(u[min_old:min_new], v[min_old:min_new])
                                R = R * 2/3

            resultOld = allfrank(u[:min_new], v[:min_new])

            BFu = resultOld["BFu"] - result1["BFu"] - result2["BFu"]

            if BFu.imag:
                ss = -2
                print("Error\n")

            U2 = np.random.uniform()

            if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and BFu.imag == 0:
                new_model = new
                rejected = current
                QQ = Q
                w = 21
            else:
                new_model = current
                rejected = new
                QQ = q
                w = 22

	else:
            if max_new < max_old and max_new != 0:
                if(s[1] == 2 and s[2] == 2):
                    result1 = allfrank(u[max_new:max_old], v[max_new:max_old])
                    result2 = allfrank(u[max_old:L], v[max_old:L])
                    R = R * 1/3
                else:
                    if(s[1] == 2 and s[2] == 1):
                        result2 = allfrank(u[max_new:max_old], v[max_new:max_old])
                        result1 = allclayton(u[max_old:L], v[max_old:L])
                        R = R * 2/3
                    else:
                        if(s[1] == 1 and s[2] == 2):
                            result2 = allclayton(u[max_new:max_old], v[max_new:max_old])
                            result1 = allfrank(u[max_old:L], v[max_old:L])
                            R = R * 2/3
                        else:
                            if(s[1] == 2 and s[2] == 3):
                                result2 = allfrank(u[max_new:max_old], v[max_new:max_old])
                                #result1 = allgumbel(u[max_old:L], v[max_old:L])
                                R = R * 2/3
                            else:
                                if(s[1] == 3 and s[2] == 2):
                                    #result1 = allgumbel(u[max_new:max_old], v[max_new:max_old])
                                    result2 = allfrank(u[max_old:L], v[max_old:L])
                                    R = R * 2/3

                resultOld = allfrank(u[max_new:L], v[max_new:L])

                BFu = resultOld["BFu"] - result1["BFu"] - result2["BFu"]

                if BFu.imag:
                    ss = -2
                    print("Error\n")

                U2 = np.random.uniform()

                if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and BFu.imag == 0:
                    new_model = new
                    rejected = current
                    QQ = Q
                    w = 23
                else:
                    new_model = current
                    rejected = new
                    QQ = q
                    w = 24
            else:
                place = kn
                if(s[1] == 2 and s[2] == 2):
                    result1 = allfrank(u[current[place - 2]:current[place - 1]], v[current[place - 2]:current[place - 1]])
                    result2 = allfrank(u[current[place - 1]:current[place]], v[current[place - 1]:current[place]])
                    R = R * 1/3
                else:
                    if(s[1] == 1 and s[2] == 2):
                        result1 = allclayton(u[current[place - 2]:current[place - 1]], v[current[place - 2]:current[place - 1]])
                        result2 = allfrank(u[current[place - 1]:current[place]], v[current[place - 1]:current[place]])
                        R = R * 2/3
                    else:
                        if(s[1] == 2 and s[2] == 1):
                            result1 = allfrank(u[current[place - 2]:current[place - 1]], v[current[place - 2]:current[place - 1]])
                            result2 = allclayton(u[current[place - 1]:current[place]], v[current[place - 1]:current[place]])
                            R = R * 2/3
                        else:
                            if(s[1] == 3 and s[2] == 2):
                                #result1 = allgumbel(u[current[place - 2]:current[place - 1]], v[current[place - 2]:current[place - 1]])
                                result2 = allfrank(u[current[place - 1]:current[place]], v[current[place - 1]:current[place]])
                                R = R * 2/3
                            else:
                                if(s[1] == 2 and s[2] == 3):
                                    result1 = allfrank(u[current[place - 2]:current[place - 1]], v[current[place - 2]:current[place - 1]])
                                    #result2 = allgumbel(u[current[place - 1]:current[place]], v[current[place - 1]:current[place]])
                                    R = R * 2/3

                resultOld = allfrank(u[current[place - 2]:current[place]], v[current[place - 2]:current[place]])

                BFu = resultOld["BFu"] - result1["BFu"] - result2["BFu"]

                if BFu.imag:
                    ss = -2
                    print("Error\n")

                U2 = np.random.uniform()

                if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and BFu.imag == 0:
                    new_model = new
                    rejected = current
                    QQ = Q
                    w = 25
                else:
                    new_model = current
                    rejected = new
                    QQ = q
                    w = 26


    else:
        if not np.any(new):
            R = 2

            if(s[1] == 2 and s[2] == 2):
                result1 = allfrank(u[:max_old], v[:max_old])
                result2 = allfrank(u[max_old:L], v[max_old:L])
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
                        if(s[1] == 3 and s[2] == 2):
                            #result1 = allgumbel(u[:max_old], v[:max_old])
                            result2 = allfrank(u[max_old:L], v[max_old:L])
                            R = R * 2/3
                        else:
                            if(s[1] == 2 and s[2] == 3):
                                result2 = allfrank(u[:max_old], v[:max_old])
                                #result1 = allgumbel(u[max_old:L], v[max_old:L])
                                R = R * 2/3

            resultOld = allfrank(u, v)

            BFu = resultOld["BFu"] - result1["BFu"] - result2["BFu"]

            if BFu.imag:
                ss = -2
                print("Error\n")

            U2 = np.random.uniform()

            if  (np.log(U2) <  min(0, ((zita ** (chain - 1)) * BFu) + np.log(R))) and BFu.imag == 0:
                new_model = new
                rejected = current
                QQ = Q
                w = 27
            else:
                new_model = current
                rejected = new
                QQ = q
                w = 28

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
    newModel = np.array([[0], [0], [0], [0], [45]])
    kn = 45
    s = [1, 2, 3, 4]
    q = 3
    Q = 5
    zita = 5
    chain = 6

    result = bayes_kill_frank(currentModel, newModel, kn, u, v, s, q, Q, zita, chain)

    print(result)
