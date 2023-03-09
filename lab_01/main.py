import numpy as np
import matplotlib.pyplot as plt

def read_table_with_der():
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


def read_table():
    table = []
    line = input()
    while line != '~':
        line = line.split(' ')
        if len(line) == 2:
            x, y = line
        else:
            return None

        if not (x and y):
            return None
        try:
            x = float(x)
            y = float(y)
        except:
            return None

        table.append([x, y, 1])
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
    while pos < len(table) - 1 and table[pos][0] < x:
        pos += 1
    
    if pos != 0 and abs(table[pos][0] - x) > abs(table[pos - 1][0] - x):
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
    while pos < len(table) - 1 and table[pos][0] < x:
        pos += 1
    
    if pos != 0 and abs(table[pos][0] - x) > abs(table[pos - 1][0] - x):
        pos -= 1
    
    new_table.append(table[pos].copy())
    if len(new_table) < n + 1:
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


def system_solution(table_1, table_2, n):
    res_table = []
    
    for i in table_2:
        res_table.append([i[0], approximate_newton(table_1, i[0], n) - i[1], i[2]])
        
    i = 0
    while i < len(res_table) - 1:
        if res_table[i + 1][1] > res_table[i][1]:
            res_table.pop(i)
        else:
            i += 1
    
    #print(*res_table, sep='\n')
    
    return root_find_newton(res_table, n)


def main():
    
    print("Введите x, y, y` через пробел, для окончания ввода введите '~': ")
    table = read_table_with_der()
    
    if not table:
        print("Ошибка ввода")
        return

    # n = input('Введите n: ')
    # if not n.isdigit():
    #     print("Ошибка ввода")
    #     return
    # n = int(n)
    
    # if len(table) < n + 1:
    #     print("Недостаточно точек")
    #     return

    x = input('Введите х: ')
    try:
        x = float(x)
    except:
        print('Ошибка ввода')
        return
    
    if x < min([x[0] for x in table]) or x > max([x[0] for x in table]):
        print("Возникла экстраполяция") 
    
    
    print("Приблизительное значение:")
    print('-' * 64)  
    print('|{:^20}|{:^20}|{:^20}|'.format('n', 'Newton', 'Hermite'))
    print('-' * 64)    
    for i in range(len(table)):
        print("|{:^20d}|{:^20.3f}|{:^20.3f}|".format(i, approximate_newton(table, x, i), approximate_hermite(table, x, i)))
    print('-' * 64)  
    
    
    print("Нахождение корня:")
    print('-' * 64)  
    print('|{:^20}|{:^20}|{:^20}|'.format('n', 'Newton', 'Hermite'))
    print('-' * 64)    
    for i in range(len(table)):
        print("|{:^20d}|{:^20.3f}|{:^20.3f}|".format(i, root_find_newton(table, i), root_find_hermite(table, i)))
    print('-' * 64)  
    
    
    print("Введите таблицу для первой функции. x, y через пробел, для окончания ввода введите '~': ")
    table_1 = read_table()
    
    if not table_1:
        print("Ошибка ввода")
        return
    
    print("Введите таблицу для второй функции. x, y через пробел, для окончания ввода введите '~': ")
    table_2 = read_table()
    
    if not table_2:
        print("Ошибка ввода")
        return
    
    print("Решение системы:")
    print('-' * 43)  
    print('|{:^20}|{:^20}|'.format('n', 'Newton'))
    print('-' * 43)    
    for i in range(8):
        print("|{:^20d}|{:^20.3f}|".format(i, system_solution(table_1, table_2, i)))
    print('-' * 43)  
    
    fig, ax = plt.subplots()
    ax.plot([x[0] for x in table], [x[1] for x in table], label='Таблица 1')
    
    new_x = list(np.linspace(table[0][0], table[0][1]))
    ax.plot(new_x, [approximate_newton(table, x, 5) for x in new_x], label='Апроксимация Ньютона (n = 5)')
    ax.plot(new_x, [approximate_hermite(table, x, 5) for x in new_x], label='Апроксимация Эрмита (n = 5)')
    ax.legend()
    ax.grid()
    
    fig_2, ax_2 = plt.subplots()
    ax_2.plot([x[0] for x in table_1], [x[1] for x in table_1], label='Таблица 1')
    ax_2.plot([x[0] for x in table_2], [x[1] for x in table_2], label='Таблица 2')
    ax_2.legend()
    ax_2.grid()
    
    plt.show()
    

if __name__ == '__main__':
    main()
