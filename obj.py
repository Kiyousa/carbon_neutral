import numpy as np
from problem_description import *
from cons import biomass_t

di = 1 / (1 + r)
coefficient = np.array([di ** x for x in range(y)])


def pv_sigma_linear(x):
    """return the obj value and the grad of the object function"""
    n = len(x)
    var = np.var(x)
    pv = np.dot(coefficient, x)
    # print("pv:", pv, "var:", var)
    obj = alpha * pv + beta * var
    grad = alpha * coefficient + beta * 2 / n * (x - np.mean(x))
    return obj, grad