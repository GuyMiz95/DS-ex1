import csv
import math


def get_tf_td(document, term):
    tf_td = document.lower().count(term.lower())

    return tf_td


def tfidf(data, terms, documents_keys):
    # creating vars
    num_of_documents = len(data)

    # create dictionaries for storing calculated tf-idf data
    tf_td_dict = {term: {document: 0 for document in documents_keys} for term in terms}
    dfi_dict = {term: 0 for term in terms}
    idfi_dict = {term: 0 for term in terms}
    tf_idf_dict = {term: {document: 0 for document in documents_keys} for term in terms}
    # iterating input
    for i in range(len(data)):
        line = data[i]
        key = documents_keys[i]
        for term in terms:
            tf_td = get_tf_td(line, term)
            tf_td_dict[term][key] = tf_td
            # if found in doc - add
            dfi_dict[term] += int(tf_td > 0)
    for term in terms:
        idfi_dict[term] = math.log(num_of_documents / dfi_dict[term], 10)

    for key in documents_keys:
        for term in terms:
            tf_idf_dict[term][key] = tf_td_dict[term][key] * idfi_dict[term]
    return tf_idf_dict


if __name__ == '__main__':
    # initiate music festivals (a)
    festival_terms = ["annual", "music", "festival", "soul", "jazz", "Belgium", "Hungary", "Israel", "Rock", "dance",
             "Desert", "electronic", "arts"]

    with open('music_festivals.csv', mode='r', newline='') as f:
        _reader = csv.reader(f)
        _data = [row for row in _reader]
    _data = _data[1:]
    festival_descriptions = [line[-1] for line in _data]
    tfidf(festival_descriptions, festival_terms, [line[0] for line in _data])
