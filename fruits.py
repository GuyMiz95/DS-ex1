import wikipedia
import csv
import json
from wikipedia import DisambiguationError

from tfidf import tfidf


def fruitcrawl():
    with open('fruits.csv', mode='r', newline='') as f:
        _reader = csv.reader(f)
        _data = [row for row in _reader]
    _data = _data[1:]
    for row in _data:
        fruit = row[0]
        fruit_page = get_fruit_page(fruit)
        with open(fruit + '.json', 'w') as f:
            json.dump(fruit_page.content, f)

def get_fruit_page(fruit):
    try:
        page = wikipedia.page(fruit + " (fruit)")
    except wikipedia.exceptions.PageError as e:
        try:
            page = wikipedia.page(fruit + " (plant)")
        except wikipedia.exceptions.DisambiguationError as e:
            page = wikipedia.page(fruit)
    return page


if __name__ == '__main__':
    festival_terms = ["annual", "music", "festival", "soul", "jazz", "Belgium", "Hungary", "Israel", "Rock", "dance",
             "Desert", "electronic", "arts"]

    with open('music_festivals.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        data = [row for row in reader]

    tfidf(data, festival_terms)

    fruitcrawl()