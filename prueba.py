from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from decouple import config

# Cargar las variables de entorno desde el archivo .env
POSTGRES_URL = config('POSTGRES_URL')
POSTGRES_USER = config('POSTGRES_USER')
POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
POSTGRES_HOST = config('POSTGRES_HOST')
POSTGRES_DATABASE = config('POSTGRES_DATABASE')
POSTGRES_PORT = config('POSTGRES_PORT')

def check_database_connection():
    try:
        # Crea una cadena de conexión para SQLAlchemy
        db_url = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

        # Crea una instancia de SQLAlchemy Engine para conectarse a la base de datos
        engine = create_engine(db_url)

        # Intenta abrir una conexión
        connection = engine.connect()
        connection.close()

        print("Conexión exitosa a la base de datos")
    except OperationalError as e:
        print(f"Error de conexión a la base de datos: {e}")

if __name__ == "__main__":
    check_database_connection()
