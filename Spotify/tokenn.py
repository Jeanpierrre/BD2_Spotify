import csv
import json
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import re
import os
import nltk

idiomas_mapeados=['es','de','en','it','pt']

# stopwords 
stopwords = {
    'en': [],  
    'es': [], 
    'it': [],
    'de':[],
    'pt':[]
}

stoplist = ["0","1","2","3","4","5","6","7","8","9","_","--", "\\",
                "^",">",'.',"@","=","$" , '?', '[', ']', '¿',"(",")",
                '-', '!',"<", '\'',',', ":","``","''", ";", "»", '(-)',
                "+","0","/", "«", "{", "}", "--", "|","`","~","'","...","..","-",".....","—","'","-","“","…", "‘","#","&","%"]

with open('en/stopwords.txt', 'r') as stopwords_file:
    stopwords['en'] = stopwords_file.read().splitlines()

stopwords['en']=stopwords['en']+stoplist

# stopwords ingles
with open('es/stopwords.txt', 'r') as stopwords_file:
    stopwords['es']  = stopwords_file.read().splitlines()
stopwords['es']=stopwords['es']+stoplist
# stopwords ingles
with open('de/stopwords.txt', 'r') as stopwords_file:
    stopwords['de']  = stopwords_file.read().splitlines()
stopwords['de']= stopwords['de']+stoplist
# stopwords ingles
with open('it/stopwords.txt', 'r') as stopwords_file:
    stopwords['it']  = stopwords_file.read().splitlines()
stopwords['it']=stopwords['it']  +stoplist
# stopwords ingles
with open('pt/stopwords.txt', 'r') as stopwords_file:
    stopwords['pt'] = stopwords_file.read().splitlines()
stopwords['pt']=  stopwords['pt'] +stoplist

print("Stopwords on")

# Crear un objeto stemmer
stemmer = PorterStemmer()

# Función para limpiar y tokenizar el texto
def clean_and_tokenize(text):
    # Eliminar caracteres no alfanuméricos y convertir a minúsculas
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text).lower()
    tokens = word_tokenize(text)
    return tokens

# Datas para los idiomas
data={
    'en': {},  
    'es': {}, 
    'it': {},
    'de':{},
    'pt':{}
}

stop=[]
idioma=''

# Abrir el archivo CSV
with open('new_spotify.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:

        # Obtener el ID de la fila
        row_id = row['track_id']
        idioma_track=row['language']

        if idioma_track in idiomas_mapeados:
            idioma=idioma_track
            stop= stopwords[idioma_track]
        else:
            idioma='en'
            stop=stopwords['en']
 
        # Concatenar los atributos textuales en una cadena
        atributos_textuales = [row[key] for key in row if key not in ['track_id','track_popularity', 'track_album_release_date','danceability','energy','key','loudness','mode','speechiness'
                                                                    ,'acousticness','instrumentalness','liveness','valence','tempo','duration_ms','track_album_id','playlist_id']]
        texto_completo = ' '.join(atributos_textuales)
        
        # Limpieza y tokenización del texto
        tokens = clean_and_tokenize(texto_completo)
        
        # Eliminar las stopwords
        tokens = [token for token in tokens if token.lower() not in stop]
        
        # Aplicar stemming a los tokens
        tokens = [stemmer.stem(token) for token in tokens]

        #ordenar los tokens
        tokens.sort()
        
        # Almacenar el ID de la fila y sus tokens en el diccionario
        data[idioma][row_id] = tokens

print("csv on")

# Guardar los datos en un archivo JSON
for idioma,datos in data.items():
    nombre_archivo = os.path.join(idioma, 'archivo_procesado.json')
    with open(nombre_archivo, 'w') as json_file:
        json.dump(data[idioma], json_file, indent=4)