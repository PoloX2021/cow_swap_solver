import numpy as np
#Returns a function which calaculates ExactInput or ExactInput for a token pair
# Token 1 is the token with the exact value
# tokenIn bool which defines if the amount given is:
#   the exact input (True), then it returns the output
#   the exact output (False), then it returns the input

#We assume that if tokenIn is False, then x<balanceToken1
def cf(balanceToken1, balanceToken2, fee, tokenIn):
    def g(x):
        if tokenIn:
            return (-balanceToken1*balanceToken2/(balanceToken1+x)+balanceToken2)*(1-fee)
        if x>=balanceToken1:
            return np.inf
        return int((balanceToken1*balanceToken2/(balanceToken1-x)-balanceToken2)*(1+fee))
    return g