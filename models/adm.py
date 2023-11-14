from flask import Flask, render_template
from models.database import Database  # Importa la clase Database desde models/database
from sqlalchemy import text

class Admin:
    def mostrar_usuarios():
        db = Database()

        conn = db.engine.connect()
        query = text("""
                SELECT u.id_usr, 
                    u.nombre || ' ' || u.apellidoP || ' ' || u.apellidoM AS nombre,
                    u.alias,
                    u.email,
                    t.tipo_usr
                FROM usuarios u
                JOIN tipo_usuario t ON u.id_tuser = t.id_tpurs
                """)

        result = conn.execute(query)

        usuarios = result.fetchall()
        conn.close()

        # Renderiza una plantilla HTML con los datos 
        return render_template('admin.html', usuarios=usuarios)

    def insertar_usuario(nombre, apellidoP, apellidoM, alias, email, psw, tipoUsuario):
        try:
            # Conectar a la base de datos
            db = Database()
            conn = db.engine.connect()

            # Insertar el nuevo usuario en la base de datos
            query = text("""
                INSERT INTO usuarios (nombre, apellidoP, apellidoM, alias, email, psw, id_tuser)
                VALUES (:nombre, :apellidoP, :apellidoM, :alias, :email, :psw, :tipoUsuario)
            """)
            
            conn.execute(query, {
                'nombre': nombre,
                'apellidoP': apellidoP,
                'apellidoM': apellidoM,
                'alias': alias,
                'email': email,
                'psw': psw,
                'tipoUsuario': tipoUsuario
            })
            
            conn.commit()  

            conn.close()
            
            return True
        except Exception as e:
            # Si ocurre un error, se captura y se devuelve False
            print(f"Error al insertar usuario: {e}")
            return False
        
    def eliminar_usuario(id_usuario):
            try:
                # Conectar a la base de datos
                db = Database()
                conn = db.engine.connect()

                # Eliminar el usuario de la base de datos
                query = text("DELETE FROM usuarios WHERE id_usr = :id_usuario")
                conn.execute(query, {'id_usuario': id_usuario})

                conn.commit()
                conn.close()

                return True
            except Exception as e:
                # Si ocurre un error, se captura y se devuelve False
                print(f"Error al eliminar usuario: {e}")
                return False
        
   
