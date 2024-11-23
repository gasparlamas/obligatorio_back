from flask import Flask, request, jsonify,session
from flask_cors import CORS 
from database.connection import get_db_connection, close_connection
from instructores import  agregar_instructor,obtener_instructores, actualizar_instructor, eliminar_instructor, ver_clases_asignadas
from alumnos import agregar_alumno,inscribir_alumno_en_clase, obtener_alumnos, actualizar_alumno, eliminar_alumno
from clases import crear_clase, cambiar_turno_clase,cambiar_tipo_clase, cambiar_estado_clase, listar_clases, cambiar_instructor_clase, cambiar_actividad_clase
from alumno_clase import registrar_equipamiento_alumno, ver_equipamiento_alumno
from turnos import agregar_turno, actualizar_turno, obtener_turnos, eliminar_turno
from actividades import obtener_actividades, actualizar_actividad
from equipamiento import obtener_equipamiento
from consultas import obtener_actividades_con_mas_ingresos, obtener_actividades_con_mas_alumnos, obtener_turnos_con_mas_clases_dictadas
from login import validar_login, registrar_usuario

app = Flask(__name__)
app.secret_key = 't3E@1R9%q2!aWz8~4^X9J3!kLp0oZ5YfR'  #clave para el login
CORS(app)  #habilita CORS para todas las rutas y permite solicitudes de cualquier origen
# para SOLO dar acceso al frontend se puede especificar: CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# ------------------------- ENDPOINTS Instructores -------------------------

@app.route("/api/instructores", methods=["POST"])
def api_agregar_instructor():
    data = request.json
    ci_instructor = data.get("ci_instructor")
    nombre = data.get("nombre")
    apellido = data.get("apellido")

    # Validar que el CI sea numérico
    if not ci_instructor or not ci_instructor.isdigit():
        return jsonify({"error": "El CI debe contener solo números."}), 400
    
    # Validar que el nombre no supere los 20 caracteres
    if not nombre or len(nombre) > 20:
        return jsonify({"error": "El nombre no debe superar los 20 caracteres."}), 400
    
    # Validar que el apellido no supere los 20 caracteres
    if not apellido or len(apellido) > 20:
        return jsonify({"error": "El apellido no debe superar los 20 caracteres."}), 400

    try:
        agregar_instructor(ci_instructor, nombre, apellido)
        return jsonify({"message": "Instructor agregado exitosamente"}), 201
    except Exception as e:
        print("Error al agregar el instructor:", e)
        return jsonify({"error": "Error al agregar el Instructor."}), 500


@app.route("/api/instructores", methods=["GET"])
def api_obtener_instructores():
    instructores = obtener_instructores()
    return jsonify(instructores)

@app.route("/api/instructores/<ci_instructor>", methods=["PUT"])
def api_actualizar_instructor(ci_instructor):
    data = request.json
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    actualizar_instructor(ci_instructor, nombre, apellido)
    return jsonify({"message": "Instructor actualizado exitosamente"})

@app.route("/api/instructores/<ci_instructor>", methods=["DELETE"])
def api_eliminar_instructor(ci_instructor):
    eliminar_instructor(ci_instructor)
    return jsonify({"message": "Instructor eliminado exitosamente"})

@app.route("/api/instructores/<ci_instructor>/clases", methods=["GET"])
def api_ver_clases_asignadas(ci_instructor):
    clases = ver_clases_asignadas(ci_instructor)
    if clases:
        return jsonify(clases), 200
    else:
        return jsonify({"message": "No se encontraron clases asignadas para este instructor"}), 404

# ------------------------- ENDPOINTS Alumnos -------------------------

@app.route("/api/alumnos", methods=["POST"])
def api_agregar_alumno():
    data = request.json
    ci_alumno = data.get("ci_alumno")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    fecha_nacimiento = data.get("fecha_nacimiento")

    # Validar que el CI sea numérico
    if not ci_alumno or not ci_alumno.isdigit():
        return jsonify({"error": "El CI debe contener solo números."}), 400
    
     # Validar que el nombre no supere los 20 caracteres
    if not nombre or len(nombre) > 20:
        return jsonify({"error": "El nombre no debe superar los 20 caracteres."}), 400
    
    # Validar que el apellido no supere los 20 caracteres
    if not apellido or len(apellido) > 20:
        return jsonify({"error": "El apellido no debe superar los 20 caracteres."}), 400

    try:
        agregar_alumno(ci_alumno, nombre, apellido, fecha_nacimiento)
        return jsonify({"message": "Alumno agregado exitosamente"}), 201
    except Exception as e:
        print("Error al agregar el alumno:", e)
        return jsonify({"error": "Error al agregar el alumno."}), 500

@app.route("/api/alumnos/<ci_alumno>/inscripcion", methods=["POST"])
def api_inscribir_alumno_en_clase(ci_alumno):
    data = request.json
    id_clase = data.get("id_clase")
    
    # Llamar a la función para inscribir al alumno en la clase
    inscribir_alumno_en_clase(ci_alumno, id_clase)
    
    return jsonify({"message": "Alumno inscrito en la clase exitosamente"}), 201

@app.route("/api/alumnos", methods=["GET"])
def api_obtener_alumnos():
    alumnos = obtener_alumnos()
    return jsonify(alumnos)

@app.route("/api/alumnos/<ci_alumno>", methods=["PUT"])
def api_actualizar_alumno(ci_alumno):
    data = request.json
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    fecha_nacimiento = data.get("fecha_nacimiento")
    actualizar_alumno(ci_alumno, nombre, apellido,fecha_nacimiento)
    return jsonify({"message": "Alumno actualizado exitosamente"})

@app.route("/api/alumnos/<ci_alumno>", methods=["DELETE"])
def api_eliminar_alumno(ci_alumno):
    eliminar_alumno(ci_alumno)
    return jsonify({"message": "Alumno eliminado exitosamente"})

# ------------------------- ENDPOINTS Clases -------------------------
@app.route("/api/clases", methods=["POST"])
def api_crear_clase():
    data = request.json
    id_clase = data.get("id_clase")
    ci_instructor = data.get("ci_instructor")
    id_actividad = data.get("id_actividad")
    id_turno = data.get("id_turno")
    dictada = data.get("dictada")
    grupal = data.get("grupal")

    # Llamar a la función crear_clase y manejar la respuesta
    resultado = crear_clase(id_clase, ci_instructor, id_actividad, id_turno, dictada, grupal)

    if resultado["success"]:
        return jsonify({"message": resultado["message"]}), 201
    else:
        return jsonify({"message": resultado["message"]}), 400
    if resultado["success"]:
        return jsonify({"message": resultado["message"]}), 201
    else:
        return jsonify({"message": resultado["message"]}), 400

@app.route("/api/clases/<int:id_clase>/instructor", methods=["PUT"])
def api_cambiar_instructor_clase(id_clase):
    # Obtener el instructor desde el cuerpo de la solicitud JSON
    data = request.json
    ci_instructor = data.get("ci_instructor")

    if not ci_instructor:
        return jsonify({"error": "El campo 'ci_instructor' es obligatorio"}), 400

    # Llamar a la función que cambia el instructor de la clase
    resultado = cambiar_instructor_clase(id_clase, ci_instructor)

    if resultado == "clase_asignada":
        return jsonify({"error": "El instructor ya está asignado a esta clase"}), 400
    elif resultado == "instructor_duplicado":
        return jsonify({"error": "El instructor ya tiene otra clase en el turno seleccionado"}), 400
    elif resultado == "clase_no_existente":
        return jsonify({"error": "La clase no existe"}), 404
    elif resultado == "error_servidor":
        return jsonify({"error": "Error interno del servidor"}), 500

    # Responder con un mensaje de éxito
    return jsonify({"message": "Instructor de la clase actualizado exitosamente"}), 200



@app.route("/api/clases/<int:id_clase>/actividad", methods=["PUT"])
def api_cambiar_actividad_clase(id_clase):
    # Obtener la actividad desde el cuerpo de la solicitud json
    data = request.json
    id_actividad = data.get("id_actividad")

    # Llamar a la función que cambia la actividad de la clase
    resultado = cambiar_actividad_clase(id_clase, id_actividad)

    # Si la clase ya está asignada, retornar un error
    if resultado == "clase_asignada":
        return jsonify({"error": "No se puede cambiar la actividad de una clase ya asignada"}), 400

    # Responder con un mensaje de éxito
    return jsonify({"message": "Actividad de la clase actualizada exitosamente"}), 200


@app.route("/api/clases/<int:id_clase>/turno/<int:id_turno>", methods=["PUT"])
def api_cambiar_turno_clase(id_clase, id_turno):
    # Llamar a la función que cambia el turno de la clase
    resultado = cambiar_turno_clase(id_clase, id_turno)

    if resultado == "clase_dictada":
        return jsonify({"error": "No se puede cambiar el turno de una clase ya dictada"}), 400
    elif resultado == "instructor_duplicado":
        return jsonify({"error": "El instructor ya tiene otra clase en el turno seleccionado"}), 400
    elif resultado == "clase_no_existente":
        return jsonify({"error": "La clase no existe"}), 404
    elif resultado == "error_servidor":
        return jsonify({"error": "Error interno del servidor"}), 500

    # Responder con un mensaje de éxito
    return jsonify({"message": "Turno de la clase actualizado exitosamente"}), 200



@app.route("/api/clases/<int:id_clase>/tipo", methods=["PUT"])
def api_cambiar_tipo_clase(id_clase):
    # Obtener el tipo de clase (grupal o individual) desde el cuerpo de la solicitud json
    data = request.json
    grupal = data.get("grupal")

    # Llamar a la función que cambia el tipo de clase
    resultado = cambiar_tipo_clase(id_clase, grupal)

    # Si la clase ya está dictada, retornar un error
    if resultado == "clase_dictada":
        return jsonify({"error": "No se puede cambiar el turno de una clase ya dictada"}), 400

    # Responder con un mensaje de éxito
    return jsonify({"message": "Tipo de clase actualizado exitosamente"}), 200


@app.route("/api/clases/<int:id_clase>/estado", methods=["PUT"])
def api_cambiar_estado_clase(id_clase):
    # Obtener el estado de clase (dictada o no) desde el cuerpo de la solicitud json
    data = request.json
    dictada = data.get("dictada")

    # Llamar a la función que cambia el estado de clase
    resultado = cambiar_estado_clase(id_clase, dictada)
    
    # Responder con un mensaje de éxito
    return jsonify({"message": "Tipo de clase actualizado exitosamente"}), 200

@app.route("/api/clases", methods=["GET"])
def api_listar_clases():
    # Llamar a la función que lista todas las clases
    clases = listar_clases()

    # Retornar las clases como respuesta en formato json
    return jsonify(clases), 200


# ------------------------- ENDPOINTS Turnos -------------------------

@app.route("/api/turnos", methods=["POST"])
def api_agregar_turno():
    data = request.json
    id_turno = data.get("id_turno")
    hora_inicio = data.get("hora_inicio")
    hora_fin = data.get("hora_fin")

     # Validar que el CI sea numérico
    if not id_turno or not id_turno.isdigit():
        return jsonify({"error": "El ID debe contener solo números."}), 400

    # Validar si el id_turno ya está en uso
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT COUNT(*) FROM turnos WHERE id_turno = %s"
            cursor.execute(query, (id_turno,))
            result = cursor.fetchone()

            if result[0] > 0:  # Si ya existe
                return jsonify({"error": "El ID del turno ya está en uso."}), 400
        except Exception as e:
            print("Error al verificar el ID del turno:", e)
            return jsonify({"error": "Error en el servidor al verificar el ID del turno."}), 500
        finally:
            close_connection(connection)

    # Si el ID no está en uso, agregar el turno
    try:
        agregar_turno(id_turno, hora_inicio, hora_fin)
        return jsonify({"message": "Turno agregado exitosamente"}), 201
    except Exception as e:
        print("Error al agregar el turno:", e)
        return jsonify({"error": "Error al agregar el turno."}), 500

@app.route("/api/turnos/<id_turno>", methods=["PUT"])
def api_actualizar_turno(id_turno):
    data = request.json
    hora_inicio = data.get("hora_inicio")
    hora_fin = data.get("hora_fin")
    actualizar_turno(id_turno, hora_inicio, hora_fin)
    return jsonify({"message": "Turno actualizado exitosamente"})

@app.route("/api/turnos", methods=["GET"])
def api_listar_turnos():
    # Llamar a la función que lista todos los turnos
    turnos = obtener_turnos()

    # Si hay turnos, devolverlos en formato JSON, de lo contrario, un mensaje de error
    if turnos:
        return jsonify(turnos), 200
    else:
        return jsonify({"message": "No se encontraron turnos"}), 404


@app.route("/api/turnos/<id_turno>", methods=["DELETE"])
def api_eliminar_turno(id_turno):
    eliminar_turno(id_turno)
    return jsonify({"message": "Turno eliminado exitosamente"})

# ------------------------- ENDPOINTS Actividades -------------------------
@app.route("/api/actividades", methods=["GET"])
def api_obtener_actividades():
    actividades = obtener_actividades()

    return jsonify(actividades), 200

@app.route("/api/actividades/<int:id_actividad>", methods=["PUT"])
def api_actualizar_actividad(id_actividad):
    data = request.json
    descripcion = data.get("descripcion")
    costo = data.get("costo")

    # Validar que la descripción no supere los 50 caracteres
    if not descripcion or len(descripcion) > 50:
        return jsonify({"error": "La descripción no debe superar los 50 caracteres."}), 400

    if not descripcion or not costo:
        return jsonify({"message": "Descripcion y costo son requeridos"}), 400

    try:
        actualizar_actividad(id_actividad, descripcion, costo)
        return jsonify({"message": "Actividad actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"message": f"Error al actualizar la actividad: {e}"}), 500



# ------------------------- ENDPOINTS Equipamiento -------------------------

@app.route("/api/equipamiento", methods=["GET"])
def api_obtener_equipamiento():
    equipamiento = obtener_equipamiento()
    return jsonify(equipamiento)



# ------------------------- ENDPOINTS Alumno Clase -------------------------
@app.route("/api/alumno_clase/registrar", methods=["POST"])
def api_registrar_equipamiento_alumno():
    data = request.json
    id_clase = data.get("id_clase")
    ci_alumno = data.get("ci_alumno")
    alquilado = data.get("alquilado")
    id_equipamiento = data.get("id_equipamiento", None)
    
    # Llamada al registro con verificación
    resultado = registrar_equipamiento_alumno(id_clase, ci_alumno, alquilado, id_equipamiento)

    # Responder con el mensaje y el código de estado adecuado
    if "error" in resultado:
        return jsonify({"message": resultado["error"]}), resultado["status"]
    
    return jsonify({"message": resultado["message"]}), resultado["status"]


@app.route("/api/alumno_clase/ver", methods=["GET"])
def api_ver_equipamiento_alumno():
    # Obtener los parámetros desde el cuerpo de la solicitud JSON
    data = request.json
    id_clase = data.get("id_clase")
    ci_alumno = data.get("ci_alumno")
    
    # Verificar que los parámetros no estén vacíos
    if id_clase is None or ci_alumno is None:
        return jsonify({"message": "Faltan parámetros id_clase o ci_alumno"}), 400

    # Llamar a la función con los valores correctos
    equipamiento = ver_equipamiento_alumno(id_clase, ci_alumno)
    
    if equipamiento:
        return jsonify(equipamiento), 200
    else:
        return jsonify({"message": "No se encontró registro de equipamiento para el alumno en esta clase."}), 404
    

# ------------------------- ENDPOINTS consultas -------------------------
@app.route("/api/consultas/ingresos", methods=["GET"])
def api_obtener_actividades_mas_ingresos():
    actividades = obtener_actividades_con_mas_ingresos()
    if actividades:
        return jsonify(actividades)
    else:
        return jsonify({"mensaje": "No se encontraron actividades"}), 404

@app.route("/api/consultas/alumnos", methods=["GET"])
def api_obtener_actividades_mas_alumnos():
    actividades = obtener_actividades_con_mas_alumnos()
    if actividades:
        return jsonify(actividades)
    else:
        return jsonify({"mensaje": "No se encontraron actividades con alumnos inscritos."}), 404

@app.route("/api/consultas/turnos", methods=["GET"])
def api_obtener_turnos_mas_clases_dictadas():
    turnos = obtener_turnos_con_mas_clases_dictadas()
    if turnos:
        return jsonify(turnos)
    else:
        return jsonify({"mensaje": "No se encontraron turnos con clases dictadas."}), 404


# ------------------------- ENDPOINTS login -------------------------

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    correo = data.get("correo")
    contraseña = data.get("contraseña")

    if not correo or not contraseña:
        return jsonify({"error": "Por favor, proporciona un Correo y una contraseña"}), 400

    # Llamar a la lógica de validación de login
    resultado = validar_login(correo, contraseña)

    if resultado["success"]:
        session["user"] = resultado["user"]
        return jsonify({"message": resultado["message"]}), 200
    else:
        return jsonify({"error": resultado["message"]}), 401

@app.route("/api/logout", methods=["POST"])
def logout():
    if "user" not in session:
        return jsonify({"message": "No hay una sesión activa"}), 400  # Cambié el código de estado a 400 (Bad Request)
    session.pop("user", None)  # Si existe la clave "user", la elimina
    return jsonify({"message": "Sesión cerrada exitosamente"}), 200

@app.route("/api/login/registrar", methods=["POST"])
def api_registrar_usuario():
    data = request.json
    correo = data.get("correo")
    contraseña = data.get("contraseña")

    if not correo or not contraseña:
        return jsonify({"error": "Por favor, proporciona un Correo y una contraseña"}), 400
    
    resultado = registrar_usuario(correo, contraseña)
    if resultado["success"]:
        return jsonify(resultado), 201  # Registro exitoso
    else:
        return jsonify(resultado), 500  # Error en el servidor o bd
    
    
if __name__ == "__main__":
    app.run(debug=True)