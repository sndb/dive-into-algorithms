import matplotlib.pyplot as plt


def next_random(previous, n1, n2, n3):
    return (previous * n1 + n2) % n3


def list_random(n1, n2, n3):
    output = [1]
    while len(output) <= n3:
        output += [next_random(output[-1], n1, n2, n3)]
    return output


def overlapping_sums(numbers, sum_length):
    numbers += numbers
    output = []

    for n in range(len(numbers)):
        output += [sum(numbers[n : (n + sum_length)])]

    return output


def feedback_shift(bits):
    xor_result = (bits[1] + bits[2]) % 2
    output = bits.pop()
    bits.insert(0, xor_result)
    return bits, output


def feedback_shift_list(bits_seed):
    bits_output = [bits_seed.copy()]
    random_output = []
    bits_next = bits_seed.copy()

    while len(bits_output) < 2 ** len(bits_seed):
        bits_next, next = feedback_shift(bits_next)
        bits_output += [bits_next.copy()]
        random_output += [next]

    return bits_output, random_output


def plot_hist():
    overlap = overlapping_sums(list_random(211111, 111112, 300007), 12)

    plt.hist(overlap, 2 ** 5, facecolor="blue", alpha=0.5)

    plt.title("Results of the Overlapping Sums Test")
    plt.xlabel("Sum of Elements of Overlapping Consecutive Sections of List")
    plt.ylabel("Frequency of Sum")

    plt.show()
