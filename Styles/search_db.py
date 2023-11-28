import psycopg2
from psycopg2 import sql
import pandas as pd
import time

def get_db():
    conn = psycopg2.connect(dbname='styles', user='postgres', host='localhost', password='1234')
    print("Conectado a base de datos - styles")
    return conn

def create_table(table, conn):
    cur = conn.cursor()
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table} (
            id integer,
            gender text,
            mastercategory text,
            subcategory text,
            articletype text,
            basecolour text,
            season text,
            year numeric,
            usage text,
            productdisplayname text
        );
    """
    cur.execute(create_table_query)

    conn.commit()
    cur.close()

def insert_from_csv (csv_file, conn):
    cur = conn.cursor()
    df = pd.read_csv(csv_file)

    for _, row in df.iterrows():
        insert_query = """
            INSERT INTO styles VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cur.execute(insert_query, tuple(row))
    conn.commit()
    cur.close()

def create_index (table_name, conn):
    try: 
        cur = conn.cursor()
        cur.execute(f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS inverted_index tsvector;")

        # --- REVISAR ---
        cur.execute(f"""UPDATE {table_name} SET inverted_index = 
                    setweight(to_tsvector('english', gender), 'A') ||
                    setweight(to_tsvector('english', mastercategory), 'B') ||
                    setweight(to_tsvector('english', subcategory), 'C') ||
                    setweight(to_tsvector('english', articletype), 'D') ||
                    setweight(to_tsvector('english', basecolour), 'D') ||
                    setweight(to_tsvector('english', season), 'D') ||
                    setweight(to_tsvector('english', productdisplayname), 'D');
                    """)
        
        # CREATE INDEX IF NOT EXISTS {table_name}_inverted_i ON {table_name} USING gin(inverted_index);

        conn.commit()
        print("Indice creado correctamente\n")
    except:
        print("Error al crear el indice\n")
    finally:
        cur.close()

def search_using_inverted_index(table_name, search_term, k):
    conn = get_db()
    cur = conn.cursor()

    # --- REVISAR ---
    search_terms = search_term.split()

    # Construir una cadena de búsqueda combinando los términos
    combined_search_term = ' & '.join(search_terms)

    # Utilizar la cadena de búsqueda en la consulta SQL
    search_query = f"""
        SELECT id, productdisplayname FROM {table_name} 
        WHERE inverted_index @@ to_tsquery('english', %s) 
        ORDER BY ts_rank_cd(inverted_index, to_tsquery('english', %s)) DESC 
        LIMIT {k};
    """
    cur.execute(search_query, (combined_search_term, combined_search_term))

    results = cur.fetchall()
    conn.close()

    _id, _productname = zip(*results) if results else ([], [])
    _id = map(str, _id)

    return list(_id), list(_productname)

# -----

# Main function - create/insert/index
def sql_main ():
    conn = get_db()
    create_table("styles", conn)
    insert_from_csv("../Data/styleslimpio.csv", conn)
    create_index("styles", conn)
    conn.close()

# Used for frontend
def for_user_sql (query, k):
    s_time = time.time()
    product_ids, product_names = search_using_inverted_index("styles", query, k)
    e_time = time.time()
    exe_time = e_time - s_time

    return product_names, product_ids, round(exe_time, 3)

# sql_main()
