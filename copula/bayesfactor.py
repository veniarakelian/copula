
from scipy.stats import norm, expon
from scipy.optimize import minimize
from scipy.linalg import det, inv
from math import pi
import numpy as np
from allnorm import allnorm
from copulalib.copulalib import Copula
from bayesfactor import bayesfactor

def bayesfactor(x,y,thetastart,copula)

if copula==1
    [~,~,~,~,~,BFu]=allclayton(x,y,thetastart)
else
    if copula==2
        [~,~,~,~,~,BFu]=allfrank(x,y,thetastart)
    else
        [~,~,~,~,~,BFu]=allgumbel(x,y,thetastart)
    #end
#end

return BFu

# den kserw pws na periorisw kai na parw mono to BFu apo ta results
# result = {"theta": theta, "cop1": cop1, "hes": hes, "hes_prior_cor": hes_prior_cop, "BF": BF, "BFu": BFu}
#   return result