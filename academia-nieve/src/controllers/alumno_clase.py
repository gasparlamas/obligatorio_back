from database.connection import get_db_connection, close_connection

# Función para registrar el equipamiento usado por un alumno en una clase
def registrar_equipamiento_alumno(id_clase, ci_alumno, alquilado, id_equipamiento=None):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Si el alumno usa el equipamiento de la escuela (alquilado = True)
            if alquilado:
                if id_equipamiento is None:
                    print("Se requiere el ID de equipamiento proporcionado por la escuela.")
                    return
                
                # Insertar registro con el equipamiento de la escuela y alquilado = True
                query = """
                    INSERT INTO alumno_clase (id_clase, ci_alumno, id_equipamiento, alquilado)
                    VALUES (%s, %s, %s, TRUE)
                """
                cursor.execute(query, (id_clase, ci_alumno, id_equipamiento))
            else:
                # Insertar registro sin equipamiento (id_equipamiento = NULL) y alquilado = False
                query = """
                    INSERT INTO alumno_clase (id_clase, ci_alumno, id_equipamiento, alquilado)
                    VALUES (%s, %s, NULL, FALSE)
                """
                cursor.execute(query, (id_clase, ci_alumno))

            connection.commit()
            print("Registro de equipamiento para el alumno completado.")

        except Exception as e:
            print("Error al registrar el equipamiento del alumno:", e)
            connection.rollback()
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
