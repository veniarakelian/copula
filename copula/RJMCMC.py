from __future__ import division
import numpy as np
from laplace_tourlou import laplace_tourlou
from pandas import read_excel

df = read_excel("/home/petropoulakis/Desktop/artificial_data_iosif.xlsx", sheet_name='Sheet1')
x = []
y = []

for index, row in df.iterrows():
    x.append([float(row['x'])])
    y.append([float(row['x'])])

x = np.asarray(x, dtype=np.float32)
y = np.asarray(y, dtype=np.float32)

dist = 30
numbrk = 30
itera = 5000
burnin = 2500
Zita = 0.8
delta = 0.1

chain1 = 1
chain2 = 2
chain3 = 3
chain4 = 4
chain5 = 5

currentModel1 = np.zeros(numbrk, dtype=int)
currentModel1[numbrk - 1] = 50

currentModel2 = np.zeros(numbrk, dtype=int)
currentModel2[0] = 100
currentModel2[1] = 180
currentModel2 = np.sort(currentModel2)

currentModel3 = np.zeros(numbrk, dtype=int)
currentModel3[0] = 100
currentModel3[1] = 200
currentModel3 = np.sort(currentModel3)

currentModel4 = np.zeros(numbrk, dtype=int)
currentModel4[numbrk - 1] = 400

currentModel5 = np.zeros(numbrk, dtype=int)
currentModel5[numbrk - 1] = 70
currentModel5 = np.sort(currentModel5)

QQ1 = np.ones(numbrk + 1, dtype=int)
QQ2 = 2 * np.ones(numbrk + 1, dtype=int)
QQ3 = 3 * np.ones(numbrk + 1, dtype=int)
QQ4 = np.ones(numbrk + 1, dtype=int)

# Initial conditions
zita = [Zita]
j = 0
jump = [0]
Accept = [0]
acceptrate = []

for i in range(0, itera):
    if(i % 10000 == 0):
        print(i)

    if i % 2 == 0:
        j += 1

        # Updates zita #
        if i % 500 == 0 and i < burnin:
            
            zita.append(zita[j-1] + delta * (0.5 - (Accept[j-1] - Accept[j-50]) / 50))
        else:
            zita.append(zita[j - 1])

        if np.random.uniform(low=np.nextafter(0.0, 1.0)) < 0.25:
            chain = 2
            result = acceptrejectaux(current_model1[:i], current_model2[:i], QQ1[:i], QQ2[:i], x, y, chain, zita[j])
            newmodel = result["currentModel"]
            Q = result["QQ"]
            accpt = result["accept"]
            result2 = laplace_tourlou(current_model2[:i], x, y, numbrk, dist, QQ2[:i], zita[j], chain2)
            result3 = laplace_tourlou(current_model3[:i], x, y, numbrk, dist, QQ3[:i], zita[j], chain3)
            result4 = laplace_tourlou(current_model4[:i], x, y, numbrk, dist, QQ4[:i], zita[j], chain4)
            result5 = laplace_tourlou(current_model5[:i], x, y, numbrk, dist, QQ5[:i], zita[j], chain5)
        else:
            if 0.25 <= np.random.uniform(low=np.nextafter(0.0, 1.0)) < 0.5:
                chain = 3
                result = acceptrejectaux(current_model1[:i], current_model3[:i], QQ1[:i], QQ3[:i], x, y, chain,zita[j]);
                newmodel = result["currentModel"]
                Q = result["QQ"]
                accpt = result["accept"]
                result2 = laplace_tourlou(current_model2[:i], x, y, numbrk, dist, QQ2[:i], zita[j], chain2)
                result3 = laplace_tourlou(current_model3[:i], x, y, numbrk, dist, QQ3[:i], zita[j], chain3)
                result4 = laplace_tourlou(current_model4[:i], x, y, numbrk, dist, QQ4[:i], zita[j], chain4)
                result5 = laplace_tourlou(current_model5[:i], x, y, numbrk, dist, QQ5[:i], zita[j], chain5)

            else:
                if 0.5 <= np.random.uniform(low=np.nextafter(0.0, 1.0)) < 0.75:
                    chain = 4
                    result = acceptrejectaux(current_model1[:i], current_model4[:i], QQ1[:i], QQ4[:i], x, y, chain, zita[j]);
                    newmodel = result["currentModel"]
                    Q = result["QQ"]
                    accpt = result["accept"]
                    result2 = laplace_tourlou(current_model2[:i], x, y, numbrk, dist, QQ2[:i], zita[j], chain2)
                    result3 = laplace_tourlou(current_model3[:i], x, y, numbrk, dist, QQ3[:i], zita[j], chain3)
                    result4 = laplace_tourlou(current_model4[:i], x, y, numbrk, dist, QQ4[:i], zita[j], chain4)
                    result5 = laplace_tourlou(current_model5[:i], x, y, numbrk, dist, QQ5[:i], zita[j], chain5)
                else:
                    chain = 5
                    result = acceptrejectaux(current_model1[:i], current_model5[:i], QQ1[:i], QQ5[:i], x, y, chain, zita[j])
                    newmodel = result["currentModel"]
                    Q = result["QQ"]
                    accpt = result["accept"]
                    result2 = laplace_tourlou(current_model2[:i], x, y, numbrk, dist, QQ2[:i], zita[j], chain2)
                    result3 = laplace_tourlou(current_model3[:i], x, y, numbrk, dist, QQ3[:i], zita[j], chain3)
                    result4 = laplace_tourlou(current_model4[:i], x, y, numbrk, dist, QQ4[:i], zita[j], chain4)
                    result5 = laplace_tourlou(current_model5[:i], x, y, numbrk, dist, QQ5[:i], zita[j], chain5)

        current_model1[:i+1] = newmodel
        QQ1[:i+1] = Q
        Accept.append(Accept[j-1] + accept)
    else:
        result1 = laplace_tourlou(current_model1[:i], x, y, numbrk, dist, QQ1[:i], zita[j], chain1)
        result2 = laplace_tourlou(current_model2[:i], x, y, numbrk, dist, QQ2[:i], zita[j], chain2)
        result3 = laplace_tourlou(current_model3[:i], x, y, numbrk, dist, QQ3[:i], zita[j], chain3)
        result4 = laplace_tourlou(current_model4[:i], x, y, numbrk, dist, QQ4[:i], zita[j], chain4)
        result5 = laplace_tourlou(current_model5[:i], x, y, numbrk, dist, QQ5[:i], zita[j], chain5)

    # Counts models jumps #
    if (np.any(current_model1[:i+1] - current_model1[: i] != np.zeros(numbrk)) or (np.all(current_model1[:i+1] - current_model1[:i] == np.zeros(numbrk)) and np.any(QQ1[:i+1] - QQ1[:i] != np.zeros(numbrk+1)))):
        jump.append(jump[i] + 1)
    else:
        jump.append(jump[i])

    # counts acceptance rate 
    acceptrate.append(jump[i + 1] / i)

'''

if (i%100000==0):
    savefile = 'EU_BANKS_EU_OTHER.mat'; 
    save(savefile)

end
end
#e

jumps  = find(mod(w1(burnin:end,1),2) != 0)
numofjumps = len(jumps)

'''


