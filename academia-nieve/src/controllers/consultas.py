from database.connection import get_db_connection, close_connection
import datetime
# Consulta para obtener actividades que más ingresos generan (sumando costo de equipamiento y el costo de la actividad)

def obtener_actividades_con_mas_ingresos():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT
                    a.descripcion AS actividad,
                    SUM(a.costo + CASE WHEN e.costo IS NULL THEN 0 ELSE e.costo END) AS ingreso_total
                    FROM actividades a
                    JOIN clase c ON a.id_actividad = c.id_actividad
                    JOIN alumno_clase ac ON c.id_clase = ac.id_clase
                    LEFT JOIN equipamiento e ON ac.id_equipamiento = e.id_equipamiento AND ac.alquilado = TRUE
                    GROUP BY a.id_actividad, a.descripcion
                    ORDER BY ingreso_total DESC
                    LIMIT 3;
                 """
            cursor.execute(query)
            actividades = cursor.fetchall()

            if actividades:
                return actividades
            else:
                print("No se encontraron actividades con ingresos registrados.")
                return None
        except Exception as e:
            print("Error al obtener los ingresos de las actividades:", e)
        finally:    
            close_connection(connection)



#Consulta para obtener las actividades con más alumnos inscritos

def obtener_actividades_con_mas_alumnos():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT 
                a.id_actividad, 
                a.descripcion,
                COUNT(ac.ci_alumno) AS total_alumnos
                FROM actividades a
                INNER JOIN clase c ON a.id_actividad = c.id_actividad  
                INNER JOIN alumno_clase ac ON c.id_clase = ac.id_clase
                INNER JOIN alumnos al ON ac.ci_alumno = al.ci_alumno
                GROUP BY a.id_actividad, a.descripcion
                ORDER BY total_alumnos DESC
                LIMIT 3;
                    """
            cursor.execute(query)
            actividades = cursor.fetchall()

            if actividades:
                return actividades
            else:
                print("No se encontraron actividades con más alumnos inscritos.")
                return None

        except Exception as e:
            print("Error al obtener las actividades con más alumnos inscritos:", e)
        finally:
            close_connection(connection)


#Consulta para obtener los turnos con más clases dictadas

def obtener_turnos_con_mas_clases_dictadas():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT 
                t.id_turno, 
                t.hora_inicio,
                t.hora_fin,
                COUNT(c.id_clase) AS total_clases_dictadas
                FROM turnos t
                INNER JOIN clase c ON t.id_turno = c.id_turno
                WHERE c.dictada = TRUE
                GROUP BY t.id_turno, t.hora_inicio, t.hora_fin
                ORDER BY total_clases_dictadas DESC
                LIMIT 3;
            """
            cursor.execute(query)
            turnos = cursor.fetchall()

            # Convertir timedelta a string
            for turno in turnos:
                if isinstance(turno['hora_inicio'], datetime.timedelta):
                    turno['hora_inicio'] = str(turno['hora_inicio'])
                if isinstance(turno['hora_fin'], datetime.timedelta):
                    turno['hora_fin'] = str(turno['hora_fin'])

            return turnos
        except Exception as e:
            print("Error al obtener los turnos con más clases dictadas:", e)
        finally:
            close_connection(connection)



