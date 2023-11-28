from flask import Flask, url_for, render_template, request, redirect, jsonify, request, send_file, make_response
from models.login import Login
from models.adm import Admin
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import Flask, session
from models.getInfo import GetInfos
from models.llenarReport import LlenarReporte
import shutil


app = Flask(__name__, static_folder='static')


app.secret_key = 'saranbabiche'  

@app.route("/")
def hello_world():
    return render_template('temp.html')

from flask_jwt_extended import create_access_token

@app.route('/inicio', methods=['GET', 'POST'])
def login():
    error = None
    email = None  # Se deben inicializar estas variables eh

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        auth_success, tipo_usuario = Login.check_login(email, password)
        print("Autenticación exitosa:", auth_success, "Tipo de Usuario:", tipo_usuario)

        if not auth_success:
            error = 'Error: Email o contraseña incorrectos'
        else:
            session['usuario_logueado'] = email 
            if tipo_usuario == 'Administrador':
                return redirect(url_for('admin'))
            elif tipo_usuario == 'Supervisor':
                return redirect(url_for('mostrar_gerente'))

    # Si  autenticación falla, muestra la página de inicio de sesión
    return render_template('inicio.html', error=error)


@app.route("/admin")
def admin():
    if 'usuario_logueado' not in session:
        return redirect(url_for('login'))  # Redirige al inicio de sesión si no está autenticado

    users_info = GetInfos.llenar_combo_users_zona()
    usuarios = Admin.obtener_usuarios()
    zonas = Admin.obtener_zonas()
    return render_template('admin.html', usuarios=usuarios, zonas=zonas, users_info=users_info)

@app.route('/gerente')
def mostrar_gerente():
    if 'usuario_logueado' not in session:
        return redirect(url_for('login'))  # Redirige al inicio de sesión si no está autenticado

    return render_template('gerente.html')

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
    datos_usuario = GetInfos.get_usuario_info(id_usuario)
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
        print("ID a actualizar: ", id_usr)
        
        resultado = Admin.actualizar_usuario(id_usr,nombre, apellidoP, apellidoM, alias)

        if resultado:
            return redirect(url_for("admin"))
        else:
            return "Hubo un error al agregar el usuario."
    else:
        return redirect(url_for("admin"))
    
@app.route('/logout')
def logout():
    session.pop('usuario_logueado', None)  # Elimina el usuario de la sesión
    return redirect(url_for('login'))      # Redirige a la página de inicio de sesión


@app.route("/agregar_zona", methods=["POST"])
def agregar_zona():
    if request.method == "POST":
        nombre_zona = request.form.get("nombreZona")
        ubicacion_zona = request.form.get("ubicacionZona")
        activo_zona = request.form.get("activoZona") == "true"
        id_usr_supervisor = request.form.get("selectUsuario")

        resultado = Admin.insertar_zona(nombre_zona, ubicacion_zona, activo_zona, id_usr_supervisor)

        if resultado:
            return redirect(url_for("admin"))
        else:
            return "Hubo un error al agregar la zona."
    else:
        return redirect(url_for("admin"))

@app.route('/eliminar_zona/<int:id_zona>', methods=['GET'])
def eliminar_zona(id_zona):
    if Admin.eliminar_zona(id_zona):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})
    
@app.route('/get_zona_info/<int:id_zona>', methods=['GET'])
def get_zona_info(id_zona):
    zona_info = GetInfos.obtener_info_zona(id_zona)
    return jsonify({'success': True, 'zona': zona_info})

@app.route('/actualizar_zona', methods=['POST'])
def actualizar_zona():
    if request.method == "POST":
        id_zn = request.form.get("id_zn_act")
        nombre_zn = request.form.get("nombreZona_act")
        ubicacion_zn = request.form.get("ubicacionZona_act")
        activo_zn = request.form.get("activoZona_act")
        id_usr = request.form.get("selectUsuario_act") 
        resultado = Admin.actualizar_zona(id_zn, nombre_zn, ubicacion_zn, activo_zn, id_usr)

        if resultado:
            print(id_zn)
            return redirect(url_for("admin"))
        else:
            return "Hubo un error al actualizar la zona."
    else:
        return redirect(url_for("admin"))


@app.route('/generar_reporte', methods=['GET'])
def generar_reporte():
    try:
        ruta_reporte_original = "./static/reportes/reporte No. 1.xlsx"
        
        # Obtener datos de la tabla usuarios y zonas (utiliza tus funciones específicas)
        datos_usuarios = LlenarReporte.tabla_usuarios()
        datos_zonas = LlenarReporte.tabla_zonas()

        # Crear una instancia de la clase LlenarReporte
        llenar_reporte = LlenarReporte(ruta_reporte_original)

        # Llenar la hoja de usuarios
        llenar_reporte.llenar_hoja_usuarios(datos_usuarios)

        # Llenar la hoja de zonas
        llenar_reporte.llenar_hoja_zonas(datos_zonas)

        # Guardar el reporte
        llenar_reporte.guardar_reporte()

        # Crear una respuesta para el archivo
        response = make_response(send_file(ruta_reporte_original, as_attachment=True, download_name="reporte_lleno.xlsx"))
        
        # Configurar la respuesta para descargar automáticamente
        response.headers["Content-Disposition"] = "attachment; filename=reporte_lleno.xlsx"

        return response

    except Exception as e:
        return f"Error al generar el reporte: {e}"







def formatear_fecha_hora(dt):    
    formato = "%Y-%m-%d %H:%M:%S"
    return dt.strftime(formato) if dt else None





if __name__ == '__main__':
    app.run(debug=True)
