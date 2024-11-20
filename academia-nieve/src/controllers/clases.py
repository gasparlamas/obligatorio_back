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
                print("El instructor ya está asignado a otra clase en el mismo turno.")
                return
            
            query = """
                INSERT INTO clase (id_clase, ci_instructor, id_actividad, id_turno, dictada, grupal)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (id_clase, ci_instructor, id_actividad, id_turno, dictada, grupal))
            connection.commit()
            print("Clase creada exitosamente.")
        except Exception as e:
            print("Error al crear la clase:", e)
            connection.rollback()
        finally:
            close_connection(connection)

#Funcion para cambiar el instructor de una clase
def cambiar_instructor_clase(id_clase, ci_instructor):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Verificar si la clase ya está asignada
            cursor.execute("SELECT ci_instructor FROM clase WHERE id_clase = %s", (id_clase,))
            clase = cursor.fetchone()

            if clase and clase[0] != ci_instructor:  # Si el instructor no es el mismo
                query = "UPDATE clase SET ci_instructor = %s WHERE id_clase = %s"
                cursor.execute(query, (ci_instructor, id_clase))
                connection.commit()
                print("Instructor de la clase actualizado exitosamente.")
            else:
                print("No se puede cambiar el instructor de la clase ya asignada.")
                return "clase_asignada"
        except Exception as e:
            print("Error al cambiar el instructor de la clase:", e)
            connection.rollback()
        finally:    
            close_connection(connection)

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

#Funcion para cambiar turno de una clase
def cambiar_turno_clase(id_clase, id_turno):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Verificar si la clase ya ha fue dictada
            cursor.execute("SELECT dictada FROM clase WHERE id_clase = %s", (id_clase,))
            clase = cursor.fetchone()

            if clase and clase[0]:  # Si dictada es True
                print("No se puede cambiar el turno de una clase ya dictada.")
                return "clase_dictada"

            # Actualizar el turno
            query = "UPDATE clase SET id_turno = %s WHERE id_clase = %s"
            cursor.execute(query, (id_turno, id_clase))
            connection.commit()
            print("Turno de la clase actualizado exitosamente.")
        except Exception as e:
            print("Error al cambiar el turno de la clase:", e)
            connection.rollback()
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




 
