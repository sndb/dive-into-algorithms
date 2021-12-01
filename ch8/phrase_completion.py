from collections import Counter

import nltk
from nltk.util import ngrams
import requests


def search_suggestion(search_term, text):
    token = nltk.word_tokenize(text)
    grams = [ngrams(token, x) for x in range(2, 6)]

    split_term = tuple(search_term.split())
    counted_grams = Counter(grams[len(split_term) - 1])
    matching_terms = [cg for cg in counted_grams.items() if cg[0][:-1] == split_term]

    return (
        " ".join(max(matching_terms, key=lambda k: k[1])[0])
        if len(matching_terms) > 0
        else "No suggested searches"
    )


text = requests.get("http://www.bradfordtuckfield.com/shakespeare.txt").text.replace("\n", "")
print(search_suggestion("life is a", text))
