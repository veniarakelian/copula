from allclayton import allclayton
from allfrank import allfrank
from allgumbel import allgumbel

def bayesfactor(x, y, copula):

    if copula==1:
        BFu = allclayton(x,y)["BFu"]
    elif copula==2:
        BFu = allfrank(x,y)["BFu"]
    else:
        BFu = allgumbel(x,y)["BFu"]

    return BFu
