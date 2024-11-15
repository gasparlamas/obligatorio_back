from database.connection import get_db_connection, close_connection


def validar_login(correo, contraseña):
    connection = get_db_connection()
    if not connection:
        return {"success": False, "message": "No se pudo conectar a la base de datos"}

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT correo, contraseña FROM login WHERE correo = %s"
        cursor.execute(query, (correo,))
        user = cursor.fetchone()

        if user and user["contraseña"] == contraseña:
            return {"success": True, "message": "Inicio de sesión exitoso", "user": user["correo"]}
        else:
            return {'success': False, 'message': 'Correo o contraseña incorrectos'}

    except Exception as e:
        return {"success": False, "message": f"Error en el servidor: {str(e)}"}

    finally:
        cursor.close()
        close_connection(connection)