from flask import Flask, url_for, render_template, request, redirect, jsonify, request, send_file, make_response
from models.login import Login
from models.adm import Admin
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import Flask, session
from models.getInfo import GetInfos
from models.llenarReport import LlenarReporte
from models.dashboard import Dash
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

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        auth_success, tipo_usuario = Login.check_login(email, password)
        print("Autenticación exitosa:", auth_success, "Tipo de Usuario:", tipo_usuario)

        if not auth_success:
            error = 'Error: Email o contraseña incorrectos'
        else:
            session['usuario_logueado'] = email
            session['tipo_usuario'] = tipo_usuario  # Guardar tipo de usuario en la sesión
            if tipo_usuario == 'Administrador':
                return redirect(url_for('admin'))
            elif tipo_usuario == 'Supervisor':
                return redirect(url_for('mostrar_gerente'))

    return render_template('login2.html', error=error)


@app.route("/admin")
def admin():
    # Verifica si el usuario está logueado y si es Administrador
    if 'usuario_logueado' not in session or session.get('tipo_usuario') != 'Administrador':
        return redirect(url_for('login'))

    users_info = GetInfos.llenar_combo_users_zona()
    usuarios = Admin.obtener_usuarios()
    zonas = Admin.obtener_zonas()
    cabanas = Admin.obtener_cabanas()
    numcabanas = Admin.num_cabanas()
    fechas = Admin.obtener_calendarios()
    num_usuarios = Dash.contar_usuarios()
    total_cabanas = Dash.obtener_total_cabanas()
    porcentaje = Dash.calcular_porcentaje(total_cabanas, 40)
    total_reservaciones = Dash.contar_total_reservaciones()

    
    return render_template('admin.html', usuarios=usuarios, zonas=zonas, users_info=users_info, cabanas=cabanas, 
                           numcabanas=numcabanas, fechas=fechas, num_usuarios = num_usuarios, 
<<<<<<< Updated upstream
                           total_cabanas=total_cabanas, porcentaje=porcentaje)
=======
                           total_cabanas=total_cabanas, porcentaje=porcentaje, reservaciones=reservaciones, total_reservaciones=total_reservaciones)
>>>>>>> Stashed changes

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
        return redirect(url_for("admin"))
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
        return redirect(url_for("admin"))
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
        
       
        datos_usuarios = LlenarReporte.tabla_usuarios()
        datos_zonas = LlenarReporte.tabla_zonas()

       
        llenar_reporte = LlenarReporte(ruta_reporte_original)

       
        llenar_reporte.llenar_hoja_usuarios(datos_usuarios)

       
        llenar_reporte.llenar_hoja_zonas(datos_zonas)

       
        llenar_reporte.guardar_reporte()

        
        response = make_response(send_file(ruta_reporte_original, as_attachment=True, download_name="reporte_lleno.xlsx"))
        
        
        response.headers["Content-Disposition"] = "attachment; filename=reporte_lleno.xlsx"

        return response

    except Exception as e:
        return f"Error al generar el reporte: {e}"

#Cabañas
@app.route("/agregar_cabana", methods=["POST"])
def agregar_cabana():
    if request.method == "POST":
        nombre_cabana = request.form.get("NoCabana")
        ubicacion_cabana = request.form.get("bcnCabana")
        capacidad_cabana = request.form.get("CpdCabana")
        id_zn_cabana = request.form.get("selectZonaCbn")

        resultado = Admin.insertar_cabana(nombre_cabana, ubicacion_cabana, capacidad_cabana, id_zn_cabana)

        if resultado:
            return redirect(url_for("admin"))
        else:
            return "Hubo un error al agregar la zona."
    else:
        return redirect(url_for("admin"))

@app.route('/get_cabana_info/<int:id_cabana>', methods=['GET'])
def obtener_cabana_info(id_cabana):
    datos_cabana = GetInfos.obtener_info_cabana(id_cabana)
    print(datos_cabana)
    return jsonify({'success': True, 'cabana': datos_cabana})

@app.route("/modificar_cabana", methods=["POST"])
def modificar_cabana():
    if request.method == "POST":
        id_cbn = request.form.get("id_cbn_act")
        nombre_cabana = request.form.get("ActNoCabana")
        ubicacion_cabana = request.form.get("ActbcnCabana")
        capacidad_cabana = request.form.get("ActCpdCabana")
        id_zn_cabana = request.form.get("ActselectZonaCbn")

        resultado = Admin.actualizar_cabana(id_cbn, nombre_cabana, ubicacion_cabana, capacidad_cabana, id_zn_cabana)

        if resultado:
            return redirect(url_for("admin"))
        else:
            return "Hubo un error al agregar la zona."
    else:
        return redirect(url_for("admin"))

#Fechas
@app.route("/agregar_fecha", methods=["POST"])
def agregar_fecha():
    if request.method == "POST":
        dia = request.form.get("lblfecha")
        hora = request.form.get("lblHora")
        id_fc_cabana = request.form.get("selectfcCbn")

        resultado = Admin.insertar_fecha(dia, hora, id_fc_cabana)

        if resultado:
            return redirect(url_for("admin"))
        else:
            return "Hubo un error al agregar la zona."
    else:
        return redirect(url_for("admin"))



@app.route('/reservations_chart')
def reservations_chart():
    # Supongamos que tienes una función para obtener las reservaciones para un mes específico
    reservations_data = Dash.obtener_reservaciones_agrupadas()

    # Devuelve los datos como un objeto JSON
    return jsonify(reservations_data)



def formatear_fecha_hora(dt):    
    formato = "%Y-%m-%d %H:%M:%S"
    return dt.strftime(formato) if dt else None





if __name__ == '__main__':
    app.run(debug=True)
