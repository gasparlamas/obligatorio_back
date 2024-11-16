import mysql.connector
from mysql.connector import Error


# conexion a la base de datos MySQL
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",  
            user="root",  
            password="rootpassword",  
            database="obligatorioBD"  
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
    
