def merge(left, right):
    new_cabinet = []

    while min(len(left), len(right)) > 0:
        if left[0] < right[0]:
            new_cabinet.append(left.pop(0))
        else:
            new_cabinet.append(right.pop(0))

    return new_cabinet + left + right


def merge_sort(cabinet):
    if len(cabinet) == 1:
        return cabinet

    return merge(
        merge_sort(cabinet[: len(cabinet) // 2]),
        merge_sort(cabinet[len(cabinet) // 2 :]),
    )


cabinet = [4, 1, 3, 2, 6, 3, 18, 2, 9, 7, 3, 1, 2.5, -9]
new_cabinet = merge_sort(cabinet)
print(new_cabinet)
