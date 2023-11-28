import json
from Styles.tf_idf import calculate_document_length, calculate_tfidf
import csv
import time

#realizar una consulta y retornar segun su scorecosine
def search(query, inverted_index, document_lengths, total_docs, tfidf_data, topk):
    topk = int(topk)
    query_tokens = query.split()
    query_tfidf = {term: calculate_tfidf(term, query_tokens, inverted_index, total_docs) for term in query_tokens}
    query_length = calculate_document_length(query_tokens, inverted_index, total_docs)
    
    # Obtener los documentos que contienen al menos uno de los términos de la consulta
    relevant_docs = set(doc_id for term in query_tfidf for doc_id in inverted_index.get(term, {}))
    cosine_scores = {}
    for doc_id in relevant_docs:
        score = sum(query_tfidf[term] * tfidf_data[doc_id].get(term, 0) for term in query_tfidf)
        score /= document_lengths[doc_id] * query_length
        cosine_scores[doc_id] = score

    # Ordenar los documentos por puntaje coseno y retornar los 10 mejores, no incluir si tiene el score 0
    results = [(doc_id, score) for doc_id, score in sorted(cosine_scores.items(), key=lambda x: x[1], reverse=True) if score > 0][:topk]
    return results

# Cargar el índice invertido
with open('Styles/indice_invertido.json', 'r') as index_file:
    inverted_index = json.load(index_file)

# Cargar las longitudes de los documentos
with open('Styles/document_lengths.json', 'r') as lengths_file:
    document_lengths = json.load(lengths_file)

# Cargar tfidf
with open('Styles/tfidf_data.json', 'r') as tfidf_file:
    tfidf_data = json.load(tfidf_file)

#print(tfidf_data['15970']['casual'])
# Ejemplo de consulta
# query = 'casual'
# results = search(query, inverted_index, document_lengths, 44424, tfidf_data)
# retornar el nombre del articulo

def get_name(id):
    with open('Data/styleslimpio.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['id'] == id:
                return row['productDisplayName']

# Recibe y muestra a frontend
results = None
def for_user_index(query, k):
    s_time = time.time()
    results = search(query, inverted_index, document_lengths, 44424, tfidf_data, k)
    e_time = time.time()
    exe_time = e_time - s_time

    # product_names = [(doc_id, get_name(doc_id)) for doc_id, _ in results]
    product_names = [get_name(doc_id) for doc_id, _ in results]
    product_ids = [doc_id for doc_id, _ in results]
    
    return product_names, product_ids, round(exe_time, 3)
