def gcd(x, y):
    larger = max(x, y)
    smaller = min(x, y)

    remainder = larger % smaller

    if remainder == 0:
        return smaller

    return gcd(smaller, remainder)


def gcd_concise(x, y):
    return y if (r := x % y) == 0 else gcd_concise(y, r)


print(gcd(105, 33))
print(gcd_concise(105, 33))
