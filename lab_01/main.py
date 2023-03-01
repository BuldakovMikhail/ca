import math as m

import matplotlib.pyplot as plt

def read_table():
    table = []
    line = input()
    while line != '~':
        line = line.split(' ')
        if len(line) == 3:
            x, y, y_der = line
        else:
            return None

        if not (x and y and y_der):
            return None

        try:
            x = float(x)
            y = float(y)
            y_der = float(y_der)
        except:
            return None

        table.append([x, y, y_der])
        line = input()

    table.sort(key=lambda x: x[0])
    return table


def divided_diff(table):
    temp = [[0] * (len(table)) for i in range(len(table) + 2)]
    for i in range(len(table)):
        temp[0][i] = table[i][0]
        temp[1][i] = table[i][2]
        temp[2][i] = table[i][1]

    x_barier = 1
    
    for i in range(3, len(temp)):
        for j in range(len(temp[0]) - i + 2):
            if temp[0][j] - temp[0][j + x_barier] == 0:
                temp[i][j] = temp[1][j]
            else:
                temp[i][j] = (temp[i - 1][j] - temp[i - 1][j + 1]) / (temp[0][j] - temp[0][j + x_barier])
        x_barier += 1
    
    return [temp[i][0] for i in range(3, len(temp))]

def select_points_newton(table, x, n):
    new_table = []
    
    pos = 0
    while table[pos][0] < x:
        pos += 1
    
    if abs(table[pos][0] - x) < abs(table[pos - 1][0] - x):
        pos -= 1
    
    
    new_table.append(table[pos].copy())    
    
    l_bound = pos - 1
    r_bound = pos + 1
    
    while len(new_table) < n + 1:
        if l_bound >= 0 and len(new_table) < n + 1:
            new_table.append(table[l_bound].copy())
            l_bound -= 1
        if r_bound < len(table) and len(new_table) < n + 1:
            new_table.append(table[r_bound].copy())
            r_bound += 1
            
    new_table.sort(key=lambda x: x[0])
    
    if len(new_table) == n + 1:
        return new_table
    else:
        return None


def select_points_hermite(table, x, n):
    new_table = []
    
    pos = 0
    while table[pos][0] < x:
        pos += 1
    
    if abs(table[pos][0] - x) > abs(table[pos - 1][0] - x):
        pos -= 1
    
    new_table.append(table[pos].copy())
    new_table.append(table[pos].copy())       
    
    l_bound = pos - 1
    r_bound = pos + 1
    
    while len(new_table) < n + 1:
        if l_bound >= 0 and len(new_table) < n + 1:
            new_table.append(table[l_bound].copy())
            if len(new_table) < n + 1:
                new_table.append(table[l_bound].copy())
            l_bound -= 1
        if r_bound < len(table) and len(new_table) < n + 1:
            new_table.append(table[r_bound].copy())
            if len(new_table) < n + 1:
                new_table.append(table[r_bound].copy())
            r_bound += 1
            
    new_table.sort(key=lambda x: x[0])
    
    
    if len(new_table) == n + 1:
        return new_table
    else:
        return None

    
def approximate_newton(table, x, n):
    selected_points = select_points_newton(table, x, n)
    diffs = divided_diff(selected_points)
    
    res = selected_points[0][1]
    accum = 1
    i = 0
    while i < len(diffs):
        accum *= (x - selected_points[i][0])
        res += accum * diffs[i]
        i += 1
        
    return res

def approximate_hermite(table, x, n):
    selected_points = select_points_hermite(table, x, n)
    
    diffs = divided_diff(selected_points)
    
    res = selected_points[0][1]
    accum = 1
    i = 0
    while i < len(diffs):
        accum *= (x - selected_points[i][0])
        res += accum * diffs[i]
        i += 1
        
    return res
    

def root_find_newton(table, n):
    inverse_table = []
    
    for i in range(len(table)):
        inverse_table.append([table[i][1], table[i][0], 1 / table[i][2]])
    
    inverse_table.sort(key=lambda x: x[0])
    
    return approximate_newton(inverse_table, 0, n)


def root_find_hermite(table, n):
    inverse_table = []
    
    for i in range(len(table)):
        inverse_table.append([table[i][1], table[i][0], 1 / table[i][2]])
    
    inverse_table.sort(key=lambda x: x[0])
    
    return approximate_hermite(inverse_table, 0, n)


def main():
    #table = [[-0.5, 0.707, 0], [-0.25, 0.924, 0], [0, 1, 0], [0.25, 0.924, 0], [0.5, 0.707, 0], [0.75, 0.383, 0], [1, 0, 0]]
    print("Введите x, y, y` через пробел, для окончания ввода введите '~': ")
    table = read_table()
    
    # plt.plot([x[0] for x in table], [y[1] for y in table])
    # plt.show()
    print(table)
    
    print(approximate_hermite(table, 0.5, 7))
    print(approximate_newton(table, 0.5, 7))
    
    print(root_find_newton(table, 6))
    print(root_find_hermite(table, 6))
    
    
    # if not table:
    #     print("Ошибка ввода")
    #     return

    # n = input('Введите n: ')
    # if not n.isdigit():
    #     print("Ошибка ввода")
    #     return
    # n = int(n)

    # x = input('Введите х: ')
    # try:
    #     x = float(x)
    # except:
    #     print('Ошибка ввода')
    #     return
    


    # x = input('Введите х: ')
    # try:
    #     x = float(x)
    # except:
    #     print('Ошибка ввода')
    #     return
    
    # x = input('Введите х: ')
    # try:
    #     x = float(x)
    # except:
    #     print('Ошибка ввода')
    #     return


if __name__ == '__main__':
    main()
