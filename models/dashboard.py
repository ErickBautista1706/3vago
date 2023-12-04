from models.adm import Admin
from models.database import Database  
from sqlalchemy import text

class Dash:
    def contar_usuarios():
        usuarios = Admin.obtener_usuarios()

        
        num_usuarios = len(usuarios)

        return num_usuarios
    
    def obtener_total_cabanas():
        db = Database()
        conn = db.engine.connect()
        
        query = text("""
            SELECT COUNT(*) as total_cabanas
            FROM cabanas
        """)

        result = conn.execute(query)
        total_cabanas = result.fetchone()[0]  
        conn.close()
        
        return total_cabanas

    def calcular_porcentaje(valor_actual, valor_total):
        if valor_total == 0:
            return 0

        porcentaje = (valor_actual / valor_total) * 100
        return round(porcentaje, 2)

    def obtener_reservaciones_agrupadas():
        try:
            db = Database()
            conn = db.engine.connect()
            query = text("""
                SELECT id_cbn, COUNT(*) as cantidad_reservaciones
                FROM reservaciones
                GROUP BY id_cbn
            """)

            result = conn.execute(query)
            reservaciones_agrupadas = [{'id_cbn': row.id_cbn, 'cantidad_reservaciones': row.cantidad_reservaciones} for row in result.fetchall()]

            conn.close()

            return reservaciones_agrupadas

        except Exception as e:
            print(f"Error al obtener información de reservaciones: {e}")
            return []

    def contar_total_reservaciones():
            try:
                db = Database()
                conn = db.engine.connect()
                query = text("""
                    SELECT COUNT(*) as total_reservaciones
                    FROM reservaciones
                """)

                result = conn.execute(query)
                total_reservaciones = result.scalar()
                print(total_reservaciones)
                conn.close()

                return total_reservaciones

            except Exception as e:
                print(f"Error al contar reservaciones: {e}")
                return 0
