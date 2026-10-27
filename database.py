import psycopg2
import pandas as pd

DB_CONFIG = {
    "host": "localhost",
    "database": "spotychipi",  
    "user": "postgres",
    "password": "",            
    "port": "5432"
}

def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def ejecutar_consulta(query, params=None):
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        df = pd.read_sql_query(query, conn, params=params)
        return df
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def ejecutar_comando(query, params=None):
    conn = get_connection()
    if conn is None:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            conn.commit()
        return True
    except Exception as e:
        print(f"Error al ejecutar comando: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()