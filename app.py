from flask import Flask, jsonify, request, render_template
from search import for_user
from flask import redirect, url_for
from prueba import buscar

# import psycopg2
app = Flask(__name__)




def get_db():
    # psycopg2 connection
    pass

@app.route("/", methods=['GET', 'POST'])
def main_query():
    product_names = None
    time = None
    if request.method == 'POST':
        user_input = request.form['input_text']
        idioma = request.form['idioma']
        #ele=request.form['indice']
        #print("ele: ",ele)
        print(idioma)
        product_names, time = for_user(user_input,idioma)
        print("User search")
        print("productos_names: ",product_names)
    return render_template('index.html', product_names=product_names, time=time)


@app.route("/listen", methods=['GET'])
def listen_to_track():
    track_name = request.args.get('track_name')
    track_artist = request.args.get('track_artist')
    print(track_name)
    print(track_artist)
    buscar(track_artist, track_name)
    # ... (lógica para reproducir la canción)

    # Redirige de vuelta a la página principal
    return redirect(url_for('main_query'))  

if __name__ == "__main__":
    app.run(debug=True)
