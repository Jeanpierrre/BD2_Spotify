from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
import pprint
import webbrowser
import pyautogui
from urllib.parse import quote

client_id = "3f54e3fbacdc45d3bedabd32238802e8"
client_secret = "e5c73a13fc0c47efb49c7bb054f0383b"

def online_search(autor, song):
    autor = autor.upper()
    flag = 0

    if len(autor) > 0:
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))
        query = f"{song} {autor}"  # Búsqueda sin el prefijo 'artist:' para obtener resultados más precisos
        result = sp.search(query, type='track', limit=1)  # Limitar los resultados a 1 canción
        # print(query)
        # print(result)
        if result['tracks']['items']:
            track_uri = result['tracks']['items'][0]['external_urls']['spotify']
            webbrowser.open(track_uri)  # Abrir el enlace en el navegador web predeterminado
        else:
            print("No se encontró la canción en Spotify.")
    else:
        print("El nombre del artista está vacío.")

# buscar('Bump Of Chicken', 'Souvenir')
# buscar('Aqours', 'ユメ語るよりユメ歌おう')
