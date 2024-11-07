from database.connection import get_db_connection, close_connection

# Función para crear una nueva clase
def crear_clase(id_clase, ci_instructor, id_actividad, id_turno, dictada, grupal):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Verificar si el instructor ya está asignado a otra clase en el mismo turno
            cursor.execute("""
                SELECT COUNT(*) AS cuenta
                FROM clase
                WHERE ci_instructor = %s AND id_turno = %s
            """, (ci_instructor, id_turno))
            resultado = cursor.fetchone()

            if resultado[0] > 0:
                print("El instructor ya está asignado a otra clase en el mismo turno.")
                return

            # Insertar la nueva clase
            query = """
                INSERT INTO clase (id_clase, ci_instructor, id_actividad, id_turno, dictada, grupal)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (id_clase, ci_instructor, id_actividad, id_turno, dictada, grupal))
            connection.commit()
            print("Clase creada exitosamente.")
        except Exception as e:
            print("Error al crear la clase:", e)
            connection.rollback()
        finally:
            close_connection(connection)

# Función para cambiar el turno de una clase
def cambiar_turno_clase(id_clase, nuevo_turno):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Verificar si la clase ya ha sido dictada
            cursor.execute("SELECT dictada FROM clase WHERE id_clase = %s", (id_clase,))
            clase = cursor.fetchone()

            if clase and clase[0]:  # Si dictada es True
                print("No se puede cambiar el turno de una clase ya dictada.")
                return

            # Actualizar el turno
            query = "UPDATE clase SET id_turno = %s WHERE id_clase = %s"
            cursor.execute(query, (nuevo_turno, id_clase))
            connection.commit()
            print("Turno de la clase actualizado exitosamente.")
        except Exception as e:
            print("Error al cambiar el turno de la clase:", e)
            connection.rollback()
        finally:
            close_connection(connection)

# Función para cambiar el tipo de clase (grupal o individual)
def cambiar_tipo_clase(id_clase, grupal):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Verificar si la clase ya ha sido dictada
            cursor.execute("SELECT dictada FROM clase WHERE id_clase = %s", (id_clase,))
            clase = cursor.fetchone()

            if clase and clase[0]:  # Si dictada es True
                print("No se puede cambiar el tipo de una clase ya dictada.")
                return

            # Actualizar el tipo de clase
            query = "UPDATE clase SET grupal = %s WHERE id_clase = %s"
            cursor.execute(query, (grupal, id_clase))
            connection.commit()
            print("Tipo de clase actualizado exitosamente.")
        except Exception as e:
            print("Error al cambiar el tipo de clase:", e)
            connection.rollback()
        finally:
            close_connection(connection)

# Función para listar todas las clases
def listar_clases():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clase")
            clases = cursor.fetchall()
            for clase in clases:
                print(clase)
        except Exception as e:
            print("Error al listar las clases:", e)
        finally:
            close_connection(connection)

# Función para eliminar una clase (solo si no ha sido dictada)
def eliminar_clase(id_clase):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Verificar si la clase ya ha sido dictada
            cursor.execute("SELECT dictada FROM clase WHERE id_clase = %s", (id_clase,))
            clase = cursor.fetchone()

            if clase and clase[0]:  # Si dictada es True
                print("No se puede eliminar una clase ya dictada.")
                return

            # Eliminar la clase
            query = "DELETE FROM clase WHERE id_clase = %s"
            cursor.execute(query, (id_clase,))
            connection.commit()
            print("Clase eliminada exitosamente.")
        except Exception as e:
            print("Error al eliminar la clase:", e)
            connection.rollback()
        finally:
            close_connection(connection)

# Ejemplos de uso
if __name__ == "__main__":
    # Crear una nueva clase
    crear_clase(11, "91234567", 3, 3, False, True)
    
    # Cambiar el turno de una clase
    cambiar_turno_clase(3, 1)
    
    # Cambiar el tipo de clase a individual
    cambiar_tipo_clase(3, False)
    
    # Listar todas las clases
    listar_clases()
    
    # Eliminar una clase
    eliminar_clase(8)
