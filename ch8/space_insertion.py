import re
import nltk


def insert_spaces(text, word_list):
    locs = list(
        {(m.start(), m.end()) for word in word_list for m in re.finditer(word, text)}
    )

    space_starts = [m.start() for m in re.finditer(" ", text)] + [-1] + [len(text)]
    space_starts.sort()

    space_starts_affine = [ss + 1 for ss in space_starts]
    space_starts.sort()

    partial_words = [
        loc
        for loc in locs
        if loc[0] in space_starts_affine and loc[1] not in space_starts
    ]
    partial_words_end = [
        loc
        for loc in locs
        if loc[0] not in space_starts_affine and loc[1] in space_starts
    ]

    between_spaces = [
        (space_starts[k] + 1, space_starts[k + 1]) for k in range(len(space_starts) - 1)
    ]
    between_spaces_invalid = [
        loc for loc in between_spaces if text[loc[0] : loc[1]] not in word_list
    ]

    new_text = text
    for loc in between_spaces_invalid:
        ends_of_beginnings = {
            loc2[1]
            for loc2 in partial_words
            if loc2[0] == loc[0] and (loc2[1] - loc[0]) > 1
        }
        beginnings_of_ends = {
            loc2[0]
            for loc2 in partial_words_end
            if loc2[1] == loc[1] and (loc2[1] - loc[0]) > 1
        }
        pivot = list(ends_of_beginnings & beginnings_of_ends)

        if len(pivot) > 0:
            pivot = min(pivot)
            new_text = new_text.replace(
                text[loc[0] : loc[1]], text[loc[0] : pivot] + " " + text[pivot : loc[1]]
            )

    new_text = new_text.replace("  ", " ")
    return new_text


nltk.download("brown")
from nltk.corpus import brown

word_list = list(set(brown.words()))
for c in "*[]?.+/;:,()":
    word_list = [word.replace(c, "") for word in word_list]

text = "The oneperfectly divine thing, the oneglimpse of God's paradisegiven on earth, is to fight a losingbattle - and notlose it."
print(insert_spaces(text, word_list))
