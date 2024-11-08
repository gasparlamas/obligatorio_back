from flask import Flask, request, jsonify
from flask_cors import CORS  
from instructores import  agregar_instructor,obtener_instructor, actualizar_instructor, eliminar_instructor, ver_clases_asignadas
from alumnos import agregar_alumno,inscribir_alumno_en_clase, obtener_alumno, actualizar_alumno, eliminar_alumno
from clases import crear_clase, cambiar_turno_clase,cambiar_tipo_clase, cambiar_estado_clase, listar_clases, eliminar_clase
from alumno_clase import registrar_equipamiento_alumno, ver_equipamiento_alumno
from turnos import agregar_turno, actualizar_turno, obtener_turno, eliminar_turno
from actividades import obtener_actividad, actualizar_actividad

app = Flask(__name__)
CORS(app)  #habilita CORS para todas las rutas y permite solicitudes de cualquier origen
# para SOLO dar acceso al frontend se puede especificar: CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# ------------------------- Instructores -------------------------

@app.route("/api/instructores", methods=["POST"])
def api_agregar_instructor():
    data = request.json
    ci_instructor = data.get("ci_instructor")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    agregar_instructor(ci_instructor, nombre, apellido)
    return jsonify({"message": "Instructor agregado exitosamente"}), 201


@app.route("/api/instructores/<ci_instructor>", methods=["GET"])
def api_obtener_instructor(ci_instructor):
    instructor = obtener_instructor(ci_instructor)
    return jsonify(instructor)

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

# ------------------------- Alumnos -------------------------

@app.route("/api/alumnos", methods=["POST"])
def api_agregar_alumno():
    data = request.json
    ci_alumno = data.get("ci_alumno")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    fecha_nacimiento = data.get("fecha_nacimiento")
    agregar_alumno(ci_alumno, nombre, apellido, fecha_nacimiento)
    return jsonify({"message": "Alumno agregado exitosamente"}), 201

@app.route("/api/alumnos/<ci_alumno>/inscripcion", methods=["POST"])
def api_inscribir_alumno_en_clase(ci_alumno):
    data = request.json
    id_clase = data.get("id_clase")
    
    # Llamar a la función para inscribir al alumno en la clase
    inscribir_alumno_en_clase(ci_alumno, id_clase)
    
    return jsonify({"message": "Alumno inscrito en la clase exitosamente"}), 201

@app.route("/api/alumnos/<ci_alumno>", methods=["GET"])
def api_obtener_alumno(ci_alumno):
    alumno = obtener_alumno(ci_alumno)
    return jsonify(alumno)

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

# ------------------------- Clases -------------------------
@app.route("/api/clases", methods=["POST"])
def api_crear_clase():
    data = request.json
    id_clase = data.get("id_clase")
    ci_instructor = data.get("ci_instructor")
    id_actividad = data.get("id_actividad")
    id_turno = data.get("id_turno")
    dictada = data.get("dictada")
    grupal = data.get("grupal")
    crear_clase(id_clase, ci_instructor, id_actividad, id_turno, dictada, grupal)
    return jsonify({"message": "Clase creada exitosamente"}), 201

@app.route("/api/clases/<int:id_clase>/turno/<int:id_turno>", methods=["PUT"])
def api_cambiar_turno_clase(id_clase, id_turno):
    # Llamar a la función que cambia el turno de la clase
    resultado = cambiar_turno_clase(id_clase, id_turno)

    # Si la clase ya está dictada, retornar un error
    if resultado == "clase_dictada":
        return jsonify({"error": "No se puede cambiar el turno de una clase ya dictada"}), 400

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

@app.route("/api/clases/<id_clase>", methods=["DELETE"])
def api_eliminar_clase(id_clase):
    resultado = eliminar_clase(id_clase)
    if not resultado["success"]:
        return jsonify({"message": resultado["message"]}), 400  
    return jsonify({"message": resultado["message"]}), 200  


# ------------------------- Turnos -------------------------

@app.route("/api/turnos", methods=["POST"])
def api_agregar_turno():
    data = request.json
    id_turno = data.get("id_turno")
    hora_inicio = data.get("hora_inicio")
    hora_fin = data.get("hora_fin")
    agregar_turno(id_turno, hora_inicio, hora_fin)
    return jsonify({"message": "Turno agregado exitosamente"}), 201

@app.route("/api/turnos/<id_turno>", methods=["PUT"])
def api_actualizar_turno(id_turno):
    data = request.json
    hora_inicio = data.get("hora_inicio")
    hora_fin = data.get("hora_fin")
    actualizar_turno(id_turno, hora_inicio, hora_fin)
    return jsonify({"message": "Turno actualizado exitosamente"})

@app.route("/api/turnos/<id_turno>", methods=["GET"])
def api_obtener_turno(id_turno):
    turno = obtener_turno(id_turno)
    if turno:
        # Devolver los datos del turno en formato json
        return jsonify({
            "id_turno": turno[0],
            "hora_inicio": turno[1],
            "hora_fin": turno[2]
        })
    else:
        # Si no se encuentra el turno, devolver un mensaje de error
        return jsonify({"message": "Turno no encontrado"}), 404


@app.route("/api/turnos/<id_turno>", methods=["DELETE"])
def api_eliminar_turno(id_turno):
    eliminar_turno(id_turno)
    return jsonify({"message": "Turno eliminado exitosamente"})

# ------------------------- Actividades -------------------------
@app.route("/api/actividades/<int:id_actividad>", methods=["GET"])
def api_obtener_actividad(id_actividad):
    actividad = obtener_actividad(id_actividad)
    if actividad:
        # Si la actividad existe, devolverla como un json
        return jsonify({
            "id_actividad": actividad[0],
            "descripcion": actividad[1],  # Asumiendo que el nombre es el segundo campo
            "costo": actividad[2],  # Asumiendo que la descripción es el tercer campo
            # Agrega más campos según la estructura de la tabla 'actividades'
        })
    else:
        # Si no se encuentra la actividad, devolver un mensaje de error
        return jsonify({"message": "Actividad no encontrada"}), 404

@app.route("/api/actividades/<int:id_actividad>", methods=["PUT"])
def api_actualizar_actividad(id_actividad):
    data = request.json
    descripcion = data.get("descripcion")
    costo = data.get("costo")

    if not descripcion or not costo:
        return jsonify({"message": "Descripcion y costo son requeridos"}), 400

    try:
        actualizar_actividad(id_actividad, descripcion, costo)
        return jsonify({"message": "Actividad actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"message": f"Error al actualizar la actividad: {e}"}), 500


# ------------------------- Alumno Clase -------------------------
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


if __name__ == "__main__":
    app.run(debug=True)