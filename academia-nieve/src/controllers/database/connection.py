import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Cambia si usas otro host
            user="root",  # Usuario de tu base de datos
            password="rootpassword",  # Contraseña de tu usuario
            database="obligatorioBD"  # Nombre de la base de datos
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos")
        return connection

    except Error as e:
        print("Error al conectar con la base de datos", e)
        return None

def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Conexión a la base de datos cerrada")
    
if __name__ == "__main__":
    connection = get_db_connection()   # Llama a la función de conexión
    if connection:                     # Si la conexión fue exitosa
        print("Conexión establecida.") # Muestra un mensaje de éxito
        connection.close()             # Cierra la conexión