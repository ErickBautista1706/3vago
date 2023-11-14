from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError  
from models.database import Database

class Login:
    def check_login(email, password):
        try:
            # Crear una instancia de la clase Database
            db = Database()

            # Obtener el motor de SQLAlchemy de la instancia de la clase Database
            conn = db.engine.connect()

            # Crear un objeto de comando
            cmd = text("SELECT * FROM usuarios WHERE email = :email AND psw = :password")

            # Ejecutar la consulta
            result = conn.execute(cmd, {'email': email, 'password': password})

            # Procesar los resultados
            user = result.fetchone()

            # Cerrar la conexión
            conn.close()

            if user:
                return True
            else:
                return False

        except OperationalError as e:
            print(f"Error de base de datos: {e}")
