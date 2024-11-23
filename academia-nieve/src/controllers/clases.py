from database.connection import get_db_connection, close_connection

# Función para crear una nueva clase
def crear_clase(id_clase, ci_instructor, id_actividad, id_turno, dictada, grupal):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Verificar si el instructor ya está asignado a otra clase en el mismo turno
            cursor.execute("""
                SELECT COUNT(*) AS cuenta
                FROM clase
                WHERE ci_instructor = %s AND id_turno = %s
            """, (ci_instructor, id_turno))
            resultado = cursor.fetchone()

            if resultado[0] > 0:
                return {"success": False, "message": "El instructor ya está asignado a otra clase en el mismo turno."}
            
            query = """
                INSERT INTO clase (id_clase, ci_instructor, id_actividad, id_turno, dictada, grupal)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (id_clase, ci_instructor, id_actividad, id_turno, dictada, grupal))
            connection.commit()
            return {"success": True, "message": "Clase creada exitosamente."}
        except Exception as e:
            # Capturar errores de clave primaria duplicada
            if "1062" in str(e):
                return {"success": False, "message": "Error: La ID de la clase ya está en uso. Por favor, elija otra."}
            # Capturar cualquier otro error
            return {"success": False, "message": f"Error al crear la clase: {e}"}
        finally:
            close_connection(connection)


def cambiar_instructor_clase(id_clase, ci_instructor):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Obtener el turno de la clase actual
            cursor.execute("SELECT id_turno FROM clase WHERE id_clase = %s", (id_clase,))
            turno_actual = cursor.fetchone()
            if not turno_actual:
                print("La clase no existe.")
                return "clase_no_existente"
            id_turno = turno_actual[0]
            # Verificar si el instructor ya tiene una clase en ese turno
            cursor.execute(
                "SELECT id_clase FROM clase WHERE ci_instructor = %s AND id_turno = %s AND id_clase != %s",
                (ci_instructor, id_turno, id_clase),
            )
            clase_conflictiva = cursor.fetchone()
            if clase_conflictiva:
                print("El instructor ya tiene otra clase asignada en el mismo turno.")
                return "instructor_duplicado"
            # Verificar si la clase ya tiene un instructor asignado y si es diferente
            cursor.execute("SELECT ci_instructor FROM clase WHERE id_clase = %s", (id_clase,))
            clase = cursor.fetchone()

            if clase and clase[0] == ci_instructor:  # Mismo instructor
                print("El instructor ya está asignado a la clase.")
                return "clase_asignada"

            # Actualizar el instructor
            query = "UPDATE clase SET ci_instructor = %s WHERE id_clase = %s"
            cursor.execute(query, (ci_instructor, id_clase))
            connection.commit()
            print("Instructor de la clase actualizado exitosamente.")
        except Exception as e:
            print("Error al cambiar el instructor de la clase:", e)
            connection.rollback()
            return "error_servidor"
        finally:
            close_connection(connection)
    else:
        print("Error al conectar a la base de datos.")
        return "error_servidor"

    return "exito"

#Funcion para cambiar la actividad de una clase
def cambiar_actividad_clase(id_clase, id_actividad):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Verificar si la clase ya está asignada
            cursor.execute("SELECT id_actividad FROM clase WHERE id_clase = %s", (id_clase,))
            clase = cursor.fetchone()

            if clase and clase[0] != id_actividad:  # Si la actividad no es la misma
                query = "UPDATE clase SET id_actividad = %s WHERE id_clase = %s"
                cursor.execute(query, (id_actividad, id_clase))
                connection.commit()
                print("Actividad de la clase actualizada exitosamente.")
            else:
                print("No se puede cambiar la actividad de la clase ya asignada.")
                return "clase_asignada"
        except Exception as e:
            print("Error al cambiar la actividad de la clase:", e)
            connection.rollback()
        finally:    
            close_connection(connection)

# Función para cambiar turno de una clase
def cambiar_turno_clase(id_clase, id_turno):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT dictada, ci_instructor FROM clase WHERE id_clase = %s", (id_clase,))
            clase = cursor.fetchone()
            if not clase:
                print("Clase no encontrada.")
                return "clase_no_existente"
            if clase[0]:  # Si dictada es True
                print("No se puede cambiar el turno de una clase ya dictada.")
                return "clase_dictada"

            ci_instructor = clase[1]
            if ci_instructor:
                # Verificar si el instructor ya está asignado a otra clase en el turno solicitado
                cursor.execute(
                    "SELECT id_clase FROM clase WHERE ci_instructor = %s AND id_turno = %s AND id_clase != %s",
                    (ci_instructor, id_turno, id_clase)
                )
                conflicto = cursor.fetchone()

                if conflicto:
                    print(f"El instructor {ci_instructor} ya tiene otra clase en el turno {id_turno}.")
                    return "instructor_duplicado"

            query = "UPDATE clase SET id_turno = %s WHERE id_clase = %s"
            cursor.execute(query, (id_turno, id_clase))
            connection.commit()
            print("Turno de la clase actualizado exitosamente.")
            return "exito"
        except Exception as e:
            print("Error al cambiar el turno de la clase:", e)
            connection.rollback()
            return "error_servidor"
        finally:
            close_connection(connection)




# Función para cambiar el tipo de clase (grupal o individual)
def cambiar_tipo_clase(id_clase, grupal):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Verificar si la clase ya fue dictada
            cursor.execute("SELECT dictada FROM clase WHERE id_clase = %s", (id_clase,))
            clase = cursor.fetchone()

            if clase and clase[0]:  # Si dictada es True
                print("No se puede cambiar el tipo de una clase ya dictada.")
                return "clase_dictada"

            # Actualizar el tipo de clase
            query = "UPDATE clase SET grupal = %s WHERE id_clase = %s"
            cursor.execute(query, (grupal, id_clase))
            connection.commit()
            print("Tipo de clase actualizado exitosamente.")
        except Exception as e:
            print("Error al cambiar el tipo de clase:", e)
            connection.rollback()
        finally:
            close_connection(connection)

# Función para cambiar si la clase esta o no dictada
def cambiar_estado_clase(id_clase, dictada):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Actualizar el tipo de clase
            query = "UPDATE clase SET dictada = %s WHERE id_clase = %s"
            cursor.execute(query, (dictada, id_clase))
            connection.commit()
            print("Estado de clase actualizado exitosamente.")
        except Exception as e:
            print("Error al cambiar el estado de clase:", e)
            connection.rollback()
        finally:
            close_connection(connection)

# Función para listar todas las clases
def listar_clases():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clase")
            clases = cursor.fetchall()
            return clases
        except Exception as e:
            print("Error al listar las clases:", e)
        finally:
            close_connection(connection)




 
