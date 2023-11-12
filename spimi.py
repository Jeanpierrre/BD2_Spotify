import json
import os

#usa una carpeta temporal, para hacer un merge de bloques dando al final un indice invertido global

idiomas_mapeados=['es','de','en','it','pt']

def spimi_invert_from_json(json_file, output_directory, max_block_size):
    # Inicializar variables y estructuras de datos necesarias
    block = {}
    block_size = 0
    block_number = 0
    temporary_files = []
    print(json_file)

    with open(json_file, 'r') as json_data:
        data = json.load(json_data)
        
        for doc_id, doc_tokens in data.items():
            for token in doc_tokens:
                # Agregar el token al bloque actual
                if token not in block:
                    block[token] = []
                block[token].append(doc_id)

                # Verificar el tamaño del bloque
                block_size += 1

                if block_size >= max_block_size:
                    # Guardar el bloque actual en un archivo temporal
                    block_filename = os.path.join(output_directory, f'temp_block_{block_number}.json')
                    with open(block_filename, 'w') as block_file:
                        json.dump(block, block_file)
                    temporary_files.append(block_filename)

                    # Limpiar el bloque para el próximo conjunto de tokens
                    block = {}
                    block_size = 0
                    block_number += 1

    # Procesar el último bloque si no se alcanzó el tamaño máximo
    if block:
        block_filename = os.path.join(output_directory, f'temp_block_{block_number}.json')
        with open(block_filename, 'w') as block_file:
            json.dump(block, block_file)
        temporary_files.append(block_filename)

    return temporary_files


def merge_blocks(temporary_directory, output_file):
    """
    Fusiona los bloques temporales para construir un índice invertido completo con términos ordenados alfabéticamente.

    Args:
        temporary_directory (str): Directorio que contiene los archivos temporales generados por SPIMI.
        output_file (str): Ruta al archivo de salida donde se guardará el índice invertido completo.
    """
    inverted_index = {}

    temporary_files = sorted(os.listdir(temporary_directory))

    for temp_file in temporary_files:
        temp_file_path = os.path.join(temporary_directory, temp_file)

        with open(temp_file_path, 'r') as temp_data:
            block_data = json.load(temp_data)

            # Fusionar los datos del bloque con el índice invertido
            for term, postings in block_data.items():
                if term not in inverted_index:
                    inverted_index[term] = []
                inverted_index[term].extend(postings)

    # Ordenar alfabéticamente los términos en el índice invertido
    sorted_inverted_index = {term: inverted_index[term] for term in sorted(inverted_index)}

    # Guardar el índice invertido completo en un archivo
    with open(output_file, 'w') as index_file:
        json.dump(sorted_inverted_index, index_file, indent=4)

    # Limpiar los archivos temporales
    for temp_file in temporary_files:
        temp_file_path = os.path.join(temporary_directory, temp_file)
        os.remove(temp_file_path)



#spimi_invert_from_json('archivo_procesado.json', 'temp', 1000)

#merge_blocks('temp', 'indice_invertido.json')


for idioma in idiomas_mapeados:

    ruta_json = os.path.join(idioma, 'archivo_procesado.json')
#    print(ruta_json)
    ruta_temp = os.path.join(idioma, 'temp')
    spimi_invert_from_json(ruta_json,ruta_temp,1000)

    nombre_output= os.path.join(idioma, 'indice_invertido.json')
    merge_blocks(ruta_temp,nombre_output)