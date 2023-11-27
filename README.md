# Proyecto 3 - Bases de Datos 

Jean Pierre Sotomayor Cavero   100%

Angel Mucha Huaman             100%

Juan Torres                    100%

## Introducción
La exploración y extracción de información en documentos de texto involucra un proceso algorítmico fascinante y, en ciertos aspectos, intrincado. En la actualidad, se dispone de una amplia gama de técnicas y algoritmos diseñados para llevar a cabo búsquedas en archivos textuales, priorizando la precisión y la eficiencia. En este contexto, nos sumergiremos en la aplicación del método de indexación invertida para la búsqueda de textos en el conjunto de datos de ArXiv, una plataforma de distribución de archivos de código abierto.

## Objetivo
Este proyecto se centra en la óptima construcción de un índice invertido para facilitar tareas de búsqueda y recuperación en documentos de texto. Implicará el desarrollo de un sistema backend-frontend, utilizando código en Python para el backend y una interfaz gráfica de usuario (GUI) intuitiva como frontend. El objetivo primordial consistirá en comparar el rendimiento computacional de nuestra propia implementación del índice invertido con la de los sistemas de gestión de bases de datos PostgreSQL. La GUI resultante permitirá visualizar los resultados en los tres escenarios, y a partir de estos datos, se llevará a cabo un análisis de los tiempos de ejecución para evaluar la eficiencia de nuestro índice invertido.

### Descripción del dominio de datos
El conjunto de datos disponible en (https://www.kaggle.com/datasets/imuhammad/audio-features-and-lyrics-of-spotify-songs) contiene una amplia variedad de información sobre más de 18,000 canciones de Spotify, que incluye detalles como el artista, álbum, características de audio (por ejemplo, volumen), letras, el idioma de las letras, géneros y subgéneros.

Inicialmente, el conjunto de datos original fue utilizado en la tercera semana del proyecto TidyTuesday y solo comprendía características de audio y géneros. Para enriquecer la información, se agregaron las letras a través de la biblioteca Genius en R, y se incorporó el idioma de las letras utilizando la biblioteca langdetect en Python. Sin embargo, es importante tener en cuenta que aproximadamente solo la mitad de las canciones originales se encuentran disponibles en este conjunto de datos, ya que las letras no pudieron recuperarse para muchas de ellas.



### Extracción de características
Para este proyecto, es escencial tener las caracteristicas de una canciones, ya que con esto podemos reconocer canciones parecidas gracias los siguientes caractersiticas:  
#### MFCC (Coeficientes Cepstrales de Frecuencia Mel)  
Representa la forma en que el oído humano percibe diferentes frecuencias.  
Se calculan 20 coeficientes de MFCC a partir de la señal de audio, estos sirven para captura características fundamentales de la señal relacionadas con la percepción auditiva.  

```python
        chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
```
#### Cromagrama  
Extrae la intensidad de los tonos musicasles a lo largo de la señal de audio.  

```python
        chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
```

### Contraste Espectral  
Es una medida que destaca las regiones en una señal de audio que tienen una diferencia significativa en cuanto a energía espectral.  

```python
        contrast = librosa.feature.spectral_contrast(y=audio, sr=sr)
```
### Tonal Centroid Features  
Proporciona información sobre la estructura tonal y armónica de una pieza musical.
```python
            tonnetz = librosa.feature.tonnetz(y=audio, sr=sr)
```

### Tempo y Tempograma  
El tempo se refiere a la velocidad o ritmo de una composición musical.  
```python
        tempo, tempogram = librosa.beat.beat_track(y=audio, sr=sr)
```
### Indexación y Búsqueda  

En cuanto a la implementación de un eficiente sistema de indexación y búsqueda para recuperar rápidamente canciones similares en grandes conjuntos de datos musicales, se usaron los siguientes:  
### KNN-Secuencial  
El método de k-NN secuencial se basa en la búsqueda secuencial para encontrar las k canciones más cercanas a una consulta. Utiliza la distancia euclidiana entre características musicales para determinar la similitud y proporciona una solución sencilla pero efectiva para recuperar canciones similares en grandes conjuntos de datos musicales.    
```python
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
```
### KNN con Cola de Prioridad  
Este metodo optimiza la búsqueda de canciones similares al utilizar una estructura de datos que prioriza las comparaciones más prometedoras. En lugar de examinar exhaustivamente todas las canciones, esta implementación se centra en las más relevantes, mejorando significativamente la eficiencia del algoritmo.

```python

def knn_search_priority_queue(query, k):
    similarities = cosine_similarity(query.reshape(1, -1), data_normalized).flatten()
    priority_queue = PriorityQueue()
    for i, sim in enumerate(similarities):
        priority_queue.put((-sim, nombres_id[i])) 
    neighbors = []
    for _ in range(k):
        sim, neighbor = priority_queue.get()
        neighbors.append((neighbor, -sim))
    return neighbors
```
### KNN Range Search
Implica identificar todas las canciones dentro de un rango predefinido con respecto a una canción de consulta. En lugar de limitarse a un número específico de vecinos más cercanos, este enfoque permite recuperar un conjunto más amplio de canciones que comparten similitudes específicas con la canción de interés.

```python
def knn_range_search(query, radio):
    vecinos_en_radio = []
    for i, sample in enumerate(data_normalized):
        distancia = euclidean_distances(query.reshape(1, -1), sample.reshape(1, -1))[0][0]
        if distancia is not None and distancia <= radio:
            vecinos_en_radio.append((nombres_id[i], distancia))
    vecinos_en_radio = sorted(vecinos_en_radio, key=lambda x: x[1])
    return vecinos_en_radio
```
