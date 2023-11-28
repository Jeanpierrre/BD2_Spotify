import json
from Spotify.tf_idf import calculate_document_length, calculate_tfidf
import csv
import time
import os

idiomas_mapeados=['es','de','en','it','pt']

# Cargar el índice invertido para cada idioma
inverted_index={'es':{},'en':{},'it':{},'pt':{},'de':{}}
document_lengths={'es':{},'en':{},'it':{},'pt':{},'de':{}}
tfidf_data={'es':{},'en':{},'it':{},'pt':{},'de':{}}

# Realizar una consulta y retornar segun su scorecosine
def search(query, inverted_index, document_lengths, total_docs, tfidf_data, idioma, k):
    k = int(k)
    try:
        query_tokens = query.split()
        query_tfidf = {}
        for term in query_tokens:
            tfidf = calculate_tfidf(term, query_tokens, inverted_index[idioma], total_docs)
            query_tfidf[term] = tfidf

        query_length = calculate_document_length(query_tokens, inverted_index[idioma], total_docs)
        cosine_scores = {}
        for doc_id, doc_length in document_lengths[idioma].items():
            score = 0.0
            for term, tfidf in query_tfidf.items():
                if term in inverted_index[idioma]:
                    if doc_id in inverted_index[idioma][term]:
                        score += tfidf * tfidf_data[idioma][doc_id][term]
            score /= doc_length * query_length
            cosine_scores[doc_id] = score

        # Ordenar los documentos por puntaje coseno y retornar los 10 mejores
        results = sorted(cosine_scores.items(), key=lambda x: x[1], reverse=True)
        results = [x for x in results if x[1] != 0.0]
        results = results[:k]
        return results

    except Exception as e:
        return []

"""
# Cargar el índice invertido
with open('indice_invertido.json', 'r') as index_file:
    inverted_index = json.load(index_file)

# Cargar las longitudes de los documentos
with open('document_lengths.json', 'r') as lengths_file:
    document_lengths = json.load(lengths_file)

#cargar tfidf
with open('tfidf_data.json', 'r') as tfidf_file:
    tfidf_data = json.load(tfidf_file)
"""

for idioma in idiomas_mapeados:
    nombre_archivo_index = os.path.join('Spotify', idioma, 'indice_invertido.json')
    with open(nombre_archivo_index, 'r') as index_file:
        inverted_index[idioma]=json.load(index_file)

# Cargar las longitudes de los documentos
for idioma in idiomas_mapeados:
    #print("para el idioma : ",idioma)
    nombre_archivo = os.path.join('Spotify', idioma, 'document_lengths.json')
    with open(nombre_archivo, 'r') as lengths_file:
        document_lengths[idioma]=json.load(lengths_file)
       # print(document_lengths[idioma])

#cargar tfidf
for idioma in idiomas_mapeados:
    nombre_archivo = os.path.join('Spotify', idioma, 'tfidf_data.json')
    with open(nombre_archivo, 'r') as tfidf_file:
        tfidf_data[idioma]=json.load(tfidf_file)

# Ejemplo de consulta
# query = 'dont stop'
# results = search(query, inverted_index, document_lengths, 18455, tfidf_data,'en')
# print(results)
# print(len(results))

"""
def get_name(id):
    diccionario={}
    with open('Data/new_spotify.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['track_id'] == id:
                diccionario['track_id']=row['track_id']
                diccionario['lyrics']=row['lyrics']
                diccionario['track_name']=row['track_name']
                diccionario['track_artist']=row['track_artist']
                return diccionario
            
# Recibe y muestra a frontend
results = None
def for_user(query,idioma):
    s_time = time.time()
    results = search(query, inverted_index, document_lengths, 21, tfidf_data,idioma)
    e_time = time.time()
    exe_time = e_time - s_time

    product_names = [get_name(doc_id) for doc_id, _ in results] # Too much time
    return product_names, round(exe_time, 3)
"""

def cargar_datos():
    datos = {}
    with open('Data/new_spotify.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            datos[row['track_id']] = {
                'track_id': row['track_id'],
                'lyrics': row['lyrics'],
                'track_name': row['track_name'],
                'track_artist': row['track_artist']
            }
    return datos

def for_user(query, idioma, datos, k):
    s_time = time.time()
    results = search(query, inverted_index, document_lengths, 21, tfidf_data, idioma, k)
    e_time = time.time()
    exe_time = e_time - s_time

    product_names = [datos.get(doc_id, {}) for doc_id, _ in results]
    return product_names, round(exe_time, 3)