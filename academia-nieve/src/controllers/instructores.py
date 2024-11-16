from database.connection import get_db_connection, close_connection


# Función para agregar un nuevo instructor
def agregar_instructor(ci_instructor, nombre, apellido):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO instructores (ci_instructor, nombre, apellido) VALUES (%s, %s, %s)"
            cursor.execute(query, (ci_instructor, nombre, apellido))
            connection.commit()
            print("Instructor agregado exitosamente.")
        except Exception as e:
            print("Error al agregar el instructor:", e)
        finally:
            close_connection(connection)


# Función para obtener todos los instructores
def obtener_instructores():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM instructores"  
            cursor.execute(query)
            instructores = cursor.fetchall()
            return instructores
        except Exception as e:
            print("Error al obtener el instructor:", e)
        finally:
            close_connection(connection)

# Función para actualizar los datos de un instructor
def actualizar_instructor(ci_instructor, nombre, apellido):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "UPDATE instructores SET nombre = %s, apellido = %s WHERE ci_instructor = %s"  
            cursor.execute(query, (nombre, apellido, ci_instructor))
            connection.commit()
            print("Instructor actualizado exitosamente.")
        except Exception as e:
            print("Error al actualizar el instructor:", e)
        finally:
            close_connection(connection)


#Funcion para eliminar un instructor
def eliminar_instructor(ci_instructor):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Eliminar las referencias en alumno_clase para todas las clases del instructor
            delete_alumno_clase_query = """
                DELETE FROM alumno_clase
                WHERE id_clase IN (
                    SELECT id_clase FROM clase WHERE ci_instructor = %s
                )
            """
            cursor.execute(delete_alumno_clase_query, (ci_instructor,))

            # Eliminar las clases asociadas a este instructor en clase
            delete_clases_query = "DELETE FROM clase WHERE ci_instructor = %s"
            cursor.execute(delete_clases_query, (ci_instructor,))

            # Eliminar el instructor en instructores
            delete_instructor_query = "DELETE FROM instructores WHERE ci_instructor = %s"
            cursor.execute(delete_instructor_query, (ci_instructor,))

            # Confirmar todos los cambios
            connection.commit()
            print("Instructor y clases asociadas eliminados exitosamente.")
        except Exception as e:
            print("Error al eliminar el instructor:", e)
            connection.rollback()
        finally:
            close_connection(connection)



# Función para ver las clases asignadas a un instructor
def ver_clases_asignadas(ci_instructor):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT clase.id_clase, actividad.descripcion AS actividad, turno.hora_inicio AS turno, clase.dictada, clase.grupal
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

