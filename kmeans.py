import csv


COLOR_IDX = 1
PEELING_IDX = 2
SEASON_IDX = 3

PRICE_IDX = 4
SUGAR_IDX = 5
TIME_IDX = 6


def kmeans(data):

    return


if __name__ == "__main__":
    # read from csv file #
    with open('fruits.csv', mode='r', newline='') as f:
        _reader = csv.reader(f)
        _data = [line for line in _reader]
    question_8d_data = [[line[PRICE_IDX], line[SUGAR_IDX], line[TIME_IDX]] for line in _data]
    print(question_8d_data)