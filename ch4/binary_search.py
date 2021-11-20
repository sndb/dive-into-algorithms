import math


def binary_search(sorted_cabinet, looking_for):
    lower = 0
    upper = len(sorted_cabinet)
    guess = (upper + lower) // 2

    while abs(sorted_cabinet[guess] - looking_for) > 10 ** -4:
        if sorted_cabinet[guess] > looking_for:
            upper = guess
        elif sorted_cabinet[guess] < looking_for:
            lower = guess

        last_guess = guess
        guess = (upper + lower) // 2
        if guess == last_guess:
            raise KeyError

    return guess


def inverse_sin(number):
    precision = 10 ** 4
    domain = [x * math.pi / precision - math.pi / 2 for x in range(0, precision)]
    the_range = [math.sin(x) for x in domain]
    return domain[binary_search(the_range, number)]


print(binary_search([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 8))
try:
    binary_search([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 4.5)
except KeyError:
    print("As expected.")


print(inverse_sin(0.9))
print(math.asin(0.9))
