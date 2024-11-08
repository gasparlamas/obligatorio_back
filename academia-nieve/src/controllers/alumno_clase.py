from database.connection import get_db_connection, close_connection

# Función para registrar el equipamiento de un alumno en una clase
def registrar_equipamiento_alumno(id_clase, ci_alumno, alquilado, id_equipamiento):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Verificar si el alumno existe
            cursor.execute("SELECT * FROM alumnos WHERE ci_alumno = %s", (ci_alumno,))
            alumno = cursor.fetchone()
            if not alumno:
                return {"error": "El alumno no existe.", "status": 404}
            
            # Verificar si la clase existe
            cursor.execute("SELECT * FROM clase WHERE id_clase = %s", (id_clase,))
            clase = cursor.fetchone()
            if not clase:
                return {"error": "La clase no existe.", "status": 404}

            # Verificar si el equipamiento existe (si se proporciona)
            if id_equipamiento:
                cursor.execute("SELECT * FROM equipamiento WHERE id_equipamiento = %s", (id_equipamiento,))
                equipamiento = cursor.fetchone()
                if not equipamiento:
                    return {"error": "El equipamiento no existe.", "status": 404}

            # Verificar si el alumno ya está registrado en otra clase en el mismo turno
            cursor.execute("""
                SELECT * FROM alumno_clase ac
                JOIN clase c ON ac.id_clase = c.id_clase
                WHERE ac.ci_alumno = %s AND c.id_turno = (SELECT id_turno FROM clase WHERE id_clase = %s)
            """, (ci_alumno, id_clase))
            conflicto_clase = cursor.fetchone()
            if conflicto_clase:
                return {"error": "El alumno ya está inscrito en otra clase en el mismo turno.", "status": 400}

            # Insertar registro en la tabla alumno_clase
            query = """
                INSERT INTO alumno_clase (id_clase, ci_alumno, alquilado, id_equipamiento)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (id_clase, ci_alumno, alquilado, id_equipamiento))
            connection.commit()
            print("Equipamiento registrado para el alumno.")
            return {"message": "Equipamiento registrado para el alumno", "status": 201}

        except Exception as e:
            print("Error al registrar el equipamiento del alumno:", str(e)) 
            connection.rollback()
            return {"error": f"Error al registrar el equipamiento del alumno: {str(e)}", "status": 500}  # Enviar el detalle
        finally:
            close_connection(connection)


# Función para ver el estado del equipamiento de un alumno en una clase
def ver_equipamiento_alumno(id_clase, ci_alumno):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT id_clase, ci_alumno, id_equipamiento, alquilado
                FROM alumno_clase
                WHERE id_clase = %s AND ci_alumno = %s
            """
            cursor.execute(query, (id_clase, ci_alumno))
            equipamiento = cursor.fetchone()
            
            if equipamiento:
                return equipamiento
            else:
                print("No se encontró registro de equipamiento para el alumno en esta clase.")
                return None

        except Exception as e:
            print("Error al obtener el equipamiento del alumno:", e)
        finally:
            close_connection(connection)

if __name__ == "__main__":
    # Prueba de registrar equipamiento de la escuela para un alumno
    registrar_equipamiento_alumno(id_clase=1, ci_alumno="10134567", alquilado=True, id_equipamiento=3)
    
    # Prueba de registrar equipamiento propio (sin id_equipamiento)
    #registrar_equipamiento_alumno(id_clase=1, ci_alumno="10034567", alquilado=False)
    
    # Prueba de ver el equipamiento de un alumno
    equipamiento = ver_equipamiento_alumno(id_clase=1, ci_alumno="10134567")
    print("Datos de equipamiento del alumno:", equipamiento)
