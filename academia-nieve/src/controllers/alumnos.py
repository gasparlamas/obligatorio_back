from database.connection import get_db_connection, close_connection

# Función para agregar un nuevo alumno
def agregar_alumno(ci_alumno, nombre, apellido, fecha_nacimiento):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO alumnos (ci_alumno, nombre, apellido, fecha_nacimiento) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (ci_alumno, nombre, apellido, fecha_nacimiento))
            connection.commit()
            print("Alumno agregado exitosamente.")
        except Exception as e:
            print("Error al agregar el alumno:", e)
        finally:
            close_connection(connection)

# Función para inscribir un alumno en una clase, verificando restricción de turno
def inscribir_alumno_en_clase(ci_alumno, id_clase):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute("SELECT id_turno FROM clase WHERE id_clase = %s", (id_clase,))
            turno_clase = cursor.fetchone()
            
            if not turno_clase:
                print("Clase no encontrada.")
                return
            
            id_turno = turno_clase['id_turno']

            # verificar si el alumno ya está inscrito en otra clase en el mismo turno
            cursor.execute("""
                SELECT COUNT(*) AS cuenta
                FROM alumno_clase ac
                JOIN clase c ON ac.id_clase = c.id_clase
                WHERE ac.ci_alumno = %s AND c.id_turno = %s
            """, (ci_alumno, id_turno))
            resultado = cursor.fetchone()

            if resultado['cuenta'] > 0:
                print("El alumno ya está inscrito en otra clase en el mismo turno.")
            else:
                cursor.execute("""
                    INSERT INTO alumno_clase (id_clase, ci_alumno, id_equipamiento, alquilado)
                    VALUES (%s, %s, NULL, FALSE)
                """, (id_clase, ci_alumno))
                connection.commit()
                print("Alumno inscrito en la clase.")
    
        except Exception as e:
            print("Error al inscribir el alumno en la clase:", e)
            connection.rollback()
        finally:
            close_connection(connection)

# Función para obtener todos los alumnos
def obtener_alumnos():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM alumnos"
            cursor.execute(query)
            alumnos = cursor.fetchall()
            return alumnos
        except Exception as e:
            print("Error al obtener los alumnos:", e)
        finally:
            close_connection(connection)

# Función para actualizar los datos de un alumno
def actualizar_alumno(ci_alumno, nombre, apellido, fecha_nacimiento):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "UPDATE alumnos SET nombre = %s, apellido = %s, fecha_nacimiento = %s WHERE ci_alumno = %s"
            cursor.execute(query, (nombre, apellido, fecha_nacimiento, ci_alumno))
            connection.commit()
            print("Alumno actualizado exitosamente.")
        except Exception as e:
            print("Error al actualizar el alumno:", e)
        finally:
            close_connection(connection)

# funcion para eliminar un alumno

def eliminar_alumno(ci_alumno):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Eliminar los registros relacionados en alumno_clase
            query_relacionados = "DELETE FROM alumno_clase WHERE ci_alumno = %s"
            cursor.execute(query_relacionados, (ci_alumno,))
            # Eliminar el alumno en la tabla alumnos
            query_alumno = "DELETE FROM alumnos WHERE ci_alumno = %s"
            cursor.execute(query_alumno, (ci_alumno,))

            connection.commit()
            print("Alumno y registros relacionados eliminados exitosamente.")
        except Exception as e:
            print("Error al eliminar el alumno:", e)
            connection.rollback()
        finally:
            close_connection(connection)


