from scipy.stats import norm, expon
from scipy.optimize import minimize
from scipy.linalg import det, inv
from math import pi
import numpy as np
from allnorm import allnorm
from copulalib.copulalib import Copula
from bayesfactor import bayesfactor

def acceptrejectaux[currentModel1,currentModel2,QQ1,QQ2,x,y,thetastart,chain,zita)

brks1 = np.nonzero(currentModel1) #find(currentModel1~=0)
brks2 = np.nonzero(currentModel2) #find(currentModel2~=0)
BFu1 = 0
BFu2 = 0
proposal1 = 0
proposal2 = 0

if brks1 != 0
    for i in range(1, (len(brks1)-1)
        temp1 = bayesfactor(x[currentModel1[brks1[i]]+1:currentModel1[brks1[i+1]]],y[currentModel1[brks1[i]]+1:currentModel1[brks1[i+1]]],thetastart,QQ1[i])
        BFu1=BFu1+temp1
    end
    BFu1=BFu1+bayesfactor(x[1:currentModel1(brks1(1))),y[1:currentModel1(brks1(1))),thetastart,QQ1[1])+bayesfactor(x[currentModel1(brks1(end)):len(x)),y[currentModel1(brks1(end)):len(y)),thetastart,QQ1[end])
else
    BFu1=bayesfactor(x,y,thetastart,QQ1[1])
#end

if brks2 != 0
    for i in range(1, len(brks2)-1)
        temp2=bayesfactor(x[currentModel2[brks2[i]]+1:currentModel2[brks2[i+1]]],y[currentModel2[brks2[i]]+1:currentModel2[brks2[i+1]]],thetastart,QQ1[i])
        BFu2=BFu2+temp2
    #end
    BFu2=BFu2+bayesfactor(x[1:currentModel2[brks2[1]]],y[1:currentModel2[brks2[1]]],thetastart,QQ2[1])+bayesfactor(x[currentModel2[brks2[end]]:len(x)],y[currentModel2[brks2[end]]:len(y)],thetastart,QQ1[end])
else
    BFu2=bayesfactor(x,y,thetastart,QQ2[1])
#end


u = np.random.uniform()

if log(u)<min(0,(1-zita^(chain-1))*(BFu2-BFu1))
   currentModel=currentModel2
   QQ=QQ2
   accept=1
else
   currentModel=currentModel1
   QQ=QQ1
   accept=0
#end  

result = {"currentModel": currentModel, "QQ": QQ, "accept": accept}
return result 