import math
import matplotlib.pyplot as plt


def income(education_years):
    return (
        math.sin((education_years - 10.6) * (2 * math.pi / 4))
        + (education_years - 11) / 2
    )


def income_derivative(education_years):
    return math.cos((education_years - 10.6) * (2 * math.pi / 4)) + 1 / 2


def gradient_ascent(current, step_size, threshold, maximum_iterations, derivative):
    for _ in range(maximum_iterations):
        change = step_size * derivative(current)
        current += change

        if abs(change) < threshold:
            break

    return current


xs = [11 + x / 100 for x in range(901)]
ys = [income(x) for x in xs]

plt.plot(xs, ys)

current_education = 12.5

plt.plot(current_education, income(current_education), "ro")

plt.title("Education and Income")
plt.xlabel("Years of Education")
plt.ylabel("Lifetime Income")

plt.show()


result = gradient_ascent(
    current_education,
    step_size=10 ** -3,
    threshold=10 ** -4,
    maximum_iterations=10 ** 5,
    derivative=income_derivative,
)

print(result)
