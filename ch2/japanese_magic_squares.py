import random
import math


luoshu = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]


def verify_square(square):
    sums = []

    row_sums = [sum(row) for row in square]
    sums.append(row_sums)

    column_sums = [sum(row[i] for row in square) for i in range(len(square))]
    sums.append(column_sums)

    main_diagonal = sum(square[i][i] for i in range(len(square)))
    sums.append([main_diagonal])

    anti_diagonal = sum(square[i][len(square) - 1 - i] for i in range(len(square)))
    sums.append([anti_diagonal])

    flattened = [j for i in sums for j in i]

    return len(set(flattened)) == 1


def print_square(square):
    labels = [f"[{x}]" for x in range(len(square))]
    format_row = "{:>6}" * (len(labels) + 1)
    print(format_row.format("", *labels))
    for label, row in zip(labels, square):
        print(format_row.format(label, *row))


def rule1(x, n, upright=False):
    return (x + (-1) ** upright * n) % n ** 2


def rule2(x, n, upleft=False):
    return (x + (-1) ** upleft) % n ** 2


def rule3(x, n, upleft=False):
    return (x + (-1) ** upleft * (-n + 1)) % n ** 2


def kurushimas_algorithm(n):
    square = [[float("nan") for _ in range(n)] for _ in range(n)]

    center_i = n // 2
    center_j = n // 2

    square[center_i][center_j] = (n ** 2 + 1) // 2
    square[center_i + 1][center_j] = 1
    square[center_i - 1][center_j] = n ** 2
    square[center_i][center_j + 1] = n ** 2 + 1 - n
    square[center_i][center_j - 1] = n

    return [
        [n ** 2 if x == 0 else x for x in row]
        for row in fill_square(
            fill_square(square, center_i, center_j, (n ** 2) / 2 - 4),
            center_i + 1,
            center_j,
            0,
        )
    ]


def fill_square(square, entry_i, entry_j, howfull):
    n = len(square)

    while sum(math.isnan(i) for row in square for i in row) > howfull:
        where_we_can_go = []

        if entry_i > 0 and entry_j > 0:
            where_we_can_go.append("up_left")
        if entry_i > 0 and entry_j < n - 1:
            where_we_can_go.append("up_right")
        if entry_i < n - 1 and entry_j > 0:
            where_we_can_go.append("down_left")
        if entry_i < n - 1 and entry_j < n - 1:
            where_we_can_go.append("down_right")

        where_to_go = random.choice(where_we_can_go)

        if where_to_go == "up_right":
            new_entry_i = entry_i - 1
            new_entry_j = entry_j + 1
            square[new_entry_i][new_entry_j] = rule1(square[entry_i][entry_j], n, True)

        elif where_to_go == "down_left":
            new_entry_i = entry_i + 1
            new_entry_j = entry_j - 1
            square[new_entry_i][new_entry_j] = rule1(square[entry_i][entry_j], n)

        elif where_to_go == "up_left" and entry_i + entry_j == n:
            new_entry_i = entry_i - 1
            new_entry_j = entry_j - 1
            square[new_entry_i][new_entry_j] = rule3(square[entry_i][entry_j], n, True)

        elif where_to_go == "down_right" and entry_i + entry_j == n - 2:
            new_entry_i = entry_i + 1
            new_entry_j = entry_j + 1
            square[new_entry_i][new_entry_j] = rule3(square[entry_i][entry_j], n)

        elif where_to_go == "up_left":
            new_entry_i = entry_i - 1
            new_entry_j = entry_j - 1
            square[new_entry_i][new_entry_j] = rule2(square[entry_i][entry_j], n, True)

        elif where_to_go == "down_right":
            new_entry_i = entry_i + 1
            new_entry_j = entry_j + 1
            square[new_entry_i][new_entry_j] = rule2(square[entry_i][entry_j], n)

        entry_i = new_entry_i
        entry_j = new_entry_j

    return square
