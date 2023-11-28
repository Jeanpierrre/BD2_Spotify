from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
import pprint
import webbrowser
import pyautogui
from time import sleep
from urllib.parse import quote
import csv
import json
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import re
import os
#TE QUIERO MUCHO CAUSA
idiomas_mapeados=['es','de','en','it','pt']
directorio_original = os.getcwd()
#estas son mis creedenciales, no se cuanto duren xDDDDD
client_id = "3f54e3fbacdc45d3bedabd32238802e8"
client_secret = "e5c73a13fc0c47efb49c7bb054f0383b"
#funcion encargada de traer el url de la cancion en base al nombre de esta misma y su artista
def buscar(autor, song):
    autor = autor.upper()
    if len(autor) > 0:
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))
        query = f"{song} {autor}"  #trae la cancion exacta del artista
        result = sp.search(query, type='track', limit=1)  #pueden haber varias versiones de la cancion del mismo artista, solo me importa 1
        #print(query)
        #print(result)
        if result['tracks']['items']:
            track_uri = result['tracks']['items'][0]['external_urls']['spotify']
            #print("asa")
            return track_uri
        else:
            print("No se encontró la canción en Spotify.")
    else:
        print("El nombre del artista está vacío.")

#buscar('Bump Of Chicken', 'Souvenir')


import subprocess
#con ese url gracias a la libreria de spotdl(pirata(?)) podemos descargar la cancion en su calidad mas baja, que viene a ser .mp3 128kbps
def descargar(artista,name):
    #name='SPECIALZ'
    #artistas='King Gnu'

    spotify_track_url = buscar(artista,name)

    comando_spotdl = f"spotdl {spotify_track_url}"

    try:
        output = subprocess.check_output(comando_spotdl, shell=True, text=True)
        print(output)
    except subprocess.CalledProcessError as e:
        print("Error al descargar la pista:", e)


#Descargar las primeras 5000 canciones del csv
with open('new_spotify.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        # Obtener el ID de la fila
        artista=row['track_name']
        name=row['track_artist']
        idioma_track=row['language']
        if idioma_track in idiomas_mapeados:
            nombre_archivo = os.path.join(idioma_track)
            #descargar(artista,name)
#            print(nombre_archivo)
        else:
            nombre_archivo = os.path.join('en')
            #print(nombre_archivo)
        
       # print(nombre_archivo)
        #carpeta de la cancion
        os.chdir(nombre_archivo)
        
        descargar(artista, name)

        os.chdir(directorio_original)#volver al directorio raiz
        print("#######--CANCION LISTA--#######")
    


