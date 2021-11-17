import math
import matplotlib.pyplot as plt


def revenue(tax):
    return 100 * (math.log(tax + 1) - (tax - 0.2) ** 2 + 0.04)


def revenue_flipped(tax):
    return -revenue(tax)


def revenue_derivative(tax):
    return 100 * (1 / (tax + 1) - 2 * (tax - 0.2))


def revenue_derivative_flipped(tax):
    return -revenue_derivative(tax)


def gradient_ascent(current, step_size, threshold, max_iterations, derivative):
    for _ in range(max_iterations):
        change = step_size * derivative(current)
        current += change

        if abs(change) < threshold:
            break

    return current


def gradient_descent(current, step_size, threshold, max_iterations, derivative):
    for _ in range(max_iterations):
        change = step_size * derivative(current)
        current -= change

        if abs(change) < threshold:
            break

    return current


def get_optimal_rate(current_rate):
    return gradient_ascent(
        current_rate,
        step_size=10 ** -3,
        threshold=10 ** -4,
        max_iterations=10 ** 5,
        derivative=revenue_derivative,
    )


def plot_curve():
    xs = [x / 1000 for x in range(1001)]
    ys = [revenue(x) for x in xs]
    current_rate = 0.7
    optimal_rate = get_optimal_rate(current_rate)

    plt.plot(xs, ys)

    plt.plot(current_rate, revenue(current_rate), "ro")
    plt.plot(optimal_rate, revenue(optimal_rate), "go")

    plt.title("Tax Rates and Revenue")
    plt.xlabel("Tax Rate")
    plt.ylabel("Revenue")

    plt.show()


def plot_flipped_curve():
    xs = [x / 1000 for x in range(1001)]
    ys = [revenue_flipped(x) for x in xs]

    plt.plot(xs, ys)

    plt.title("The Tax/Revenue Curve - Flipped")
    plt.xlabel("Tax Rate")
    plt.ylabel("Revenue - Flipped")

    plt.show()


print(f"Optimal rate: {get_optimal_rate(0.7):.3}")
