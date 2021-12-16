import pandas as pd
import numpy as np

ess = pd.read_csv("ess.csv")

ess = ess.loc[ess["sclmeet"] <= 10, :].copy()
ess = ess.loc[ess["rlgdgr"] <= 10, :].copy()
ess = ess.loc[ess["hhmmb"] <= 50, :].copy()
ess = ess.loc[ess["netusoft"] <= 5, :].copy()
ess = ess.loc[ess["agea"] <= 200, :].copy()
ess = ess.loc[ess["health"] <= 5, :].copy()
ess = ess.loc[ess["happy"] <= 10, :].copy()
ess = ess.loc[ess["eduyrs"] <= 100, :].copy().reset_index(drop=True)

max_depth = 3


def get_split_point(all_values, predicted_values):
    lowest_error = float("inf")
    best_split_point = None
    best_lower_mean = np.mean(predicted_values)
    best_higher_mean = np.mean(predicted_values)

    for percentile in range(100):
        split_candidate = np.percentile(all_values, percentile)

        lower_outcomes = [
            outcome
            for value, outcome in zip(all_values, predicted_values)
            if value <= split_candidate
        ]
        higher_outcomes = [
            outcome
            for value, outcome in zip(all_values, predicted_values)
            if value > split_candidate
        ]

        if min(len(lower_outcomes), len(higher_outcomes)) > 0:
            lower_mean = np.mean(lower_outcomes)
            higher_mean = np.mean(higher_outcomes)

            lower_errors = [abs(outcome - lower_mean) for outcome in lower_outcomes]
            higher_errors = [abs(outcome - higher_mean) for outcome in higher_outcomes]

            total_error = sum(lower_errors) + sum(higher_errors)

            if total_error < lowest_error:
                best_split_point = split_candidate
                lowest_error = total_error
                best_lower_mean = lower_mean
                best_higher_mean = higher_mean

    return best_split_point, lowest_error, best_lower_mean, best_higher_mean


def get_split(depth, data, variables, outcome_variable):
    best_variable = ""
    lowest_error = float("inf")
    best_split_point = None
    predicted_values = list(data.loc[:, outcome_variable])
    best_lower_mean = -1
    best_higher_mean = -1

    for variable in variables:
        all_values = list(data.loc[:, variable])
        splitted = get_split_point(all_values, predicted_values)

        if splitted[1] < lowest_error:
            best_variable = variable
            best_split_point = splitted[0]
            lowest_error = splitted[1]
            best_lower_mean = splitted[2]
            best_higher_mean = splitted[3]

    generated_tree = [
        [best_variable, float("-inf"), best_split_point, []],
        [best_variable, best_split_point, float("inf"), []],
    ]

    if depth < max_depth:
        data1 = data.loc[data[best_variable] <= best_split_point, :]
        data2 = data.loc[data[best_variable] > best_split_point, :]

        if len(data1.index) > 10 and len(data2.index) > 10:
            generated_tree[0][3] = get_split(
                depth + 1, data1, variables, outcome_variable
            )
            generated_tree[1][3] = get_split(
                depth + 1, data2, variables, outcome_variable
            )
        else:
            depth = max_depth + 1
            generated_tree[0][3] = best_lower_mean
            generated_tree[1][3] = best_higher_mean
    else:
        generated_tree[0][3] = best_lower_mean
        generated_tree[1][3] = best_higher_mean

    return generated_tree


def get_prediction(observation, tree):
    j = 0

    while True:
        j += 1
        variable_to_check = tree[0][0]
        bound1 = tree[0][1]
        bound2 = tree[0][2]
        bound3 = tree[1][2]

        if observation.loc[variable_to_check] < bound2:
            tree = tree[0][3]
        else:
            tree = tree[1][3]

        if isinstance(tree, float):
            return tree
