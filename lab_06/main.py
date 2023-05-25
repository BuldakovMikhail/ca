import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

import sympy as sym


a = 0
b = 1


def psi(x):
    return 1 - x


def fi(x):
    return 0


def get_legendre_poly(n):
    x = sym.symbols("x")
    func = f"(x**2-1)**{n} / (2 ** {n})"
    func = sym.sympify(func)
    func = func / sym.factorial(n)
    return sym.Derivative(func, (x, n)).doit()


def get_gauss_cofs(roots):
    matrix = np.array([roots ** i for i in range(len(roots))], dtype="float")
    b = np.array([0 if i % 2 != 0 else 2 / (i + 1)
                 for i in range(len(roots))], dtype="float")

    return np.linalg.solve(matrix, b)


def count_integral_gauss(a, b, func, N):
    legendre_poly = get_legendre_poly(N)
    roots = np.array(sym.solve(legendre_poly.doit(),
                     sym.Symbol('x')), dtype=np.float64)
    coffs = get_gauss_cofs(roots)

    x = (b + a) / 2 + (b - a) / 2 * roots
    fx = func(x)

    return (b - a) / 2 * fx @ coffs


def count_integral_simpson(a, b, func, n):
    N = 2 * n
    x = (b - a)

    steps = [x / N * i for i in range(N + 1)]

    h = x / N

    s1 = 2 * np.sum([func(steps[2 * j]) for j in range(1, N // 2)])
    s2 = 4 * np.sum([func(steps[2 * j - 1]) for j in range(1, N // 2 + 1)])

    return h / 3 * (func(steps[0]) + s1 + s2 + func(steps[N]))


class Plane:
    def __init__(self, data):
        Y = np.array(data.index)
        X = np.array(data.columns.values)
        matrix = np.array(
            [[1, X[0], Y[0]],
             [1, X[-1], Y[-1]],
             [1, X[0], Y[-1]]]
        )

        b = np.array([data[X[0]][Y[0]], data[X[-1]][Y[-1]], data[X[0]][Y[-1]]])

        self.coffs = np.linalg.solve(matrix, b)

    def get_value(self, x, y):
        return self.coffs[0] + self.coffs[1] * x + self.coffs[2] * y


def der(a, b, h):
    return (a - b) / h


def runge(y, h, i):

    f1 = (y[i] - y[i - 1]) / h
    f2 = (y[i] - y[i - 2]) / (2 * h)

    return f1 + (f1 - f2) / (2 ** 2 - 1)


def leveling_vars(y, x):
    eta = 1 / y
    xi = 1 / x
    eta_der_by_xi = [(eta[i+1] - eta[i]) / (xi[i + 1] - xi[i])
                     for i in range(len(xi) - 1)]
    y_der = [eta_der_by_xi[i] * y[i] ** 2 / x[i]
             ** 2 for i in range(len(eta_der_by_xi))]

    return y_der


def second_der(yn1, yn2, yn3, h):
    return (yn1 - 2 * yn2 + yn3) / h ** 2


def main():
    data = pd.read_csv('lab_06/data.csv', sep='\t', index_col=0, header=0)
    data.columns = data.columns.values.astype(np.float64)

    aprox = Plane(np.log(data))

    def func_1(x, y):
        # print(aprox.get_value(x, y))
        return np.exp(aprox.get_value(x, y))

    def solution(a, b, fi, psi, n1=10, n2=10):
        def wrap(y):
            def func_split(x):
                return func_1(x, y)
            return count_integral_gauss(fi(y), psi(y), func_split, n1)

        return count_integral_simpson(a, b, wrap, n2)

    print("Задание 1: ", round(solution(a, b, fi, psi), 3))

    x = np.array([i for i in range(1, 7)])
    data_2 = np.array([0.571, 0.889, 1.091, 1.231, 1.333, 1.412])

    h = (x[1] - x[0])
    one_side_ders = [der(data_2[i], data_2[i - 1], h)
                     for i in range(1, len(data_2))]
    center_ders = [der(data_2[i+1], data_2[i-1], 2 * h)
                   for i in range(1, len(data_2) - 1)]
    runge_ders = [runge(data_2, h, i) for i in range(2, len(data_2))]
    leveling = leveling_vars(data_2, x)
    second_ders = [second_der(data_2[i - 1], data_2[i], data_2[i + 1], h)
                   for i in range(1, len(data_2) - 1)]

    df = pd.DataFrame()
    df['y'] = data_2
    df['Односторонняя производная'] = ['*'] + \
        list(map(lambda x: round(x, 3), one_side_ders))
    df['Центральная производная'] = ['*'] + \
        list(map(lambda x: round(x, 3), center_ders)) + ['*']
    df['2я формула Рунге'] = ['*'] + ['*'] + \
        list(map(lambda x: round(x, 3), runge_ders))
    df['Выравнивающие переменные'] = list(
        map(lambda x: round(x, 3), leveling)) + ['*']
    df['Вторая производная'] = ['*'] + \
        list(map(lambda x: round(x, 3), second_ders)) + ['*']

    print(df)


if __name__ == '__main__':
    main()
