from flask import Flask, url_for, render_template, request, redirect, jsonify
from models.login import Login
from models.adm import Admin

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
        if not Login.check_login(email, password):
            error = 'Error: Email o contraseña incorrectos'
        else:
            return redirect(url_for('admin'))
    return render_template('inicio.html', error=error)


@app.route("/admin")
def admin():
    return Admin.mostrar_usuarios()

@app.route("/agregar_usuario", methods=["POST"])
def agregar_usuario():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        apellidoP = request.form.get("apellidoP")
        apellidoM = request.form.get("apellidoM")
        alias = request.form.get("alias")
        email = request.form.get("email")
        psw = request.form.get("psw")
        tipoUsuario = request.form.get("tipoUsuario")
        
        resultado = Admin.insertar_usuario(nombre, apellidoP, apellidoM, alias, email, psw, tipoUsuario)

        if resultado:
            return redirect(url_for("admin"))
        else:
            return "Hubo un error al agregar el usuario."
    else:
        return redirect(url_for("admin"))
    

@app.route('/eliminar_usuario/<int:id_usuario>', methods=['GET'])
def eliminar_usuario(id_usuario):
    if Admin.eliminar_usuario(id_usuario):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})
    
@app.route('/get_usuario_info/<int:id_usuario>', methods=['GET'])
def obtener_usuario_info(id_usuario):
    datos_usuario = Admin.get_usuario_info(id_usuario)
    print(datos_usuario)
    return jsonify({'success': True, 'usuario': datos_usuario})

@app.route('/actualizar_usuario', methods=['POST'])
def actualizar_usuario():
    if request.method == "POST":
        id_usr = request.form.get("id_usr")
        nombre = request.form.get("nombre")
        apellidoP = request.form.get("apellidoP")
        apellidoM = request.form.get("apellidoM")
        alias = request.form.get("alias")
        tipoUsuario = request.form.get("tipoUsuario")
        print("ID a actualizar: ", id_usr)
        
        resultado = Admin.actualizar_usuario(id_usr,nombre, apellidoP, apellidoM, alias)

        if resultado:
            return redirect(url_for("admin"))
        else:
            return "Hubo un error al agregar el usuario."
    else:
        return redirect(url_for("admin"))


if __name__ == '__main__':
    app.run(debug=True)
