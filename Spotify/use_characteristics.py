import pickle

import numpy as np

import pandas as pd
from sklearn.preprocessing import StandardScaler

import os

from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances, manhattan_distances
from queue import PriorityQueue

from rtree import index
from sklearn.decomposition import PCA

import faiss

# //////////

# Cargar la lista desde el archivo .pkl
with open('Spotify/canciones.pkl', 'rb') as file:
    canciones_cargadas = pickle.load(file)

# //////////

# Cargar el archivo features.pkl con allow_pickle=True
# caractersiticas_Existentes = np.load('features.pkl', allow_pickle=True)
with open('Spotify/id_caracteristicas.txt', 'r', encoding='utf-8') as file:
    nombres_id = file.readlines()

# //////////

scaler = StandardScaler()
# Normalizar data
data_normalized = scaler.fit_transform(canciones_cargadas)

# ////////// - NEW FUNCTIONS FOR COMPATIBILITY

def search_id_characteristics(id_a_buscar):
    try:
        with open('Spotify/id_caracteristicas.txt', 'r') as file:
            for num, linea in enumerate(file, 1):
                if id_a_buscar in linea:
                    num = num - 1
                    return num  # Retorna el número de línea si se encuentra el ID
        return None  # Retorna None si el ID no se encuentra en ninguna línea
    except FileNotFoundError:
        print(f'Error: El archivo no fue encontrado.')
        return None
    
def extract_normalized(track_pos):
    return data_normalized[track_pos]

# ////////// - KNN PQ

def knn_search_priority_queue(query, k):
    # Hasta el de mejor resultados
    similarities = cosine_similarity(query.reshape(1, -1), data_normalized).flatten()
    
    # cola de prioridad
    priority_queue = PriorityQueue()
    for i, sim in enumerate(similarities):
        priority_queue.put((-sim, nombres_id[i]))  # por ser una cola para sacar los mejores(mas abajo ) desde abajo los metemos
    

    neighbors = []
    for _ in range(k):
        sim, neighbor = priority_queue.get()
        neighbors.append((neighbor, -sim))
    
    return neighbors

"""
k = 5
nueva_cancion_features =  data_normalized[3481]

knn_result_priority_queue = knn_search_priority_queue((nueva_cancion_features), k)
print("Vecinos más cercanos (KNN con cola de prioridad): ")

for i, data in knn_result_priority_queue:
    print(i,":" ,data)
"""
    
# ////////// - KNN RANGE SEARCH

def knn_range_search(query, k):
    radio = 50
    vecinos_en_radio = []

    for i, sample in enumerate(data_normalized):
        distancia = euclidean_distances(query.reshape(1, -1), sample.reshape(1, -1))[0][0]
        if distancia is not None and distancia <= radio:
            vecinos_en_radio.append((nombres_id[i], distancia))
    
    vecinos_en_radio = sorted(vecinos_en_radio, key=lambda x: x[1])
    vecinos_en_radio = vecinos_en_radio[:k]

    return vecinos_en_radio

"""
r = 10
rango = knn_range_search((nueva_cancion_features), r)
print(f"Vecinos más cercanos (range search):")
for i, data in rango:
    print(i, data)
"""

# ////////// - KNN SEQ

def knn_sequential(query, k):
    distances = []
    for sample in data_normalized:
        distance = euclidean_distances(query.reshape(1, -1), sample.reshape(1, -1))[0][0]
        distances.append(distance)
    
    indices = np.argsort(distances)[:k]#indices de manera ascendendete
    
    neighbors = []
    for index in indices:
        neighbors.append((nombres_id[index], distances[index]))
    
    return neighbors

# ////////// - R TREE

matrices_array = np.array(data_normalized)
# Número de dimensiones deseadas después de PCA
n_dimensions = 100
# Crear un objeto PCA
pca = PCA(n_components=n_dimensions)
# Aplicar PCA a las matrices
matrices_reduced = pca.fit_transform(matrices_array)

p = index.Property()
p.dimension = 100
p.buffering_capacity = 8
idx = index.Index(properties=p)

def init_rtree():
    for i, sample in enumerate(matrices_reduced):
        idx.insert(i, sample)

def knn_rtree(query, k):
    nearest_neighbors_indices = list(idx.nearest((matrices_reduced[query]), k))
    return nearest_neighbors_indices

def find_for_rtree(lista):
    out = []
    for i in lista:
        out.append(nombres_id[i])
    return out

# ////////// - BY USING FAISS

def train_index_HNSWFlat(data):
    # Inicializa el índice de FAISS con HNSW (Hierarchical Navigable Small World)
    M = 32  # Número de vecinos en la lista de entrada
    efConstruction = 100  # explorar al construir canciones mientras mayor es mejor la precision y mas demora
    dimension = 1000  # Dimensión de tus características
    quantizer = faiss.IndexHNSWFlat(dimension, M, faiss.METRIC_L2)#distancia eulediana
    quantizer.hnsw.efConstruction = efConstruction
    index = quantizer
    index.add(data)
    return index

"""
Sí, eso es correcto. En el contexto del índice HNSW con el parámetro M establecido en 32, cada punto (en este caso, cada canción) 
está directamente conectado a un máximo de 32 puntos en su lista de entrada. Estos son sus "vecinos cercanos" en el espacio de características.
"""
"""
En otras palabras, cada canción en tu conjunto de datos tiene conexiones directas con hasta M 
canciones más cercanas según la métrica de distancia especificada (en este caso, la distancia L2).
"""

# Entrenamiento con IndexHNSWFlat
index_train = train_index_HNSWFlat(data_normalized)

def knn_faiss_HNSWFlat(query_object, k):
    distances, indices = index_train.search(np.expand_dims(query_object, axis=0), k)
    resultados = []
    for i in range(k):
        distancia = distances[0][i]
        etiqueta = nombres_id[indices[0][i]]
        resultados.append((distancia, etiqueta))
    return resultados

"""
query_example = nueva_cancion_features
k_result = knn_faiss_HNSWFlat(index_train, query_example, 5)
print(len(k_result))

print("Resultados de búsqueda KNN con FAISS (IndexHNSWFlat):")
for a, i in k_result:
    print(f"Distancia: {a}, Etiqueta: {i}")
"""