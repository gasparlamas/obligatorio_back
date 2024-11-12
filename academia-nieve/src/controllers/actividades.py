from database.connection import get_db_connection, close_connection

# Función para obtener todas las actividades
def obtener_actividades():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM actividades"
            cursor.execute(query)
            actividades = cursor.fetchall()  
            return actividades
        except Exception as e:
            print("Error al obtener las actividades:", e)
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
    # Prueba de obtener actividades
    obtener_actividades()  
    
    # Prueba de actualizar una actividad
    actualizar_actividad(1, "Descripción actualizada", 1500)  # Cambia el ID y los datos según sea necesario
