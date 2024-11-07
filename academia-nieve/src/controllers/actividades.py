from database.connection import get_db_connection, close_connection

# Función para obtener una actividad por ID
def obtener_actividad(id_actividad):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM actividades WHERE id_actividad = %s"
            cursor.execute(query, (id_actividad,))
            actividad = cursor.fetchone()
            return actividad
        except Exception as e:
            print("Error al obtener la actividad:", e)
        finally:
            close_connection(connection)

# Función para actualizar los datos de una actividad
def actualizar_actividad(id_actividad, descripcion, costo):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "UPDATE actividades SET descripcion = %s, costo = %s WHERE id_actividad = %s"
            cursor.execute(query, (descripcion, costo, id_actividad))
            connection.commit()
            print("Actividad actualizada exitosamente.")
        except Exception as e:
            print("Error al actualizar la actividad:", e)
        finally:
            close_connection(connection)

if __name__ == "__main__":
    # Prueba de obtener una actividad
    actividad = obtener_actividad(1)  # Cambia el ID según lo necesites
    print("Datos de la actividad:", actividad)
    
    # Prueba de actualizar una actividad
    actualizar_actividad(1, "Descripción actualizada", 1500)  # Cambia el ID y los datos según lo necesites
