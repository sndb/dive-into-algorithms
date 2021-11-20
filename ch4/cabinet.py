import math
import random
from timeit import default_timer as timer

import matplotlib.pyplot as plt
import numpy as np

step_counter = 0


def insert_cabinet(cabinet, to_insert):
    global step_counter

    check_location = len(cabinet) - 1
    insert_location = 0

    while check_location >= 0:
        step_counter += 1

        if to_insert > cabinet[check_location]:
            insert_location = check_location + 1
            break
        check_location -= 1

    step_counter += 1

    cabinet.insert(insert_location, to_insert)
    return cabinet


def insertion_sort(cabinet):
    global step_counter

    new_cabinet = []

    while len(cabinet) > 0:
        step_counter += 1

        to_insert = cabinet.pop(0)
        new_cabinet = insert_cabinet(new_cabinet, to_insert)

    return new_cabinet


def check_steps(size_of_cabinet):
    global step_counter
    step_counter = 0

    unsorted_cabinet = [random.randint(0, 1000) for _ in range(size_of_cabinet)]
    insertion_sort(unsorted_cabinet)

    return step_counter


def check_time():
    start = timer()

    unsorted_cabinet = [8, 4, 6, 1, 2, 5, 3, 7]
    sorted_cabinet = insertion_sort(unsorted_cabinet)

    end = timer()

    print(sorted_cabinet)
    print(end - start)
    print(step_counter)


xs = list(range(1, 100))
ys = [check_steps(x) for x in xs]
ys_exp = [math.exp(x) for x in xs]
ys_threehalves = [x ** 1.5 for x in xs]
ys_squared = [x ** 2 for x in xs]
ys_cubed = [x ** 3 for x in xs]

plt.plot(xs, ys)

axes = plt.gca()
axes.set_ylim([np.min(ys), np.max(ys) + 140])

plt.plot(xs, ys_exp)
plt.plot(xs, xs)
plt.plot(xs, ys_threehalves)
plt.plot(xs, ys_squared)
plt.plot(xs, ys_cubed)

plt.title("Comparing Insertion Sort to Other Growth Rates")
plt.xlabel("Number of Files in Random Cabinet")
plt.ylabel("Steps Required to Sort Cabinet by Insertion Sort")

plt.show()
