from flask import Flask, url_for, render_template, request, redirect
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from decouple import config

app = Flask(__name__, static_folder='static')

@app.route("/")
def hello_world():
    return render_template('temp.html')

@app.route('/inicio', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not check_login(email, password):
            error = 'Error: Email o contraseña incorrectos'
        else:
            return redirect(url_for('admin'))
    return render_template('inicio.html', error=error)


@app.route("/admin")
def admin():
    return render_template('admin.html')

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

def check_login(email, password):
    try:
        conn = engine.connect()

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


if __name__ == '__main__':
    app.run(debug=True)
