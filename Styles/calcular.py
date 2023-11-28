import json
from spimi import spimi_invert_from_json
from tf_idf import calculate_tfidf, calculate_document_length

# Supongamos que ya tienes el índice invertido construido y guardado en 'inverted_index.json'.
# Cargar el índice invertido
with open('indice_invertido.json', 'r') as index_file:
    inverted_index = json.load(index_file)

# Supongamos que tienes una estructura de datos que contiene los documentos y sus tokens (doc_tokens).
# Cargar los datos desde el archivo JSONw
with open('archivo_procesado.json', 'r') as json_file:
    doc_tokens = json.load(json_file)

# Calcula los pesos TF-IDF y las longitudes de los documentos
tfidf_data = {}
document_lengths = {}
total_docs = len(doc_tokens)

for doc_id, tokens in doc_tokens.items():
    tfidf_values = {}
    doc_length = calculate_document_length(tokens, inverted_index, total_docs)

    for term in set(tokens):
        tfidf = calculate_tfidf(term, tokens, inverted_index, total_docs)
        tfidf_values[term] = tfidf
    tfidf_data[doc_id] = tfidf_values
    document_lengths[doc_id] = doc_length

# Guardar los cálculos de TF-IDF en un archivo JSON
with open('tfidf_data.json', 'w') as tfidf_file:
    json.dump(tfidf_data, tfidf_file, indent=4)

# Guardar las longitudes de documentos en un archivo JSON
with open('document_lengths.json', 'w') as lengths_file:
    json.dump(document_lengths, lengths_file, indent=4)
