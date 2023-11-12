import os
import numpy as np
import librosa
from sklearn.preprocessing import StandardScaler

def extract_features(file_path, max_length=1000):
    audio, sr = librosa.load(file_path, mono=True)

    # 1. Coeficientes MFCC
    mfccs = librosa.feature.mfcc(y=audio, sr=sr)
    mfcc_features = np.concatenate((mfccs.mean(axis=1), mfccs.std(axis=1)))

    # 2. Cromagrama
    chroma = librosa.feature.chroma_stft(y=audio, sr=sr)

    # 3. Contraste espectral
    contrast = librosa.feature.spectral_contrast(y=audio, sr=sr)

    # 4. Tonnetz
    tonnetz = librosa.feature.tonnetz(y=audio, sr=sr)

    # 5. Tempograma
    tempo, tempogram = librosa.beat.beat_track(y=audio, sr=sr)

    # Asegurar que todas las características tengan la misma longitud
    all_features = np.concatenate((mfcc_features, chroma.mean(axis=1)[:max_length], contrast.mean(axis=1)[:max_length], tonnetz.mean(axis=1)[:max_length], tempogram[:max_length]))
    
    # Rellenar con ceros si es necesario
    if len(all_features) < max_length:
        all_features = np.pad(all_features, (0, max_length - len(all_features)))

    return all_features

def save_features(folder_path, output_file):
    features = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".mp3"):
            file_path = os.path.join(folder_path, file_name)
            song_features = extract_features(file_path)
            features.append(song_features)

    np.save(output_file, np.array(features))

# Cambia 'ruta_de_tu_carpeta' por la ruta real de tus canciones
folder_path = 'es'
save_features(folder_path, 'features.npy')
