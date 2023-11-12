import json
from tf_idf import calculate_document_length, calculate_tfidf
import csv
import time
import os
#idiomas
idiomas_mapeados=['es','de','en','it','pt']

inverted_index={'es':{},'en':{},'it':{},'pt':{},'de':{}}
document_lengths={'es':{},'en':{},'it':{},'pt':{},'de':{}}
tfidf_data={'es':{},'en':{},'it':{},'pt':{},'de':{}}
# Cargar el índice invertido por cada idioma






#realizar una consulta y retornar segun su scorecosine
def search(query, inverted_index, document_lengths, total_docs, tfidf_data, idioma):
    try:
        #print("documentos de : ",document_lengths[idioma])

        query_tokens = query.split()
        #print(query_tokens)
        query_tfidf = {}
        for term in query_tokens:
            tfidf = calculate_tfidf(term, query_tokens, inverted_index[idioma], total_docs)
            #print("term: ",term,"  ","tfidf: ",tfidf)
            query_tfidf[term] = tfidf

        query_length = calculate_document_length(query_tokens, inverted_index[idioma], total_docs)
        #print(query_length)
        cosine_scores = {}
        for doc_id, doc_length in document_lengths[idioma].items():
            #print("Doc_id: ",doc_id)
            score = 0.0
            for term, tfidf in query_tfidf.items():
                if term in inverted_index[idioma]:
                    if doc_id in inverted_index[idioma][term]:
                        score += tfidf * tfidf_data[idioma][doc_id][term]
            score /= doc_length * query_length
            cosine_scores[doc_id] = score
        #print(cosine_scores)
        # Ordenar los documentos por puntaje coseno y retornar los 10 mejores
        results = sorted(cosine_scores.items(), key=lambda x: x[1], reverse=True)#[:10]
        results = [x for x in results if x[1] != 0.0]
        #-1 similitud perfecta pero en direcciones opuestas
        #similitud perfecta

        return results

    except Exception as e:
        # Manejar la excepción aquí, por ejemplo, imprimir el mensaje de error
       # print("Error:", e)
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
#print(tfidf_data['15970']['casual'])

for idioma in idiomas_mapeados:
    nombre_archivo_index = os.path.join(idioma, 'indice_invertido.json')
    with open(nombre_archivo_index, 'r') as index_file:
        inverted_index[idioma]=json.load(index_file)
        #print("para el idioma : ",idioma," index: ",inverted_index[idioma])


# Cargar las longitudes de los documentos
for idioma in idiomas_mapeados:
    #print("para el idioma : ",idioma)
    nombre_archivo = os.path.join(idioma, 'document_lengths.json')
    with open(nombre_archivo, 'r') as lengths_file:
        document_lengths[idioma]=json.load(lengths_file)
       # print(document_lengths[idioma])

#cargar tfidf
for idioma in idiomas_mapeados:
    nombre_archivo = os.path.join(idioma, 'tfidf_data.json')
    with open(nombre_archivo, 'r') as tfidf_file:
        tfidf_data[idioma]=json.load(tfidf_file)
#print(inverted_index['en'])

# Ejemplo de consulta

query = 'girl'
results = search(query, inverted_index, document_lengths, 18455, tfidf_data,'en')
print(results)
print(len(results))

#retornar el nombre del articulo
def get_name(id):
    diccionario={}
    with open('new_spotify.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['track_id'] == id:
                #return row['lyrics']
                diccionario['track_id']=row['track_id']
                diccionario['lyrics']=row['lyrics']
                diccionario['track_name']=row['track_name']
                diccionario['track_artist']=row['track_artist']
                return diccionario             
               

# Recibe y muestra a frontend
#results = None
def for_user(query,idioma):
    print("IDIOMA: ",idioma)
    s_time = time.time()
    results = search(query, inverted_index, document_lengths, 21, tfidf_data,idioma)
    e_time = time.time()
    exe_time = e_time - s_time

    product_names = [get_name(doc_id) for doc_id, _ in results]
    return product_names, round(exe_time, 3)

"""#imprimir los resultados
for doc_id, score in results:
    print("------------------------------------------------")
    print(f'{get_name(doc_id)} - {score}')
    print("------------------------------------------------")
    print('\n')"""

