def read_table() -> list:
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


def divided_diff(table: list) -> list:
    temp = [[0 * len(table)] for i in range(len(table))]
    for i in range(len(table)):
        temp[i][0] = table[i][1]

    for i in range(1, len(table)):
        for j in range(1, len(table) - i):
            temp[i][j] = (temp[i - 1][j - 1] - temp[i - 1][j]) / (table[i + j][0])


def approximate_newton(table: list, n: int, x: float) -> float:
    position = 0
    while position < len(table) - 1 and x < table[position + 1]:
        position += 1


def main() -> int:
    print("Введите x, y, y` через пробел, для окончания ввода введите '~': ")
    table = read_table()

    if not table:
        print("Ошибка ввода")
        return

    n = input('Введите n: ')
    if not n.isdigit():
        print("Ошибка ввода")
        return
    n = int(n)

    x = input('Введите х: ')
    try:
        x = float(x)
    except:
        print('Ошибка ввода')
        return


if __name__ == '__main__':
    main()
