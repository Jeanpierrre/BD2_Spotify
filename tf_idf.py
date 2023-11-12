import math

def calculate_tf(term, doc_tokens):

    tf = doc_tokens.count(term)
    #aplicamos logaritmo para suaavizar la frecuencia
    if tf > 0:
        tf = 1 + math.log(tf)

    return tf

def calculate_idf(term, inverted_index, total_docs):

    if term in inverted_index:
        doc_frequency = len(inverted_index[term])
        if doc_frequency > 0:
            idf = math.log(total_docs / doc_frequency)
            return idf
    return 0.0

def calculate_tfidf(term, doc_tokens, inverted_index, total_docs):

    tf = calculate_tf(term, doc_tokens)
    idf = calculate_idf(term, inverted_index, total_docs)
    tfidf = tf * idf
    return tfidf

def calculate_document_length(doc_tokens, inverted_index, total_docs):

    squared_sum = 0
    for term in set(doc_tokens):
        tfidf = calculate_tfidf(term, doc_tokens, inverted_index, total_docs)
        squared_sum += tfidf**2
    doc_length = math.sqrt(squared_sum)
    return doc_length
