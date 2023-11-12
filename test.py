from decouple import config
import psycopg2
from psycopg2 import OperationalError

# Cargar las variables de entorno desde el archivo .env
POSTGRES_URL = config('POSTGRES_URL')
POSTGRES_USER = config('POSTGRES_USER')
POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
POSTGRES_HOST = config('POSTGRES_HOST')
POSTGRES_DATABASE = config('POSTGRES_DATABASE')
POSTGRES_PORT = config('POSTGRES_PORT')

def check_database_connection():
    try:
        # Intenta establecer una conexión a la base de datos
        conn = psycopg2.connect(
            dbname=POSTGRES_DATABASE,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )

        # Abre un cursor para ejecutar comandos SQL
        cursor = conn.cursor()

        # Realiza un ping simple para comprobar la conexión
        cursor.execute("SELECT 1")

        # Cierra el cursor y la conexión
        cursor.close()
        conn.close()

        print("Conexión exitosa a la base de datos")
    except OperationalError as e:
        print(f"Error de conexión a la base de datos: {e}")

if __name__ == "__main__":
    check_database_connection()

