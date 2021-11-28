import matplotlib.pyplot as plt

temperature = lambda t: 1 / (t + 1)

xs = range(100)

plt.plot(xs, [temperature(t) for t in xs])

plt.title("The Temperature Function")
plt.xlabel("Time")
plt.ylabel("Temperature")

plt.show()
