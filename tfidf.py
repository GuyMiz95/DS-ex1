import csv
import math

def get_tf_td(document, term):
    tf_td = document.lower().count(term.lower())

    return tf_td

def tfidf(data, terms):
    # creating vars
    data = data[1::]
    documents = [line[0] for line in data]
    num_of_documents = len(data)

    # create dictionaries for storing calculated tf-idf data
    tf_td_dict = {term: {document: 0 for document in documents} for term in terms}
    dfi_dict = {term : 0 for term in terms}
    idfi_dict = {term : 0 for term in terms}
    tf_idf_dict = {term: {document: 0 for document in documents} for term in terms}
    # iterating input
    for line in data:
        for term in terms:
            tf_td = get_tf_td(line[-1], term)
            tf_td_dict[term][line[0]] = tf_td
            # if found in doc - add
            dfi_dict[term] += int(tf_td > 0)
    for term in terms:
        idfi_dict[term] = math.log(num_of_documents / dfi_dict[term], 10)

    for line in data:
        for term in terms:
            tf_idf_dict[term][line[0]] = tf_td_dict[term][line[0]] * idfi_dict[term]
    return tf_idf_dict