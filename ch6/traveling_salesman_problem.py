import math

import matplotlib.collections as mc
import matplotlib.pylab as pl
import numpy as np


def generate_lines(cities, itinerary):
    # only in python 3.10
    # from itertools import pairwise
    # return [(cities[x], cities[y]) for x, y in pairwise(itinerary)]

    lines = []
    for i in range(len(itinerary) - 1):
        lines += [(cities[itinerary[i]], cities[itinerary[i + 1]])]
    return lines


def how_far(lines):
    distance = 0
    for l in lines:
        distance += math.sqrt((l[0][0] - l[1][0]) ** 2 + (l[0][1] - l[1][1]) ** 2)
    return distance


def plot_itinerary(cities, itinerary, plot_title, filename):
    lc = mc.LineCollection(generate_lines(cities, itinerary), linewidths=2)
    fig, ax = pl.subplots()
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)
    pl.scatter(x, y)
    pl.title(plot_title)
    pl.xlabel("X Coordinate")
    pl.ylabel("y Coordinate")
    pl.savefig(filename + ".png")
    pl.close()


def find_nearest(cities, i, visited):
    point = cities[i]
    min_distance = math.inf
    min_i = -1

    for j, city in enumerate(cities):
        distance = math.sqrt((point[0] - city[0]) ** 2 + (point[1] - city[1]) ** 2)
        if distance < min_distance and distance > 0 and j not in visited:
            min_distance = distance
            min_i = j

    return min_i


def do_nearest_neighbor(cities, n):
    itinerary = [0]
    for _ in range(n - 1):
        itinerary += [find_nearest(cities, itinerary[-1], itinerary)]
    return itinerary


def perturb(cities, itinerary):
    i1 = int(np.random.rand() * len(itinerary))
    i2 = int(np.random.rand() * len(itinerary))

    itinerary2 = itinerary.copy()

    itinerary2[i1] = itinerary[i2]
    itinerary2[i2] = itinerary[i1]

    d1 = how_far(generate_lines(cities, itinerary))
    d2 = how_far(generate_lines(cities, itinerary2))

    return itinerary.copy() if d1 < d2 else itinerary2.copy()


def perturb_simulated_annealing(cities, itinerary, time):
    i1 = int(np.random.rand() * len(itinerary))
    i2 = int(np.random.rand() * len(itinerary))

    itinerary2 = itinerary.copy()

    itinerary2[i1] = itinerary[i2]
    itinerary2[i2] = itinerary[i1]

    d1 = how_far(generate_lines(cities, itinerary))
    d2 = how_far(generate_lines(cities, itinerary2))

    temperature = 1 / ((time / 1000) + 1)
    accept_worse = np.random.rand() < temperature

    if (d2 > d1 and accept_worse) or (d1 > d2):
        return itinerary2.copy()
    return itinerary.copy()


def perturb_simulated_annealing_2(cities, itinerary, time):
    i1 = int(np.random.rand() * len(itinerary))
    i2 = int(np.random.rand() * len(itinerary))

    itinerary2 = itinerary.copy()

    small, big = min(i1, i2), max(i1, i2)

    if (r := np.random.rand()) >= 0.55:
        itinerary2[small:big] = itinerary2[small:big][::-1]
    elif r < 0.45:
        del itinerary2[small:big]
        j = int(np.random.rand() * len(itinerary2))
        itinerary2 = itinerary2[:j] + itinerary[small:big] + itinerary2[j:]
    else:
        itinerary2[i1] = itinerary[i2]
        itinerary2[i2] = itinerary[i1]

    d1 = how_far(generate_lines(cities, itinerary))
    d2 = how_far(generate_lines(cities, itinerary2))

    temperature = 1 / ((time / 1000) + 1)
    accept_worse = np.random.rand() < temperature

    if (d2 > d1 and accept_worse) or (d1 > d2):
        return itinerary2.copy()
    return itinerary.copy()


def perturb_simulated_annealing_3(cities, itinerary, time, total):
    global min_distance
    global min_itinerary
    global min_index

    i1 = int(np.random.rand() * len(itinerary))
    i2 = int(np.random.rand() * len(itinerary))

    itinerary2 = itinerary.copy()

    small, big = min(i1, i2), max(i1, i2)
    r = np.random.rand()
    if r >= 0.55:
        itinerary2[small:big] = itinerary2[small:big][::-1]
    elif r < 0.45:
        del itinerary2[small:big]
        j = int(np.random.rand() * len(itinerary2))
        itinerary2 = itinerary2[:j] + itinerary[small:big] + itinerary2[j:]
    else:
        itinerary2[i1] = itinerary[i2]
        itinerary2[i2] = itinerary[i1]

    d1 = how_far(generate_lines(cities, itinerary))
    d2 = how_far(generate_lines(cities, itinerary2))

    scale = 3.5
    temperature = 1 / (time / (total / 10) + 1)
    accept_worse = np.random.rand() < math.exp(scale * (d1 - d2)) * temperature

    result = (
        itinerary2.copy()
        if (d2 > d1 and accept_worse) or (d1 > d2)
        else itinerary.copy()
    )

    reset = True
    reset_threshold = 0.04
    if reset and (time - min_index) > (total * reset_threshold):
        result = min_itinerary
        min_index = time

    d = how_far(generate_lines(cities, result))
    if d < min_distance:
        min_distance = d
        min_itinerary = result
        min_index = time

    if abs(time - total) <= 1:
        result = min_itinerary.copy()

    return result


def simulated_annealing(cities, itinerary):
    global min_distance
    global min_itinerary
    global min_index

    min_distance = how_far(generate_lines(cities, itinerary))
    min_itinerary = itinerary
    min_index = 0

    total = len(itinerary) * 50000
    for i in range(total):
        itinerary = perturb_simulated_annealing_3(cities, itinerary, i, total)

    return itinerary


def main():
    run_perturb = False

    np.random.seed(1729)

    N = 40
    x = np.random.rand(N)
    y = np.random.rand(N)

    cities = list(zip(x, y))

    random_itinerary = list(range(N))
    print(how_far(generate_lines(cities, random_itinerary)))

    nearest_neighbor_itinerary = do_nearest_neighbor(cities, N)
    print(how_far(generate_lines(cities, nearest_neighbor_itinerary)))

    if run_perturb:
        perturb_itinerary = random_itinerary.copy()
        for _ in range(len(perturb_itinerary) * 50000):
            perturb_itinerary = perturb(cities, perturb_itinerary)
        print(how_far(generate_lines(cities, perturb_itinerary)))

    simulated_annealing_itinerary = simulated_annealing(cities, random_itinerary.copy())
    print(how_far(generate_lines(cities, simulated_annealing_itinerary)))


if __name__ == "__main__":
    main()
