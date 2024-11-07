from database.connection import get_db_connection, close_connection

# Función para obtener un instructor por CI
def obtener_instructor(ci):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM instructores WHERE ci_instructor = %s"  
            cursor.execute(query, (ci,))
            instructor = cursor.fetchone()
            return instructor
        except Exception as e:
            print("Error al obtener el instructor:", e)
        finally:
            close_connection(connection)

# Función para actualizar los datos de un instructor
def actualizar_instructor(ci, nombre, apellido):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "UPDATE instructores SET nombre = %s, apellido = %s WHERE ci_instructor = %s"  
            cursor.execute(query, (nombre, apellido, ci))
            connection.commit()
            print("Instructor actualizado exitosamente.")
        except Exception as e:
            print("Error al actualizar el instructor:", e)
        finally:
            close_connection(connection)

# Función para eliminar un instructor
def eliminar_instructor(ci):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM instructores WHERE ci_instructor = %s" 
            cursor.execute(query, (ci,))
            connection.commit()
            print("Instructor eliminado exitosamente.")
        except Exception as e:
            print("Error al eliminar el instructor:", e)
        finally:
            close_connection(connection)

# Función para ver las clases asignadas a un instructor
def ver_clases_asignadas(ci_instructor):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT clase.id_clase, actividad.nombre AS actividad, turno.horario AS turno, clase.dictada, clase.grupal
                FROM clase
                JOIN actividades AS actividad ON clase.id_actividad = actividad.id_actividad
                JOIN turnos AS turno ON clase.id_turno = turno.id_turno
                WHERE clase.ci_instructor = %s
            """
            cursor.execute(query, (ci_instructor,))
            clases = cursor.fetchall()
            return clases
        except Exception as e:
            print("Error al obtener las clases asignadas:", e)
        finally:
            close_connection(connection)

if __name__ == "__main__":
    # Prueba de obtener un instructor
    instructor = obtener_instructor("12345678")
    print("Datos del instructor:", instructor)
    
    # Prueba de actualizar un instructor
    actualizar_instructor("87654321", "María", "Fernández")
    
    # Prueba de eliminar un instructor
    eliminar_instructor("87654321")
    
    # Prueba de ver clases asignadas
    clases_asignadas = ver_clases_asignadas("12345678")
    print("Clases asignadas al instructor:", clases_asignadas)
