import math

import wikipedia
import csv
import json
from wikipedia import DisambiguationError
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import re
from tfidf import tfidf


# nltk.download('punkt')
# nltk.download('stopwords')

def fruitcrawl(_data):
    # with open('fruits.csv', mode='r', newline='') as f:
    #     _reader = csv.reader(f)
    #     _data = [row for row in _reader]
    _data = _data[1:]
    bag_of_words = set()
    for row in _data:
        fruit = row[0]
        fruit_page = get_fruit_page(fruit)
        with open(fruit + '.json', 'w') as f:
            json.dump(fruit_page.content, f)
            # bag_of_words = bag_of_words.union(get_bag_of_words(fruit_page.content))
    # return bag_of_words


def get_fruit_page(fruit):
    try:
        page = wikipedia.page(fruit + " (fruit)")
    except wikipedia.exceptions.PageError as e:
        try:
            page = wikipedia.page(fruit + " (plant)")
        except wikipedia.exceptions.DisambiguationError as e:
            page = wikipedia.page(fruit)
    return page


def textsum(tfidf_table, data):
    return


def create_vectors(tfidf_table):
    sample_word = next(iter(tfidf_table.values()))
    all_indices = sample_word.keys()

    vectors = {idx: [] for idx in all_indices}

    for word in tfidf_table:
        for idx in all_indices:
            vectors[idx].append(tfidf_table[word].get(idx, 0))

    return vectors


def get_bag_of_words(content):
    # Tokenize the text into words
    words = word_tokenize(content.lower())

    # Convert the list of words into a set to get unique words
    unique_words = set([word for word in words if word.isalpha()])

    # Print the unique words
    return unique_words


def create_similarity_matrix(sentence_vectors):
    matrix = [[0 for _ in range(len(sentence_vectors))] for _ in range(len(sentence_vectors))]
    for row in range(len(sentence_vectors)):
        for col in range(len(sentence_vectors)):
            matrix[row][col] = calculate_similarity(sentence_vectors["idx" + str(row)],
                                                    sentence_vectors["idx" + str(col)])
    return matrix


def calculate_similarity(vector1, vector2):
    dot_product = calc_dot_product(vector1, vector2)
    norm_vector1 = math.sqrt(sum(v1 * v1 for v1 in vector1))
    norm_vector2 = math.sqrt(sum(v2 * v2 for v2 in vector2))
    return dot_product / (norm_vector1 * norm_vector2)


def calc_dot_product(vector1, vector2):
    dot_product = 0
    for i in range(len(vector1)):
        dot_product += vector1[i] * vector2[i]
    return dot_product


def get_highest_similarity_vector_index(similarity_matrix):
    max_similarity = 0
    max_similarity_index = 0
    for i in range(len(similarity_matrix)):
        if sum(similarity_matrix[i]) > max_similarity:
            max_similarity = sum(similarity_matrix[i])
            max_similarity_index = i
    return max_similarity_index


def find_top_k_similar_vectors(similarity_matrix, k=5):
    # Sum the similarities for each vector
    similarity_sums = [sum(row) for row in similarity_matrix]

    # Get the indices of the vectors sorted by their summed similarities in descending order
    sorted_indices = sorted(range(len(similarity_sums)), key=lambda i: similarity_sums[i], reverse=True)

    return sorted_indices[:k]


if __name__ == '__main__':
    # read from csv file #
    # with open('fruits.csv', mode='r', newline='') as f:
    #     _reader = csv.reader(f)
    #     _data = [line for line in _reader]

    # create json files for each fruit #
    # fruitcrawl(_data)

    # align fruits #
    # fruits = [line[0] for line in _data[1:]]

    # todo: 1) decide if opening json is outside or inside of textsum()
    # todo: 2) import code into textsum() (i think it should be operated per fruit and return a list of the 5 sentences)
    # todo: 3) eventually run on all fruits instead of just Banana and we're done with (b)
    fruits = ["Banana"]
    for fruit in fruits:
        with open(fruit + '.json', 'r') as f:
            cur_data = json.load(f)

        listed_data = sent_tokenize(cur_data)
        sent_index = ["idx" + str(i) for i in range(len(listed_data))]
        words_in_fruit = get_bag_of_words(cur_data)
        fruit_tfidf_score = tfidf(listed_data, words_in_fruit, sent_index)
        vectors = create_vectors(fruit_tfidf_score)
        similarity_matrix = create_similarity_matrix(vectors)
        best_vectors_indexes = find_top_k_similar_vectors(similarity_matrix)
        for index in best_vectors_indexes:
            print(listed_data[index])
