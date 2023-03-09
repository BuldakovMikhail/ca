import matplotlib.pyplot as plt
import numpy as np

from spline import *
from newton import *


if __name__ == '__main__':
    table = [[0, 0.250, 1],
    [0.5, 0.571, 1],
    [0.75, 0.842, 1],
    [1.25, 0.842, 1],
    [1.5, 0.571, 1],
    [2, 0.250, 1],
    [3, 0.077, 1],
    [4, 0.036, 1],
    [5, 0.020, 1],
    [6, 0.013, 1],
    [7, 0.009, 1]
    ]
    
    x_single = float(input('Введите х: '))
    
    x = [x[0] for x in table]
    y = [y[1] for y in table]
    
    selected_points_left = select_points_newton(table, min(x), 3)
    selected_points_right = select_points_newton(table, max(x), 3)
    
    divided_diffs_left = divided_diff(selected_points_left)
    divided_diffs_right = divided_diff(selected_points_right)
    
    newton_sec_dir_left = divided_diffs_left[1] + divided_diffs_left[2] * (4 * min(x) - 2 * selected_points_left[2][0])
    newton_sec_dir_right = divided_diffs_right[1] + divided_diffs_right[2] * (4 * max(x) - 2 * selected_points_right[2][0])
    
    spline_natural = Spline(table, 0, 0)
    spline_left_edge_newton = Spline(table, newton_sec_dir_left, 0)
    spline_both_edge_newton = Spline(table, newton_sec_dir_left, newton_sec_dir_right)
    
    new_x = np.linspace(min(x) - 0.5, max(x) + 0.5, 150)
    
    print("Сплайн с натуральными краевыми условиями: {:.3f}".format(spline_natural.aproximate_value(x_single)))
    print("Сплайн с краевыми условиями P''(x0) и 0: {:.3f}".format(spline_left_edge_newton.aproximate_value(x_single)))
    print("Сплайн с краевыми условиями P''(x0) и P''(xn): {:.3f}".format(spline_both_edge_newton.aproximate_value(x_single)))
    print("Полином Ньютона 3й степени: {:.3f}".format(approximate_newton(table, x_single, 3)))
    
    
    # fig_1, ax_1 = plt.subplots()
    # ax_1.plot(x, y, label='Исходная таблица')
    # ax_1.plot(new_x, [spline_natural.aproximate_value(i) for i in new_x], label='Сплайн (0, 0)')
    # ax_1.legend()
    # ax_1.grid()
    
    # fig_2, ax_2 = plt.subplots()
    # ax_2.plot(x, y, label='Исходная таблица')
    # ax_2.plot(new_x, [spline_left_edge_newton.aproximate_value(i) for i in new_x], label='Сплайн (P``(x0), 0)')
    # ax_2.legend()
    # ax_2.grid()
    
    # fig_3, ax_3 = plt.subplots()
    # ax_3.plot(x, y, label='Исходная таблица')
    # ax_3.plot(new_x, [spline_both_edge_newton.aproximate_value(i) for i in new_x], label='Сплайн (P``(x0), P``(xn))')
    # ax_3.legend()
    # ax_3.grid()
    
    # fig_4, ax_4 = plt.subplots()
    # ax_4.plot(x, y, label='Исходная таблица')
    # ax_4.plot(new_x, [approximate_newton(table, i, 3) for i in new_x], label='Полином Ньютона 3й степени')
    # ax_4.legend()
    # ax_4.grid() 
    
    
    fig_5, ax_5 = plt.subplots()
    ax_5.plot(x, y, label='Исходная таблица')
    ax_5.plot(new_x, [spline_natural.aproximate_value(i) for i in new_x], label='Сплайн (0, 0)')
    
    ax_5.plot(new_x, [spline_left_edge_newton.aproximate_value(i) for i in new_x], label='Сплайн (P``(x0), 0)')
    ax_5.plot(new_x, [spline_both_edge_newton.aproximate_value(i) for i in new_x], label='Сплайн (P``(x0), P``(xn))')
    ax_5.plot(new_x, [approximate_newton(table, i, 3) for i in new_x], label='Полином Ньютона 3й степени')
    
    ax_5.legend()
    ax_5.grid() 
    
    # fig_6, ax_6 = plt.subplots()
    # ax_6.plot(x, y, label='Исходная таблица')
    
    # ax_6.legend()
    # ax_6.grid() 
    
    
    plt.show()