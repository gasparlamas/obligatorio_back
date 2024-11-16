from database.connection import get_db_connection, close_connection

# Función para agregar un nuevo turno
def agregar_turno(id_turno, hora_inicio, hora_fin):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO turnos (id_turno, hora_inicio, hora_fin) VALUES (%s, %s, %s)"
            cursor.execute(query, (id_turno, hora_inicio, hora_fin))
            connection.commit()
            print("Turno agregado exitosamente.")
        except Exception as e:
            print("Error al agregar el turno:", e)
        finally:
            close_connection(connection)


# Función para actualizar los datos de un turno
def actualizar_turno(id_turno, hora_inicio, hora_fin):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "UPDATE turnos SET hora_inicio = %s, hora_fin = %s WHERE id_turno = %s"
            cursor.execute(query, (hora_inicio, hora_fin, id_turno))
            connection.commit()
            print("Turno actualizado exitosamente.")
        except Exception as e:
            print("Error al actualizar el turno:", e)
        finally:
            close_connection(connection)

# Función para eliminar un turno
def eliminar_turno(id_turno):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM turnos WHERE id_turno = %s"
            cursor.execute(query, (id_turno,))
            connection.commit()
            print("Turno eliminado exitosamente.")
        except Exception as e:
            print("Error al eliminar el turno:", e)
        finally:
            close_connection(connection)

# Función para obtener todos los turnos
def obtener_turnos():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM turnos"
            cursor.execute(query)
            turnos = cursor.fetchall()  # Obtener todas las filas como diccionarios

            # Convertir valores de hora_inicio y hora_fin a formato "HH:MM:SS"
            for turno in turnos:
                turno['hora_inicio'] = str(turno['hora_inicio'])
                turno['hora_fin'] = str(turno['hora_fin'])

            return turnos
        except Exception as e:
            print("Error al obtener los turnos:", e)
        finally:
            close_connection(connection)


