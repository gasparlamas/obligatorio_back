from database.connection import get_db_connection, close_connection

#Funcion para obtener todo el equipamiento

def obtener_equipamiento():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM equipamiento"
            cursor.execute(query)
            alumnos = cursor.fetchall()
            return alumnos
        except Exception as e:
            print("Error al obtener el equipamiento:", e)
        finally:
            close_connection(connection)



# Ejemplos de uso
if __name__ == "__main__":
    # Obtener el equipamiento
    obtener_equipamiento()
