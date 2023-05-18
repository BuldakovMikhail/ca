import matplotlib.pyplot as plt
import numpy as np
#https://colab.research.google.com/drive/1VzeUeLm7O3L1CRm4cOOk2-rmlgfzuJWm?usp=sharing

def gaussElim(a, b):
    n = len(b)
    for k in range(0, n-1):
        for i in range(k+1, n):
            if a[i, k] != 0.0:
                lam = a[i, k] / a[k, k]
                a[i, k+1:n] = a[i, k+1:n] - lam*a[k, k+1:n]
                b[i] = b[i] - lam*b[k]
    for k in range(n-1, -1, -1):
        b[k] = (b[k] - np.dot(a[k, k+1:n], b[k+1:n]))/a[k, k]

    return b


class LinearRegression:
    def __init__(self, x, y, p, n):
        self.x = x
        self.y = y
        self.p = p

        self.n = n + 1

        self.train()

    def train(self):
        mat = [[0] * self.n for _ in range(self.n)]
        b = []

        for i in range(self.n):
            for j in range(self.n):
                mat[i][j] = np.dot(self.p, self.x ** (i + j))
            b.append(np.dot(self.y, self.p * (self.x ** i)))

        mat = np.array(mat)
        self.a = np.array(gaussElim(mat, b))

    def get_func_value(self, x):
        return np.polyval(self.a[::-1], x)


class LinearRegression3D:
    def __init__(self, x, y, z, p):
        self.x = x
        self.y = y
        self.z = z
        self.p = p
        self.n = 3

        self.train()

    def train(self):
        mat = [[0] * self.n for i in range(self.n)]

        mat[0][0] = np.dot(self.p, self.x ** 0)
        mat[0][1] = np.dot(self.p, self.x)
        mat[0][2] = np.dot(self.p, self.y)

        mat[1][0] = np.dot(self.p, self.x)
        mat[1][1] = np.dot(self.p, self.x ** 2)
        mat[1][2] = np.dot(self.p, self.y * self.x)

        mat[2][0] = np.dot(self.p, self.y)
        mat[2][1] = np.dot(self.p, self.x * self.y)
        mat[2][2] = np.dot(self.p, self.y ** 2)

        b = [np.dot(self.p, self.z), np.dot(self.p, self.z *
                                            self.x), np.dot(self.p, self.z * self.y)]

        mat = np.array(mat)

        self.a = np.array(gaussElim(mat, b))

    def get_func_value(self, x, y):
        return self.a[0] + self.a[1] * x + self.a[2] * y


def show_menu():
    print("""
1) Показать таблицу
2) Построить графики
3) Изменить веса
4) Создать таблицу (2D)
5) Заполнить вектор весов
6) Создать таблицу (3D)
7) Показать таблицу (3D)
8) Построить графики для (3D) 
9) Решить диффур
0) Выйти""")


def table_create(N):
    X_l = np.random.uniform(0, 2, size=N).reshape((-1, 1))
    Y_l = (1+25*X_l**2)**-1 + np.random.normal(scale=0.1, size=X_l.shape)

    x_temp = X_l.reshape(-1)
    y_temp = Y_l.reshape(-1)

    return x_temp, y_temp


def table_create_3d(N):
    X_l = np.random.uniform(0, 2, size=N).reshape((-1, 1))
    Y_l = np.random.uniform(0, 2, size=N).reshape((-1, 1))
    Z_l = X_l ** 2 / 25 - Y_l ** 2 / 16 + \
        np.random.normal(scale=0.1, size=X_l.shape)

    x_temp = X_l.reshape(-1)
    y_temp = Y_l.reshape(-1)
    z_temp = Z_l.reshape(-1)

    return x_temp, y_temp, z_temp


def print_table(x, y, p):
    print("|{:^10}||{:^10}||{:^10}||{:^10}|".format("№", "x", "y", "p"))
    print("-" * 48)
    for i in range(len(x)):
        print("|{:^10}||{:^10.3f}||{:^10.3f}||{:^10.3f}|".format(
            i, x[i], y[i], p[i]))


def print_table_3d(x, y, z, p):
    print("|{:^10}||{:^10}||{:^10}||{:^10}||{:^10}|".format(
        "№", "x", "y", "z", "p"))
    print("-" * 58)
    for i in range(len(x)):
        print("|{:^10}||{:^10.3f}||{:^10.3f}||{:^10.3f}||{:^10.3f}|".format(
            i, x[i], y[i], z[i], p[i]))


def plot(x, y, p):
    l1 = LinearRegression(x, y, p, 1)
    l2 = LinearRegression(x, y, p, 2)
    l3 = LinearRegression(x, y, p, 4)

    fig, ax = plt.subplots()
    ax.scatter(x, y)

    x_temp = np.linspace(0, max(x), len(x) * 10)
    y_temp = [l1.get_func_value(i) for i in x_temp]
    ax.plot(x_temp, y_temp, label="n = 1")

    y_temp = [l2.get_func_value(i) for i in x_temp]
    ax.plot(x_temp, y_temp, label="n = 2")

    y_temp = [l3.get_func_value(i) for i in x_temp]
    ax.plot(x_temp, y_temp, label="n = 4")

    ax.set_ylim(min(y), max(y))
    ax.legend()
    plt.show()


def plot_3d(x, y, z, p):
    l1 = LinearRegression3D(x, y, z, p)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter(x, y, z)

    x_grid = np.linspace(min(x), max(x), len(x))
    y_grid = np.linspace(min(y), max(y), len(y))
    X, Y = np.meshgrid(x_grid, y_grid)
    z = l1.get_func_value(X, Y)

    ax.plot_surface(X, Y, z)

    plt.show()


def equation(x, a):
    return (1 - x) + a[0] * (x * (1 - x)) + a[1] * (x**2 * (1 - x)) + a[2] * (x**3 * (1 - x))


def equation_solution():
    X = np.linspace(-10, 10, 1000)

    alpha = -2 + 2 * X - 3 * X ** 2
    bet = 2 - 6 * X + 3 * X ** 2 - 4 * X ** 3
    gam = 6 * X - 12 * X ** 2 + 4 * X ** 3 - 5 * X ** 4

    b = []

    mat = [[0] * 3 for _ in range(3)]

    temp = [alpha, bet, gam]
    for i in range(3):
        b.append(np.dot((4 * X - 1), temp[i]))
        for j in range(3):
            mat[i][j] = np.dot(temp[i], temp[j])

    mat = np.array(mat)
    mat2 = np.array(mat[:2, :2])
    b2 = b[:2]

    a = gaussElim(mat, b)
    a2 = gaussElim(mat2, b2)

    fig, ax = plt.subplots()

    a2.append(0)

    ax.plot(X, equation(X, a2), label="m=2")
    ax.plot(X, equation(X, a), label="m=3")

    print(
        "Ответ: y(x) = (1 - x) {:+f} * (x(1-x)) {:+f} * (x^2(1-x))".format(a2[0], a2[1]))

    print(
        "Ответ: y(x) = (1 - x) {:+f} * (x(1-x)) {:+f} * (x^2(1-x)) {:+f} * (x^3(1-x))".format(a[0], a[1], a[2]))

    ax.legend()
    plt.show()


def main():
    p = []
    x = []
    y = []
    z = []

    while True:
        show_menu()
        com = int(input("Введите пункт: "))
        if com == 1:
            print_table(x, y, p)
        elif com == 2:
            plot(x, y, p)
        elif com == 3:
            i, val = map(float, input(
                "Введите позицию и значение через пробел: ").split(" "))
            i = int(i)
            p[i] = val
        elif com == 4:
            N = int(input("Введите количество точек: "))
            x, y = table_create(N)
            p = np.ones(N)
        elif com == 5:
            val = int(input("Введите новый вес: "))
            p = np.ones(len(x)) * val
        elif com == 6:
            N = int(input("Введите количество точек: "))
            x, y, z = table_create_3d(N)
            p = np.ones(N)
        elif com == 7:
            print_table_3d(x, y, z, p)
        elif com == 8:
            plot_3d(x, y, z, p)
        elif com == 9:
            equation_solution()
        elif com == 0:
            break


# 1) Показать таблицу
# 2) Построить графики
# 3) Изменить веса
# 4) Создать таблицу (2D)
# 5) Заполнить вектор весов
# 6) Создать таблицу (3D)
# 7) Показать таблицу (3D)
# 8) Построить графики для (3D)
# 0) Выйти
if __name__ == '__main__':
    main()
