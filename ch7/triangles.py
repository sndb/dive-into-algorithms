import math

import numpy as np
import pylab as pl
from matplotlib import collections as mc


def points_to_triangle(p1, p2, p3):
    return (tuple(p1), tuple(p2), tuple(p3))


def generate_lines(points, itinerary):
    lines = []
    for i in range(len(itinerary) - 1):
        lines += [(points[itinerary[i]], points[itinerary[i + 1]])]
    return lines


def plot_triangle_simple(triangle, filename):
    fig, ax = pl.subplots()
    xs = [triangle[0][0], triangle[1][0], triangle[2][0]]
    ys = [triangle[0][1], triangle[1][1], triangle[2][1]]
    itinerary = [0, 1, 2, 0]
    lines = generate_lines(triangle, itinerary)

    lc = mc.LineCollection(lines, linewidths=2)

    ax.add_collection(lc)
    ax.margins(0.1)
    pl.scatter(xs, ys)

    pl.savefig(filename + ".png")
    pl.close()


def get_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def triangle_to_circumcenter(triangle):
    x, y, z = (
        complex(triangle[0][0], triangle[0][1]),
        complex(triangle[1][0], triangle[1][1]),
        complex(triangle[2][0], triangle[2][1]),
    )
    w = z - x
    w /= y - x
    c = (x - y) * (w - abs(w) ** 2) / 2j / w.imag - x
    radius = abs(c + x)
    return ((0 - c.real, 0 - c.imag), radius)


def plot_voronoi_diagram(triangles, centers, radii, filename):
    fig, ax = pl.subplots()
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])

    for i in range(len(triangles)):
        triangle = triangles[i]
        center = centers[i]
        radius = radii[i]
        xs = [triangle[0][0], triangle[1][0], triangle[2][0]]
        ys = [triangle[0][1], triangle[1][1], triangle[2][1]]
        itinerary = [0, 1, 2, 0]
        lines = generate_lines(triangle, itinerary)

        lc = mc.LineCollection(lines, linewidths=2)

        ax.add_collection(lc)
        ax.margins(0.1)
        pl.scatter(xs, ys)
        pl.scatter(center[0], center[1])

        circle = pl.Circle(center, radius, color="b", fill=False)

        ax.add_artist(circle)

    pl.savefig(filename + ".png")
    pl.close()


def generate_delaunay(points):
    delaunay = [points_to_triangle((-5, -5), (-5, 10), (10, -5))]

    for point_to_add in points:
        invalid_triangles = []
        for triangle in delaunay:
            circumcenter, radius = triangle_to_circumcenter(triangle)
            distance = get_distance(circumcenter, point_to_add)
            if distance < radius:
                invalid_triangles += [triangle]

        points_in_invalid = set()
        for triangle in invalid_triangles:
            delaunay.remove(triangle)
            for point in triangle:
                points_in_invalid.add(point)
        points_in_invalid = list(points_in_invalid)

        for i in range(len(points_in_invalid)):
            for j in range(i + 1, len(points_in_invalid)):
                count_occurrences = 0
                for triangle in invalid_triangles:
                    count_occurrences += (
                        1
                        * (points_in_invalid[i] in triangle)
                        * (points_in_invalid[j] in triangle)
                    )
                if count_occurrences == 1:
                    delaunay += [
                        points_to_triangle(
                            points_in_invalid[i], points_in_invalid[j], point_to_add
                        )
                    ]

    return delaunay


def plot_voronoi_diagram(
    triangles,
    centers,
    plot_circumcircles,
    plot_points,
    plot_triangles,
    plot_voronoi,
    plot_circumcenters,
    filename,
):
    fig, ax = pl.subplots()
    ax.set_xlim([-0.1, 1.1])
    ax.set_ylim([-0.1, 1.1])

    lines = []
    for i in range(len(triangles)):
        triangle = triangles[i]
        center = centers[i][0]
        radius = centers[i][1]
        xs = [triangle[0][0], triangle[1][0], triangle[2][0]]
        ys = [triangle[0][1], triangle[1][1], triangle[2][1]]
        itinerary = [0, 1, 2, 0]

        lc = mc.LineCollection(generate_lines(triangle, itinerary), linewidths=2)
        if plot_triangles:
            ax.add_collection(lc)
        if plot_points:
            pl.scatter(xs, ys)

        ax.margins(0.1)

        if plot_circumcenters:
            pl.scatter(center[0], center[1])

        circle = pl.Circle(center, radius, color="b", fill=False)
        if plot_circumcircles:
            ax.add_artist(circle)

        if plot_voronoi:
            for j in range(len(triangles)):
                common_points = 0
                for k in range(len(triangles[i])):
                    for n in range(len(triangles[j])):
                        if triangles[i][k] == triangles[j][n]:
                            common_points += 1
                if common_points == 2:
                    lines += [[centers[i][0], centers[j][0]]]

        lc = mc.LineCollection(lines, linewidths=1)
        ax.add_collection(lc)

    pl.savefig(filename + ".png")
    pl.close()


N = 15
np.random.seed(5201314)
xs = np.random.rand(N)
ys = np.random.rand(N)
points = list(zip(xs, ys))
delaunay = generate_delaunay(points)
circumcenters = []
for triangle in delaunay:
    circumcenters += [triangle_to_circumcenter(triangle)]
plot_voronoi_diagram(delaunay, circumcenters, False, True, False, True, False, "final")
