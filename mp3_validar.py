import numpy as np
from sklearn.neighbors import NearestNeighbors
from mp3_Caracteristicas import extract_features
from sklearn.preprocessing import StandardScaler

# Cargar características existentes
existing_features = np.load('features.npy')
print("-----------CARGADO------------")
# Configurar el modelo k-NN
n_neighbors = 4
knn_model = NearestNeighbors(n_neighbors=n_neighbors, metric='euclidean')

# Ajustar y transformar las características existentes con StandardScaler
scaler = StandardScaler()
existing_features_scaled = scaler.fit_transform(existing_features)
knn_model.fit(existing_features_scaled)

# Calcular características de la nueva canción y transformar con el mismo StandardScaler
nueva_cancion_features = extract_features("Bad Bunny - NI BIEN NI MAL.mp3")
nueva_cancion = scaler.transform([nueva_cancion_features])

# Encontrar vecinos cercanos
distances, indices = knn_model.kneighbors(nueva_cancion)

print(f"Vecinos cercanos para la nueva canción: {indices} con distancia {distances}")
