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

# Función para obtener un turno por id
def obtener_turno(id_turno):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM turnos WHERE id_turno = %s"
            cursor.execute(query, (id_turno,))
            turno = cursor.fetchone()

            # Convertir los valores de hora_inicio y hora_fin a formato "HH:MM:SS"
            if turno:
                id_turno, hora_inicio, hora_fin = turno
                hora_inicio = str(hora_inicio)
                hora_fin = str(hora_fin)
                return (id_turno, hora_inicio, hora_fin)
        except Exception as e:
            print("Error al obtener el turnp:", e)
        finally:
            close_connection(connection)

if __name__ == "__main__":
    # Prueba de agregar un turno
    agregar_turno("4", "18:30:00", "21:00:00")
    
    
    # Prueba de obtener un turno
    turno = obtener_turno("4")
    print("Datos del turno:", turno)
    
    # Prueba de actualizar un turno
    actualizar_turno("4", "19:00:00", "22:00:00")
    
    # Prueba de eliminar un alumno
    eliminar_turno("4")