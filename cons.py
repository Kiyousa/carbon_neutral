import numpy as np
from problem_description import *


def g(t):
    """The coefficients are adopted form Xu's work"""
    # g(t) = 0 if t < 0
    w = 201.19
    k = 6.727
    a = 0.0617
    value = w / (1 + k * np.exp(-a * t))
    return value


constrain = np.array([g(y - i) - g(y - 1 - i) for i in range(y)])
biomass_t = np.array([g(i) for i in range(y, 0, -1)])


def later(t):
    return np.array([g(y + t - i) - g(y + t - 1 - i) for i in range(y)])


def exist_forest_seq_t(year):
    """return the net carbon sequestration of exist forest in year t"""
    x_young_age = 58.7754  # g(20)
    x_middle_age = 56.2592  # g(50)
    x_per_mature = 28.6133  # g(70)
    x_mature = 24.6766  # g(100) 
    x_over_mature = 11.5640  # g(120)

    x_exists = [x_young_age, x_middle_age, x_per_mature, x_mature, x_over_mature]
    car_seq_co = [g(20 + year) - g(20 + year - 1),
                  g(50 + year) - g(50 + year - 1),
                  g(70 + year) - g(70 + year - 1),
                  g(100 + year) - g(100 + year - 1),
                  g(120 + year) - g(120 + year - 1)]
    return np.dot(x_exists, car_seq_co)


def cons_cs(x): return np.dot(x, constrain) + exist_forest_seq_t(y) - T
