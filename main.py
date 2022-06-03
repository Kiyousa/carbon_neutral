import numpy as np
from scipy.optimize import minimize
from problem_description import *
from obj import pv_sigma_linear, coefficient
from cons import cons_cs, constrain, later, g, exist_forest_seq_t

np.set_printoptions(suppress=True)

cons = ({'type': 'eq', 'fun': cons_cs})
bound = [(0, np.inf) for i in range(y)]
"Ways to get a initial solution"
# x0 = np.array([0.0] * y)
# x0[39] = (T - exist_forest_seq_t(y)) / (g(1) - g(0))
# x0 = (T - exist_forest_seq_t(y)) / constrain / y
x0 = ((T - exist_forest_seq_t(y)) / sum(constrain)) * np.ones(y)

# , tol=1e-11, options={'disp': True, 'maxiter': 500})
res = minimize(pv_sigma_linear, x0, method='SLSQP',
               jac=True, bounds=bound, constraints=cons,
               options={'disp': True, 'maxiter': 100})
print(res)
# print("initial solution:\n", x0)
print("carbon sequestration in year Y under initial solution", np.dot(x0, constrain) + exist_forest_seq_t(y))
print("discount rate", 1 / (1 + r))
print("Pv = ", np.dot(coefficient, res.x))

span = 30
constrain_after = np.array([g(y + span - i) - g(y + span - 1 - i) for i in range(y + span)])
car_seq_mat = np.matrix(np.zeros(y * (y + span)).reshape(y + span, y))
for i in range(y):
    car_seq_mat[i, :i + 1] = constrain_after[y + span - i - 1:]
for i in range(span):
    car_seq_mat[i + y] = constrain_after[span - i - 1: span - i - 1 + y]


car_seq_series = np.dot(car_seq_mat, res.x) + np.array([exist_forest_seq_t(t) for t in range(1, y + span + 1)])
print("carbon sequestration series:\n", car_seq_series)
print("carbon sequestration target:", 85.9e2 * 12.0 / 44.0 * 2.0)
print("total new area", sum(res.x))

xop= 2
# np.savez('conservative_0', sol=res.x, seq=car_seq_series)
# np.savez('conservative_1', sol=res.x, seq=car_seq_series)
# np.savez('conservative_2', sol=res.x, seq=car_seq_series)
# np.savez('optimistic_0', sol=res.x, seq=car_seq_series)
# np.savez('optimistic_1', sol=res.x, seq=car_seq_series)
# np.savez('optimistic_2', sol=res.x, seq=car_seq_series)