from flask import Flask, jsonify, request, render_template, redirect, url_for
from Styles.search import for_user_index
from Styles.search_db import for_user_sql
from Spotify.search import for_user, cargar_datos
from Spotify.db import for_user_spotify_sql
from Spotify.stfy_search import online_search
from Spotify.use_characteristics import search_id_characteristics, extract_normalized, knn_search_priority_queue, knn_range_search, knn_sequential, knn_rtree, find_for_rtree, init_rtree, knn_faiss_HNSWFlat
import csv
import re
# import eyed3

app = Flask(__name__)
# For listen on spotify
app.config['time_g'] = None
app.config['product_names_g'] = []

def get_links(file):
    links = {}
    file = "Data/" + file
    with open(file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            id = row['filename']
            id = id.replace('.jpg', '')
            link_ = row['link']
            links[id] = link_
    return links

def get_track_name(t_id):
    with open('Data/new_spotify.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['track_id'] == t_id:
                return row['track_name']
    return None

def get_track_artist(t_id):
    with open('Data/new_spotify.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['track_id'] == t_id:
                return row['track_artist']
    return None

"""
def extraer_caratula(ruta_archivo):
    audiofile = eyed3.load(ruta_archivo)

    # Verificar si hay información de carátula
    if audiofile.tag and audiofile.tag.images:
        imagen = audiofile.tag.images[0]
        
        # Extraer el tipo de imagen (generalmente 'image/jpeg' o 'image/png')
        tipo_imagen = imagen.mime_type

        # Guardar la imagen en un archivo
        with open('caratula.jpg', 'wb') as f:
            f.write(imagen.image_data)

        print(f"Carátula extraída y guardada como caratula.{tipo_imagen.split('/')[1]}")
    else: 
        print("No se encontró información de carátula en el archivo.")
"""
        
"""
@app.route("/", methods=['GET', 'POST'])
def main_query():
    product_names = []
    product_ids = []
    
    time = None
    gallery_links = None
    gallery_data = None

    search_option = ""
    active_section = ""
    # is_clothes = True

    if request.method == 'POST':
        active_section = request.form['active_section']
        print(active_section)

    if request.method == 'POST' and active_section == 'clothSearch':
        user_input = request.form['input_text']
        search_option = request.form['search_option']

        if search_option == "Our_index":
            product_names, product_ids, time = for_user_index(user_input)
            print(f"User search - {user_input}, Search option - {search_option}")
        else:
            product_names, product_ids, time = for_user_sql(user_input)
            print(f"User search - {user_input}, Search option - {search_option}")

        # Obtener links de csv y hacer match según resultado de busqueda
        query_links = get_links("images.csv")
        gallery_links = [query_links.get(id, '') for id in product_ids]

        # gallery_data = zip(gallery_links, product_names)
        if gallery_links is not None and product_names is not None:
            gallery_data = zip(gallery_links, product_names)
        else:
            gallery_data = []
        
    elif request.method == 'POST' and active_section == 'songSearch':
        user_input = request.form['input_text']
        search_option = request.form['search-option-songs']
        language = request.form['language-option']
        
        if language == "Language":
            print("None")
        else:
            if search_option == "Our_index":
                datos = cargar_datos()
                product_names, time = for_user(user_input, language, datos)
                print(f"User search - {user_input}, Search option - {search_option}, Language - {language}")
            else:
                product_names, time = for_user_spotify_sql(user_input, language)
                print(f"User search - {user_input}, Search option - {search_option}, Language - {language}")

        app.config['time_g'] = time
        app.config['product_names_g'] = product_names
        return render_template('song_search.html', gallery_data=gallery_data, time=time, product_names=product_names)

    return render_template('index.html', gallery_data=gallery_data, time=time)
"""

@app.route("/", methods=['GET', 'POST'])
def main_clothes():
    product_names = []
    product_ids = []
    
    time = None
    gallery_links = None
    gallery_data = None

    search_option = ""
    active_section = ""

    error_message = None

    if request.method == 'POST':
        main_button_value = request.form.get('main_button')

        if main_button_value == '1':
            return redirect(url_for('main_clothes'))
        elif main_button_value == '2':
            return redirect(url_for('main_songs'))

    if request.method == 'POST':
        user_input = request.form['input_text']
        search_option = request.form['search_option']
        
        pattern = re.compile(r'^\s*([\w\s-]+)\s*-\s*([\d-]+)\s*$')
        match = pattern.match(user_input)

        if not match:
            error_message = 'Formato incorrecto. Debe ser Query - TopK'
            
        else:
            word_query = match.group(1)
            num_k = int(match.group(2))

            if search_option == "Our_index":
                product_names, product_ids, time = for_user_index(word_query, num_k)
                print(f"User search - {word_query}, Search option - {search_option}")

                if product_names == []:
                    time = 0.0
                    error_message = f'Oops! No se encontró nada relacionado a {word_query}'

            else:
                product_names, product_ids, time = for_user_sql(word_query, num_k)
                print(f"User search - {word_query}, Search option - {search_option}")

                if product_names == []:
                    time = 0.0
                    error_message = f'Oops! No se encontró nada relacionado a {word_query}'

        query_links = get_links("images.csv")
        gallery_links = [query_links.get(id, '') for id in product_ids]

        if gallery_links is not None and product_names is not None:
            gallery_data = zip(gallery_links, product_names)
        else:
            gallery_data = []

    return render_template('clothes_search.html', gallery_data=gallery_data, time=time, error_message=error_message)

@app.route("/songs-engine", methods=['GET', 'POST'])
def main_songs():
    product_names = []
    product_ids = []
    
    time = None
    gallery_links = None
    gallery_data = None

    search_option = ""
    active_section = ""

    error_message_1 = None

    if request.method == 'POST':
        user_input = request.form['input_text']
        search_option = request.form['search-option-songs']
        language = request.form['language-option']
        
        if language == "Language":
            print("Language - None")
            error_message_1 = 'Select a language'
        else:
            pattern = re.compile(r'^\s*([\w\s-]+)\s*-\s*([\d-]+)\s*$')
            match = pattern.match(user_input)
        
            if not match:
                error_message_1 = 'Formato incorrecto. Debe ser Query - TopK'
            else:
                word_query = match.group(1)
                num_k = int(match.group(2))
                
                if search_option == "Our_index":
                    datos = cargar_datos()
                    product_names, time = for_user(user_input, language, datos, num_k)
                    print(f"User search - {word_query}, Search option - {search_option}, Language - {language}")

                    if product_names == []:
                        time = 0.0
                        error_message_1 = f'Oops! No se encontró nada relacionado a {word_query}'

                else:
                    product_names, time = for_user_spotify_sql(user_input, language, num_k)
                    print(f"User search - {word_query}, Search option - {search_option}, Language - {language}")

                    if product_names == []:
                        time = 0.0
                        error_message_1 = f'Oops! No se encontró nada relacionado a {word_query}'

    app.config['time_g'] = time
    app.config['product_names_g'] = product_names
    
    return render_template('songs_search.html', time=time, product_names=product_names, error_message_1=error_message_1)

# Load song on spotify web page
@app.route("/listen", methods=['GET'])
def listen_to_track():
    # Lógica para reproducir la canción
    track_name = request.args.get('track_name')
    track_artist = request.args.get('track_artist')
    
    online_search(track_artist, track_name)

    # Devuelve una respuesta JSON
    response_data = {'time': app.config['time_g'], 'product_names': app.config['product_names_g']}

    return jsonify(response_data)

# Doing algorithms for nearest data
@app.route("/table_for_knn_priority_queue", methods=['POST'])
def for_knn_priority_queue():
    k = int(request.form.get('quantity'))

    track_id = request.form.get('track_id')
    pos = search_id_characteristics(track_id)
    
    if pos is not None:
        vt = extract_normalized(pos)

        out = knn_search_priority_queue(vt, k);

        tabla_html = "<table><thead><tr><th>Track Name</th><th>Track Artist</th><th>Similarity</th><th>Player</th></tr></thead><tbody>"

        for i, data in out:
            aux = get_track_name(i[:-5])
            artist = get_track_artist(i[:-5])
            sim = round(data, 3)

            audio_path = url_for('static', filename='Songs/'+ i[:-1])
            # tabla_html += f"<tr><td>{aux}</td><td>{artist}</td><td>{sim}</td></tr>"
            tabla_html += f"<tr><td>{aux}</td><td>{artist}</td><td>{sim}</td><td><audio controls><source src='{audio_path}' type='audio/mp3'></audio></td></tr>"

        tabla_html += "</tbody></table>"

        return tabla_html
    else:
        return "<h2>No data available for algorithm</h2>"

@app.route("/table_for_range_search", methods=['POST'])
def for_knn_by_range():
    k = int(request.form.get('quantity'))

    track_id = request.form.get('track_id')
    pos = search_id_characteristics(track_id)

    if pos is not None:
        vt = extract_normalized(pos)

        out = knn_range_search(vt, k);

        tabla_html = "<table><thead><tr><th>Track Name</th><th>Track Artist</th><th>Similarity</th></tr></thead><tbody>"

        for i, data in out:
            aux = get_track_name(i[:-5])
            artist = get_track_artist(i[:-5])
            sim = round(data, 3)

            audio_path = url_for('static', filename='Songs/'+ i[:-1])
            # tabla_html += f"<tr><td>{aux}</td><td>{artist}</td><td>{sim}</td></tr>"
            tabla_html += f"<tr><td>{aux}</td><td>{artist}</td><td>{sim}</td><td><audio controls><source src='{audio_path}' type='audio/mp3'></audio></td></tr>"

        tabla_html += "</tbody></table>"

        return tabla_html
    else:
        return "<h2>No data available for algorithm</h2>"

@app.route("/table_for_knn_sequential", methods=['POST'])
def for_knn_sequential():
    k = int(request.form.get('quantity'))

    track_id = request.form.get('track_id')
    pos = search_id_characteristics(track_id)

    if pos is not None:
        vt = extract_normalized(pos)

        out = knn_sequential(vt, k);

        tabla_html = "<table><thead><tr><th>Track Name</th><th>Track Artist</th><th>Similarity</th></tr></thead><tbody>"

        for i, data in out:
            aux = get_track_name(i[:-5])
            artist = get_track_artist(i[:-5])
            sim = round(data, 3)
            
            audio_path = url_for('static', filename='Songs/'+ i[:-1])
            # tabla_html += f"<tr><td>{aux}</td><td>{artist}</td><td>{sim}</td></tr>"
            tabla_html += f"<tr><td>{aux}</td><td>{artist}</td><td>{sim}</td><td><audio controls><source src='{audio_path}' type='audio/mp3'></audio></td></tr>"

        tabla_html += "</tbody></table>"

        return tabla_html
    else:
        return "<h2>No data available for algorithm</h2>"

@app.route("/table_for_knn_rtree", methods=['POST'])
def for_knn_rtree():
    k = int(request.form.get('quantity'))
    track_id = request.form.get('track_id')
    pos = search_id_characteristics(track_id)

    if pos is not None:
        out = knn_rtree(pos, k)
        out_f = find_for_rtree(out)

        tabla_html = "<table><thead><tr><th>Track Name</th></tr></thead><tbody>"

        for i in out_f:
            aux = get_track_name(i[:-5])
            artist = get_track_artist(i[:-5])

            audio_path = url_for('static', filename='Songs/'+ i[:-1])
            # tabla_html += f"<tr><td>{aux}</td><td>{artist}</td></tr>"
            tabla_html += f"<tr><td>{aux}</td><td>{artist}</td><td><audio controls><source src='{audio_path}' type='audio/mp3'></audio></td></tr>"
        
        tabla_html += "</tbody></table>"

        return tabla_html
    else:
        return "<h2>No data available for algorithm</h2>"

@app.route("/table_for_knn_highd", methods=['POST'])
def for_knn_highd():
    k = int(request.form.get('quantity'))
    track_id = request.form.get('track_id')

    pos = search_id_characteristics(track_id)

    if pos is not None:
        vt = extract_normalized(pos)
        out = knn_faiss_HNSWFlat(vt, k);

        tabla_html = "<table><thead><tr><th>Track Name</th><th>Track Artist</th><th>Similarity</th></tr></thead><tbody>"

        for data, i in out:
            aux = get_track_name(i[:-5])
            artist = get_track_artist(i[:-5])
            sim = round(data, 3)

            audio_path = url_for('static', filename='Songs/'+ i[:-1])
            # tabla_html += f"<tr><td>{aux}</td><td>{artist}</td><td>{sim}</td></tr>"
            tabla_html += f"<tr><td>{aux}</td><td>{artist}</td><td>{sim}</td><td><audio controls><source src='{audio_path}' type='audio/mp3'></audio></td></tr>"

        tabla_html += "</tbody></table>"

        return tabla_html
    else:
        return "<h2>No data available for algorithm</h2>"

if __name__ == "__main__":
    # For Rtree
    # init_rtree()
    app.run(debug=True)
