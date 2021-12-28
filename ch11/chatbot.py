import string

import nltk
import numpy as np
import pandas as pd
from scipy import spatial
from sklearn.feature_extraction.text import TfidfVectorizer


def stem_tokens(tokens):
    stemmer = nltk.stem.porter.PorterStemmer()
    return [stemmer.stem(token) for token in tokens]


def normalize(text):
    remove_punctuation_map = {ord(char): None for char in string.punctuation}
    return stem_tokens(
        nltk.word_tokenize(text.lower().translate(remove_punctuation_map))
    )


def chatbot(query, all_reports):
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 1), tokenizer=normalize, stop_words="english"
    )
    vectorizer.fit(all_reports)
    tfidf_reports = vectorizer.transform(all_reports).todense()
    tfidf_question = vectorizer.transform([query]).todense()
    row_similarities = [
        1 - spatial.distance.cosine(tfidf_report, tfidf_question)
        for tfidf_report in tfidf_reports
    ]
    return all_reports[np.argmax(row_similarities)]


all_documents = [
    "Chapter 1. The algorithmic approach to problem solving, including Galileo and baseball.",
    "Chapter 2. Algorithms in history, including magic squares, Russian peasant multiplication, and Egyptian methods.",
    "Chapter 3. Optimization, including maximization, minimization, and the gradient ascent algorithm.",
    "Chapter 4. Sorting and searching, including merge sort, and algorithm runtime.",
    "Chapter 5. Pure math, including algorithms for continued fractions and random numbers and other mathematical ideas.",
    "Chapter 6. More advanced optimization, including simulated annealing and how to use it to solve the traveling salesman problem.",
    "Chapter 7. Geometry, the postmaster problem, and Voronoi triangulations.",
    "Chapter 8. Language, including how to insert spaces and predict phrase completions.",
    "Chapter 9. Machine learning, focused on decision trees and how to predict happiness and heart attacks.",
    "Chapter 10. Artificial intelligence, and using the minimax algorithm to win at dots and boxes.",
    "Chapter 11. Where to go and what to study next, and how to build a chatbot.",
]

queries = [
    "I want to read about how to search for items.",
    "Please tell me which chapter I can go to if I want to read about mathematics algorithms.",
]

for query in queries:
    print(chatbot(query, all_documents))
