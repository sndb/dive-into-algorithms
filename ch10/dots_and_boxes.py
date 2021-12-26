import matplotlib.pyplot as plt
from matplotlib import collections as mc
import numpy as np


def draw_lattice(n):
    for i, j in ((i, j) for i in range(1, n + 1) for j in range(1, n + 1)):
        plt.plot(i, j, "o", c="black")


def draw_game(n, filename, game):
    colors = ["red" if i % 2 == 0 else "blue" for i in range(len(game))]
    lc = mc.LineCollection(game, colors=colors, linewidths=2)
    fig, ax = plt.subplots()
    draw_lattice(n)
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)
    plt.savefig(filename)


def count_squares(game):
    return sum(
        line[0][1] == line[1][1]
        and [(line[0][0], line[0][1] - 1), (line[1][0], line[1][1] - 1)] in game
        and [(line[0][0], line[0][1]), (line[1][0] - 1, line[1][1] - 1)] in game
        and [(line[0][0] + 1, line[0][1]), (line[1][0], line[1][1] - 1)] in game
        for line in game
    )


def score(game):
    result = [0, 0]
    prev = 0
    for i, curr in [(i, count_squares(game[: i + 1])) for i in range(len(game))]:
        if curr > prev:
            result[0 if i % 2 == 0 else 1] += 1
        prev = curr
    return result


def generate_tree(possible_moves, depth, max_depth, game):
    tree = []

    for move in possible_moves:
        move_profile = [move]
        game_next = game.copy()
        game_next.append(move)
        move_profile.append(score(game_next))

        if depth < max_depth:
            possible_moves_next = possible_moves.copy()
            possible_moves_next.remove(move)
            move_profile.append(
                generate_tree(possible_moves_next, depth + 1, max_depth, game_next)
            )
        else:
            move_profile.append([])

        tree.append(move_profile)

    return tree


def minimax(max_or_min, tree):
    scores = []

    for move_profile in tree:
        if move_profile[2] == []:
            scores.append(move_profile[1][0] - move_profile[1][1])
        else:
            scores.append(minimax(-max_or_min, move_profile[2])[1])

    scores = [score * max_or_min for score in scores]
    best_score = max(scores)
    best_move = np.argmax(scores)

    return best_move, max_or_min * best_score


def possible_moves(game_size):
    moves = []

    for x in range(1, game_size + 1):
        for y in range(2, game_size + 1):
            moves.append([(x, y), (x, y - 1)])

    for x in range(1, game_size):
        for y in range(1, game_size + 1):
            moves.append([(x, y), (x + 1, y)])

    return moves


game = [
    [(1, 2), (1, 1)],
    [(3, 3), (4, 3)],
    [(1, 5), (2, 5)],
    [(1, 2), (2, 2)],
    [(2, 2), (2, 1)],
    [(1, 1), (2, 1)],
    [(3, 4), (3, 3)],
    [(3, 4), (4, 4)],
]
game_size = 5
all_posible = [move for move in possible_moves(game_size) if move not in game]
tree = generate_tree(all_posible, 0, 3, game)
move, _ = minimax(1, tree)

print(tree[move][0])
