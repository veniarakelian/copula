from __future__ import division
from __future__ import print_function
from laplace_tourlou import laplace_tourlou
from acceptrejectaux import acceptrejectaux
from pandas import read_excel
import numpy as np
import sys
import time

np.random.seed(2)

df = read_excel("../data/artificial_data.xlsx", sheet_name='Sheet1')
x = []
y = []
					
for index, row in df.iterrows():
	x.append([float(row['x'])])
	y.append([float(row['y'])])

x = np.asarray(x, dtype=np.float32)
y = np.asarray(y, dtype=np.float32)

dist = 30
numbrk = 5
itera = 50
burnin = 2000
Zita = 0.8
delta = 0.1

chain1 = 1
chain2 = 2
chain3 = 3
chain4 = 4
chain5 = 5

current_model1 = np.zeros(numbrk, dtype=int)
current_model2 = np.zeros(numbrk, dtype=int)
current_model3 = np.zeros(numbrk, dtype=int)
current_model4 = np.zeros(numbrk, dtype=int)
current_model5 = np.zeros(numbrk, dtype=int)

current_model2[0] = 100
current_model2[1] = 180

current_model3[1] = 100
current_model3[2] = 200

current_model2 = np.sort(current_model2)
current_model3 = np.sort(current_model3)

QQ1 = np.ones(numbrk + 1, dtype=int)
QQ2 = 2 * np.ones(numbrk + 1, dtype=int)
QQ3 = 3 * np.ones(numbrk + 1, dtype=int)
QQ4 = np.ones(numbrk + 1, dtype=int)
QQ5 = np.ones(numbrk + 1, dtype=int)

# Initial conditions
accept = 0
zita = [Zita]
j = 0
jump = [0]
Accept = [0]
acceptrate = [0]

start = time.time()
for i in range(0, itera):
    
    print("\rStep: {}/{}".format(i + 1, itera), end = "")
    sys.stdout.flush()

    if i >= 9 and (i+1) % 10 == 0:
        j += 1

        # Updates zita #
        if i >= 499 and ((i+1) % 500 == 0) and (i + 1 <= burnin):
            zita.append(zita[j-1] + delta * (0.5 - (Accept[j-1] - Accept[j-50]) / 50))
        elif j == 0:
            zita.append(Zita)
        else:            
            zita.append(zita[j - 1])

        if np.random.uniform(low=np.nextafter(0.0, 1.0)) < 0.25:
            chain = 2
            result = acceptrejectaux(current_model1[i], current_model2[i], QQ1[i], QQ2[i], x, y, chain, zita[j])
            newmodel = result["currentModel"]
            Q = result["QQ"]
            accept = result["accept"]

            result = laplace_tourlou(current_model2[i], x, y, numbrk, dist, QQ2[i], zita[j], chain2)
            current_model2 = np.vstack((current_model2, result["new_model"]))
            rejected2 = np.vstack((rejected2, result["rejected"]))
            QQ2 = np.vstack((QQ2, result["QQ"]))

            result = laplace_tourlou(current_model3[i], x, y, numbrk, dist, QQ3[i], zita[j], chain3)
            current_model3 = np.vstack((current_model3, result["new_model"]))
            rejected3 = np.vstack((rejected3, result["rejected"]))
            QQ3 = np.vstack((QQ3, result["QQ"]))

            result = laplace_tourlou(current_model4[i], x, y, numbrk, dist, QQ4[i], zita[j], chain4)
            current_model4 = np.vstack((current_model4, result["new_model"]))
            rejected4 = np.vstack((rejected4, result["rejected"]))
            QQ4 = np.vstack((QQ4, result["QQ"]))

            result = laplace_tourlou(current_model5[i], x, y, numbrk, dist, QQ5[i], zita[j], chain5)
            current_model5 = np.vstack((current_model5, result["new_model"]))
            rejected5 = np.vstack((rejected5, result["rejected"]))
            QQ5 = np.vstack((QQ5, result["QQ"]))

        else:
            if 0.25 <= np.random.uniform(low=np.nextafter(0.0, 1.0)) < 0.5:
                chain = 3
                result = acceptrejectaux(current_model1[i], current_model3[i], QQ1[i], QQ3[i], x, y, chain,zita[j])
                newmodel = result["currentModel"]
                Q = result["QQ"]
                accept = result["accept"]

                result = laplace_tourlou(current_model2[i], x, y, numbrk, dist, QQ2[i], zita[j], chain2)
                current_model2 = np.vstack((current_model2, result["new_model"]))
                rejected2 = np.vstack((rejected2, result["rejected"]))
                QQ2 = np.vstack((QQ2, result["QQ"]))

                result = laplace_tourlou(current_model3[i], x, y, numbrk, dist, QQ3[i], zita[j], chain3)
                current_model3 = np.vstack((current_model3, result["new_model"]))
                rejected3 = np.vstack((rejected3, result["rejected"]))
                QQ3 = np.vstack((QQ3, result["QQ"]))
                
                result = laplace_tourlou(current_model4[i], x, y, numbrk, dist, QQ4[i], zita[j], chain4)
                current_model4 = np.vstack((current_model4, result["new_model"]))
                rejected4 = np.vstack((rejected4, result["rejected"]))
                QQ4 = np.vstack((QQ4, result["QQ"]))
        
                result = laplace_tourlou(current_model5[i], x, y, numbrk, dist, QQ5[i], zita[j], chain5)
                current_model5 = np.vstack((current_model5, result["new_model"]))
                rejected5 = np.vstack((rejected5, result["rejected"]))
                QQ5 = np.vstack((QQ5, result["QQ"]))

            else:
                if 0.5 <= np.random.uniform(low=np.nextafter(0.0, 1.0)) < 0.75:
                    chain = 4
                    result = acceptrejectaux(current_model1[i], current_model4[i], QQ1[i], QQ4[i], x, y, chain, zita[j])
                    newmodel = result["currentModel"]
                    Q = result["QQ"]
                    accept = result["accept"]

                    result = laplace_tourlou(current_model2[i], x, y, numbrk, dist, QQ2[i], zita[j], chain2)
                    current_model2 = np.vstack((current_model2, result["new_model"]))
                    rejected2 = np.vstack((rejected2, result["rejected"]))
                    QQ2 = np.vstack((QQ2, result["QQ"]))

                    result = laplace_tourlou(current_model3[i], x, y, numbrk, dist, QQ3[i], zita[j], chain3)
                    current_model3 = np.vstack((current_model3, result["new_model"]))
                    rejected3 = np.vstack((rejected3, result["rejected"]))
                    QQ3 = np.vstack((QQ3, result["QQ"]))

                    result = laplace_tourlou(current_model4[i], x, y, numbrk, dist, QQ4[i], zita[j], chain4)
                    current_model4 = np.vstack((current_model4, result["new_model"]))
                    rejected4 = np.vstack((rejected4, result["rejected"]))
                    QQ4 = np.vstack((QQ4, result["QQ"]))

                    result = laplace_tourlou(current_model5[i], x, y, numbrk, dist, QQ5[i], zita[j], chain5)
                    current_model5 = np.vstack((current_model5, result["new_model"]))
                    rejected5 = np.vstack((rejected5, result["rejected"]))
                    QQ5 = np.vstack((QQ5, result["QQ"]))
                else:
                    chain = 5
                    result = acceptrejectaux(current_model1[i], current_model5[i], QQ1[i], QQ5[i], x, y, chain, zita[j])
                    newmodel = result["currentModel"]
                    Q = result["QQ"]
                    accept = result["accept"]

                    result = laplace_tourlou(current_model2[i], x, y, numbrk, dist, QQ2[i], zita[j], chain2)
                    current_model2 = np.vstack((current_model2, result["new_model"]))
                    rejected2 = np.vstack((rejected2, result["rejected"]))
                    QQ2 = np.vstack((QQ2, result["QQ"]))

                    result = laplace_tourlou(current_model3[i], x, y, numbrk, dist, QQ3[i], zita[j], chain3)
                    current_model3 = np.vstack((current_model3, result["new_model"]))
                    rejected3 = np.vstack((rejected3, result["rejected"]))
                    QQ3 = np.vstack((QQ3, result["QQ"]))

                    result = laplace_tourlou(current_model4[i], x, y, numbrk, dist, QQ4[i], zita[j], chain4)
                    current_model4 = np.vstack((current_model4, result["new_model"]))
                    rejected4 = np.vstack((rejected4, result["rejected"]))
                    QQ4 = np.vstack((QQ4, result["QQ"]))

                    result = laplace_tourlou(current_model5[i], x, y, numbrk, dist, QQ5[i], zita[j], chain5)
                    current_model5 = np.vstack((current_model5, result["new_model"]))
                    rejected5 = np.vstack((rejected5, result["rejected"]))
                    QQ5 = np.vstack((QQ5, result["QQ"]))

        current_model1 = np.vstack((current_model1, newmodel))
        QQ1 = np.vstack((QQ1, Q))
        Accept.append(Accept[j-1] + accept)
    else:

        if i == 0:
            result = laplace_tourlou(current_model1, x, y, numbrk, dist, QQ1, zita[j], chain1)
            current_model1 = np.vstack((current_model1, result["new_model"]))
            rejected1 = result["rejected"]
            QQ1 = np.vstack((QQ1, result["QQ"]))

            result = laplace_tourlou(current_model2, x, y, numbrk, dist, QQ2, zita[j], chain2)
            current_model2 = np.vstack((current_model2, result["new_model"]))
            rejected2 = result["rejected"]
            QQ2 = np.vstack((QQ2, result["QQ"]))
            
            result = laplace_tourlou(current_model3, x, y, numbrk, dist, QQ3, zita[j], chain3)
            current_model3 = np.vstack((current_model3, result["new_model"]))
            rejected3 = result["rejected"]
            QQ3 = np.vstack((QQ3, result["QQ"]))
            
            result = laplace_tourlou(current_model4, x, y, numbrk, dist, QQ4, zita[j], chain4)
            current_model4 = np.vstack((current_model4, result["new_model"]))
            rejected4 = result["rejected"]
            QQ4 = np.vstack((QQ4, result["QQ"]))
            
            result = laplace_tourlou(current_model5, x, y, numbrk, dist, QQ5, zita[j], chain5)
            current_model5 = np.vstack((current_model5, result["new_model"]))
            rejected5 = result["rejected"]
            QQ5 = np.vstack((QQ5, result["QQ"]))
         
        else:
            result = laplace_tourlou(current_model1[i], x, y, numbrk, dist, QQ1[i], zita[j], chain1)
            current_model1 = np.vstack((current_model1, result["new_model"]))
            rejected1 = np.vstack((rejected1, result["rejected"]))
            QQ1 = np.vstack((QQ1, result["QQ"]))

            result = laplace_tourlou(current_model2[i], x, y, numbrk, dist, QQ2[i], zita[j], chain2)
            current_model2 = np.vstack((current_model2, result["new_model"]))
            rejected2 = np.vstack((rejected2, result["rejected"]))
            QQ2 = np.vstack((QQ2, result["QQ"]))

            result = laplace_tourlou(current_model3[i], x, y, numbrk, dist, QQ3[i], zita[j], chain3)
            current_model3 = np.vstack((current_model3, result["new_model"]))
            rejected3 = np.vstack((rejected3, result["rejected"]))
            QQ3 = np.vstack((QQ3, result["QQ"]))

            result = laplace_tourlou(current_model4[i], x, y, numbrk, dist, QQ4[i], zita[j], chain4)
            current_model4 = np.vstack((current_model4, result["new_model"]))
            rejected4 = np.vstack((rejected4, result["rejected"]))
            QQ4 = np.vstack((QQ4, result["QQ"]))

            result = laplace_tourlou(current_model5[i], x, y, numbrk, dist, QQ5[i], zita[j], chain5)
            current_model5 = np.vstack((current_model5, result["new_model"]))
            rejected5 = np.vstack((rejected5, result["rejected"]))
            QQ5 = np.vstack((QQ5, result["QQ"]))

    # Counts models jumps #
    if (np.any(current_model1[i+1] - current_model1[i] != np.zeros(numbrk)) or (np.all(current_model1[i+1] - current_model1[i] == np.zeros(numbrk)) and np.any(QQ1[i+1] - QQ1[i] != np.zeros(numbrk+1)))):
        jump.append(jump[i] + 1)
    else:
        jump.append(jump[i])

	# counts acceptance rate # 
    acceptrate.append(jump[i + 1] / (i+1))

end = time.time()

print("\nElapsed: " + str(round(end - start,3)) + "sec")

