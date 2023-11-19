import os
import numpy as np
import librosa
from sklearn.preprocessing import StandardScaler
import pickle

def extract_features(file_path, max_length=1000):
    audio, sr = librosa.load(file_path, mono=True)

    # Calcular 20 coeficientes de MFCC
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=20)
    mfcc_features = np.concatenate((mfccs.mean(axis=1), mfccs.std(axis=1)))#Eje que represanta el tiempo
    

    # Derivada temporal
    delta_mfccs = librosa.feature.delta(mfccs)
    delta_mfcc_features = np.concatenate((delta_mfccs.mean(axis=1), delta_mfccs.std(axis=1)))

    # Segunda Derivada temporal
    delta2_mfccs = librosa.feature.delta(mfccs, order=2)
    delta2_mfcc_features = np.concatenate((delta2_mfccs.mean(axis=1), delta2_mfccs.std(axis=1)))

    # Calcula un cromagrama a partir de una señal de audio
    chroma = librosa.feature.chroma_stft(y=audio, sr=sr)

    # Calcula el contraste espectral a partir de una señal de audio
    contrast = librosa.feature.spectral_contrast(y=audio, sr=sr)

    # Calcula el tonnetz (tonal centroid features) a partir de una señal de audio
    tonnetz = librosa.feature.tonnetz(y=audio, sr=sr)

    #  Calcula el tempo y el tempograma de una señal de audio
    tempo, tempogram = librosa.beat.beat_track(y=audio, sr=sr)

    #CONCATENAR TDO 
    all_features = np.concatenate((
        mfcc_features,
        delta_mfcc_features,
        delta2_mfcc_features,
        chroma.mean(axis=1),
        contrast.mean(axis=1),
        tonnetz.mean(axis=1),
        tempogram
    ))

    # Validar que tenga 1000 siempre
    if len(all_features) < max_length:
        all_features = np.pad(all_features, (0, max_length - len(all_features)))
    else:
        # Recortar 
        all_features = all_features[:max_length]

    return all_features



def save_features_to_pickle(folder_path, output_file):
    features = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".mp3"):
            file_path = os.path.join(folder_path, file_name)
            song_features = extract_features(file_path)
            features.append(song_features)
            print("Yes")
        
    with open(output_file, 'wb') as file:
        pickle.dump(features, file)


# Cambia 'ruta_de_tu_carpeta' por la ruta real de tus canciones
folder_path = 'Musicas'

save_features_to_pickle(folder_path,'features.pkl')
