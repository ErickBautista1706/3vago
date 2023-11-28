from models.database import Database  
from sqlalchemy import text
from datetime import datetime


class Admin:
    def obtener_usuarios():
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
            return usuarios

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
            

    def actualizar_usuario(id_usuario, nombre, apellidoP, apellidoM, alias):
        try:
            # Conectar a la base de datos
            db = Database()
            conn = db.engine.connect()

            # Actualizar el usuario en la base de datos
            query = text("""
                UPDATE usuarios
                SET nombre = :nombre, apellidoP = :apellidoP, apellidoM = :apellidoM, alias = :alias
                WHERE id_usr = :id_usuario
            """)

            conn.execute(query, {
                'id_usuario': id_usuario,
                'nombre': nombre,
                'apellidoP': apellidoP,
                'apellidoM': apellidoM,
                'alias': alias
            })

            conn.commit()

            conn.close()

            return True
        except Exception as e:
            # Si ocurre un error, se captura y se devuelve False
            print(f"Error al actualizar usuario: {e}")
            return False
    
    def obtener_zonas():
            db = Database()
            conn = db.engine.connect()
            query = text("""
                SELECT z.*, u.nombre
                FROM zonas z
                INNER JOIN usuarios u ON z.id_usr = u.id_usr
                """)

            result = conn.execute(query)
            zonas = result.fetchall()
            conn.close()
            return zonas
                
    def insertar_zona(nombre_zn, ubicacion_zn, activo_zn, id_usr):
        try:
            # Conectar a la base de datos
            db = Database()
            conn = db.engine.connect()

            # Insertar la nueva zona en la base de datos
            query = text("""
                INSERT INTO zonas (nombre_zn, ubicacion_zn, activo_zn, id_usr, uptade_zn)
                VALUES (:nombre_zn, :ubicacion_zn, :activo_zn, :id_usr, :update_time)
            """)

            conn.execute(query, {
                'nombre_zn': nombre_zn,
                'ubicacion_zn': ubicacion_zn,
                'activo_zn': activo_zn,
                'id_usr': id_usr,
                'update_time': datetime.now()
            })

            conn.commit()
            conn.close()

            return True
        except Exception as e:
            # Si ocurre un error, se captura y se devuelve False
            print(f"Error al insertar zona: {e}")
            return False

    def eliminar_zona(id_zona):
        try:
            db = Database()
            conn = db.engine.connect()

            # Eliminar la zona con el ID proporcionado
            query = text("DELETE FROM zonas WHERE id_zn = :id_zona")
            conn.execute(query, {"id_zona": id_zona})
            
            conn.commit()
            conn.close()

            return True
        except Exception as e:
            print(f"Error al eliminar zona: {e}")
            return False
        
    def actualizar_zona(id_zn, nombre_zn, ubicacion_zn, activo_zn, id_usr):
        try:
            # Conectar a la base de datos
            db = Database()
            conn = db.engine.connect()

            # Actualizar la zona en la base de datos
            query = text("""
                UPDATE zonas
                SET nombre_zn = :nombre_zn,
                    ubicacion_zn = :ubicacion_zn,
                    activo_zn = :activo_zn,
                    id_usr = :id_usr,
                    uptade_zn = :update_time
                WHERE id_zn = :id_zn
            """)

            conn.execute(query, {
                'nombre_zn': nombre_zn,
                'ubicacion_zn': ubicacion_zn,
                'activo_zn': activo_zn,
                'id_usr': id_usr,
                'update_time': datetime.now(),
                'id_zn': id_zn
            })

            conn.commit()
            conn.close()

            return True
        except Exception as e:
            # Si ocurre un error, se captura y se devuelve False
            print(f"Error al actualizar zona: {e}")
            return False
