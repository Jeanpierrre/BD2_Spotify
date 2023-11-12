import json
#from spimi import spimi_invert_from_json
from tf_idf import calculate_tfidf, calculate_document_length
import os

idiomas_mapeados=['es','de','en','it','pt']
inverted_index={'es':{},'en':{},'it':{},'pt':{},'de':{}}


# Supongamos que tenemos los indices en las carpetas de cada idioma en el archivo indice_invertido.json


# Cargar el índice invertido por cada idioma

for idioma in idiomas_mapeados:
    nombre_archivo_index = os.path.join(idioma, 'indice_invertido.json')
    with open(nombre_archivo_index, 'r') as index_file:
        inverted_index[idioma]=json.load(index_file)




# Supongamos que tienes una estructura de datos que contiene los documentos y sus tokens (doc_tokens).
# Cargar los datos desde el archivo JSON
doc_tokens={
    'es':{},
    'en':{},
    'it':{},
    'pt':{},
    'de':{}
}


for idioma in idiomas_mapeados:
    nombre_archivo_tokens = os.path.join(idioma, 'archivo_procesado.json')
    with open(nombre_archivo_tokens, 'r') as json_file:
        doc_tokens[idioma]=json.load(json_file)


# Calcula los pesos TF-IDF y las longitudes de los documentos
tfidf_data = {
    'es':{},
    'en':{},
    'it':{},
    'pt':{},
    'de':{}
}
document_lengths = {
    'es':{},
    'en':{},
    'it':{},
    'pt':{},
    'de':{}
}
#total_docs = len(doc_tokens)


for idioma in idiomas_mapeados:
    for doc_id, tokens in doc_tokens[idioma].items():
        #print(tokens)
        total_docs=len(doc_tokens[idioma])
        tfidf_values = {}#inicializar
        doc_length = calculate_document_length(tokens, inverted_index[idioma], total_docs)
        #                       print("Idioma: ",idioma," len ",total_docs)
        for term in set(tokens):
            tfidf = calculate_tfidf(term, tokens, inverted_index[idioma], total_docs)
            tfidf_values[term] = tfidf
    #errorrrrrrr
        tfidf_data[idioma][doc_id] = tfidf_values
        document_lengths[idioma][doc_id] = doc_length



for idioma in idiomas_mapeados:
    nombre_archivo_tokens = os.path.join(idioma, 'archivo_procesado.json')
    with open(nombre_archivo_tokens, 'r') as json_file:
        doc_tokens[idioma]=json.load(json_file)
    

for idioma in idiomas_mapeados:
    nombre_archivo = os.path.join(idioma, 'tfidf_data.json')
    with open(nombre_archivo, 'w') as tfidf_file:
        json.dump(tfidf_data[idioma], tfidf_file, indent=4)
#
# Guardar los cálculos de TF-IDF en un archivo JSON
#with open('tfidf_data.json', 'w') as tfidf_file:
 #   json.dump(tfidf_data, tfidf_file, indent=4)

for idioma in idiomas_mapeados:
    nombre_archivo = os.path.join(idioma, 'document_lengths.json')
    with open(nombre_archivo, 'w') as lengths_file:
        json.dump(document_lengths[idioma], lengths_file, indent=4)

# Guardar las longitudes de documentos en un archivo JSON
#with open('document_lengths.json', 'w') as lengths_file:
 #   json.dump(document_lengths, lengths_file, indent=4)
