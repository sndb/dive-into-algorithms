import pandas as pd


def russian_peasant_multiplication(n1, n2):
    halving = [n1]
    while halving[-1] > 1:
        halving += [halving[-1] // 2]

    doubling = [n2]
    while len(doubling) < len(halving):
        doubling += [doubling[-1] * 2]

    half_double = pd.DataFrame(zip(halving, doubling))
    half_double = half_double.loc[half_double[0] % 2 == 1, :]

    return sum(half_double.loc[:, 1])


def russian_peasant_multiplication_fp(n1, n2):
    halving, doubling = [n1], [n2]

    while halving[-1] > 1:
        halving += [halving[-1] // 2]
        doubling += [doubling[-1] * 2]

    return sum(x[1] for x in zip(halving, doubling) if x[0] % 2 == 1)


n1 = 89
n2 = 18
answer = russian_peasant_multiplication(n1, n2)
answer_fp = russian_peasant_multiplication_fp(n1, n2)

print(answer)
print(answer_fp)
