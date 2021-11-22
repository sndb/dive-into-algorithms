import math


def continued_fraction(x, y, length_tolerance):
    output = []
    big, small = max(x, y), min(x, y)

    while small > 0 and len(output) < length_tolerance:
        quotient = big // small
        output += [quotient]
        big, small = small, big % small

    return output


def continued_fraction_decimal(x, error_tolerance, length_tolerance):
    output = []

    first_term = int(x)
    leftover = x - first_term
    output.append(first_term)
    error = leftover

    while error > error_tolerance and len(output) < length_tolerance:
        next_term = math.floor(1 / leftover)
        leftover = 1 / leftover - next_term
        output.append(next_term)
        error = abs(get_number(output) - x)

    return output


def get_number(continued_fraction):
    i = -1
    number = continued_fraction[i]

    while abs(i) < len(continued_fraction):
        next = continued_fraction[i - 1]
        number = 1 / number + next
        i -= 1

    return number


print(to_check := continued_fraction(105, 33, 10))
print(get_number(to_check))

print(continued_fraction_decimal(1.4142135623730951, 10 ** -5, 100))
