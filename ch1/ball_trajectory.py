import matplotlib.pyplot as plt


def ball_trajectory_formula(x, v1, v2):
    return v2 / v1 * x + (-9.81 * x ** 2) / (2 * v1 ** 2)


def ball_trajectory(x):
    return ball_trajectory_formula(x, 0.99, 9.9)


xs = [x / 100 for x in range(201)]
ys = [ball_trajectory(x) for x in xs]

xs2 = [0.1, 2]
ys2 = [ball_trajectory(0.1), 0]
xs3 = [0.2, 2]
ys3 = [ball_trajectory(0.2), 0]
xs4 = [0.3, 2]
ys4 = [ball_trajectory(0.3), 0]
xs5 = [0.3, 0.3]
ys5 = [0, ball_trajectory(0.3)]
xs6 = [0.3, 2]
ys6 = [0, 0]

plt.title("The trajectory of a thrown ball (tangent calculation)")
plt.xlabel("Horizontal position of ball")
plt.ylabel("Vertical position of ball")
plt.text(0.31, ball_trajectory(0.3) / 2, "A", fontsize=16)
plt.text((0.3 + 2) / 2, 0.05, "B", fontsize=16)

plt.plot(
    xs,
    ys,
    # xs2, ys2, xs3, ys3,
    xs4,
    ys4,
    xs5,
    ys5,
    xs6,
    ys6,
)
plt.show()
