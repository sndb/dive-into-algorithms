import math


def square_root(x, y, error_tolerance):
    while True:
        z = x / y
        y = (y + z) / 2
        if y ** 2 - x < error_tolerance:
            break
    return y


print(square_root(5, 1, 10 ** -15))
print(math.sqrt(5))
