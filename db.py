import psycopg2
from psycopg2 import sql
import pandas as pd
from dotenv import load_dotenv
import os
import time
#.env
from dotenv import load_dotenv
load_dotenv()

"""
PRIEMRP CREA LA BD LLAMADA Spotify en PGADMIN
CAMBIA LAS CREDENCIALES SEA EL CASO
HOST="localhost"
PORT="5432"
DBNAME="Spotify"
USER="postgres"
PASSWORD=""
"""


"""
print("HOST:", os.getenv("HOST"))
print("PORT:", os.getenv("PORT"))
print("DBNAME:", os.getenv("DBNAME"))
print("USER:", os.getenv("USER"))
print("PASSWORD:", os.getenv("PASSWORD"))"""

def conectar_bd():
    # Establecer la conexión a la base de datos PostgreSQL
    conn = psycopg2.connect(
        host=os.getenv("HOST"),
        port=os.getenv("PORT"),
        dbname=os.getenv("DBNAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD")
    )
    print("Conectado a la base de datos:", conn.dsn)
    return conn

def crear_tabla(tabla,conn):
    
    cur = conn.cursor()
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {tabla} (
        track_id VARCHAR(255),
        track_name TEXT,
        track_artist TEXT,
        lyrics TEXT,
        track_popularity INT,
        track_album_id VARCHAR(255),
        track_album_name TEXT,
        track_album_release_date DATE,
        playlist_name TEXT,
        playlist_id VARCHAR(255),
        playlist_genre TEXT,
        playlist_subgenre TEXT,
        danceability FLOAT,
        energy FLOAT,
        key INT,
        loudness FLOAT,
        mode INT,
        speechiness FLOAT,
        acousticness FLOAT,
        instrumentalness FLOAT,
        liveness FLOAT,
        valence FLOAT,
        tempo FLOAT,
        duration_ms INT,
        language VARCHAR(255)
    );
    """
    # Ejecutar la consulta 
    cur.execute(create_table_query)

    # Gruardar cambios
    conn.commit()
    #cerrar cursor
    cur.close()


def insertar_datos(conn, csv_file_path):
    cur = conn.cursor()

    # Leer el archivo CSV usando pandas
    df = pd.read_csv(csv_file_path)

    #iterar en el csv
    for _, row in df.iterrows():
        # insertar
        insert_query = """
        INSERT INTO song VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        # Ejecutar la consulta de inserción
        cur.execute(insert_query, tuple(row))#tienen las mismas columnas

    conn.commit()
    cur.close()

def main():
    # Conectar a la bd
    conn = conectar_bd()

    # crear tabla
    tabla="song"
    crear_tabla(tabla,conn)


    csv_file_path = 'new_spotify.csv'  

    insertar_datos(conn, csv_file_path)

    conn.close()

    print(f"La tabla {tabla} se ha creado y los datos se han insertado correctamente.")


def get_mapped_language(language, idiomas_mapeados):
    return idiomas_mapeados.get(language, 'english')

# Crear índice invertido según el idioma de cada fila
def create_index_by_language(conn, idiomas_mapeados):
    cur = conn.cursor()
    cur.execute("ALTER TABLE song ADD COLUMN inverted_index tsvector;")
    cur.execute("SELECT track_id, track_name, track_artist, lyrics, language FROM song;")
    for row in cur.fetchall():
        track_id, track_name, track_artist, lyrics, language = row
        idioma_mapeado = idiomas_mapeados.get(language, 'english')
        print("Para el lenguaje: ",language)
        print("Se utilizo el stopword de: ", idioma_mapeado)
        cur.execute(sql.SQL("""
            UPDATE song
            SET inverted_index = setweight(to_tsvector(%s, COALESCE(%s, '')), 'A') ||
                                 setweight(to_tsvector(%s, COALESCE(%s, '')), 'B') ||
                                 setweight(to_tsvector(%s, COALESCE(%s, '')), 'C')
            WHERE track_id = %s;
        """), (idioma_mapeado, track_name, idioma_mapeado, track_artist, idioma_mapeado, lyrics, track_id))
    conn.commit()
    cur.close()



idiomas_mapeados = {
    'es': 'spanish',
    'it': 'italian',
    'pt': 'portuguese',
    'en': 'english',
    'de':'german'
}


#main()
#create_index_by_language(idiomas_mapeados)
def search_inverted_index(query, language):
    conn = conectar_bd()
    cur = conn.cursor()

    # Crear la consulta SQL para la búsqueda en el índice invertido con el idioma especificado
    search_query = f"""
        SELECT track_id, track_name, track_artist, lyrics, ts_rank_cd(inverted_index, query) AS rank
        FROM song,
             to_tsquery(%s) AS query
        WHERE inverted_index @@ query
        AND language = %s
        ORDER BY rank DESC;
    """

    cur.execute(search_query, (query, language))
    results = cur.fetchall()

    cur.close()
    conn.close()

    return results

def for_user_sql(query,idioma):
    s_time = time.time()
    results = search_inverted_index(query,idioma)
    e_time = time.time()
    exe_time = e_time - s_time

   
    return results, round(exe_time, 3)

"""
search_results = search_inverted_index('girl','en')

if search_results:
    print("Resultados de la búsqueda:")
    for result in search_results:
        track_id, track_name, track_artist, lyrics, rank = result
        print(f"ID: {track_id}, Nombre: {track_name}, Artista: {track_artist}, Letras: {lyrics[:100]}..., Relevancia: {rank}")
    print(len(search_results))
else:
    print("No se encontraron resultados para la consulta.")
"""

