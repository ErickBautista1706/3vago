from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from decouple import config

# Cargar las variables de entorno desde el archivo .env
POSTGRES_URL = config('POSTGRES_URL')
POSTGRES_USER = config('POSTGRES_USER')
POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
POSTGRES_HOST = config('POSTGRES_HOST')
POSTGRES_DATABASE = config('POSTGRES_DATABASE')
POSTGRES_PORT = config('POSTGRES_PORT')

# Crear la cadena de conexión para SQLAlchemy
DB_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

# Crear el motor de SQLAlchemy
engine = create_engine(DB_URL)

def query_tipo_usuario():
    try:
        # Conectar al motor de la base de datos
        conn = engine.connect()

        # Crear un objeto de comando
        cmd = text("SELECT * FROM usuarios")  # Reemplaza 'tu_tabla' con el nombre real de tu tabla

        # Ejecutar la consulta
        result = conn.execute(cmd)

        # Procesar los resultados como sea necesario
        for row in result:
            print(row)

    except OperationalError as e:
        print(f"Error de base de datos: {e}")

    finally:
        # Cerrar la conexión
        conn.close()

# Llamar a la función
query_tipo_usuario()
