from flask import Flask, request, jsonify
from flask_cors import CORS  
from instructores import inscribir_instructor_en_clase, obtener_instructor, actualizar_instructor, eliminar_instructor
from alumnos import registrar_alumno, obtener_alumno, actualizar_alumno, eliminar_alumno
from clases import crear_clase, obtener_clase, actualizar_clase, eliminar_clase
from alumno_clase import registrar_equipamiento_alumno, ver_equipamiento_alumno
from turnos import obtener_turnos, crear_turno, eliminar_turno
from actividades import obtener_actividades, crear_actividad, eliminar_actividad

app = Flask(__name__)
CORS(app)  #habilita CORS para todas las rutas y permite solicitudes de cualquier origen
# para SOLO dar acceso al frontend se puede especificar: CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# ------------------------- Instructores -------------------------
@app.route("/api/instructores/inscribir", methods=["POST"])
def api_inscribir_instructor():
    data = request.json
    ci_instructor = data.get("ci_instructor")
    id_clase = data.get("id_clase")
    inscribir_instructor_en_clase(ci_instructor, id_clase)
    return jsonify({"message": "Instructor inscrito a la clase"}), 201

@app.route("/api/instructores/<ci>", methods=["GET"])
def api_obtener_instructor(ci):
    instructor = obtener_instructor(ci)
    return jsonify(instructor)

@app.route("/api/instructores/<ci>", methods=["PUT"])
def api_actualizar_instructor(ci):
    data = request.json
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    actualizar_instructor(ci, nombre, apellido)
    return jsonify({"message": "Instructor actualizado exitosamente"})

@app.route("/api/instructores/<ci>", methods=["DELETE"])
def api_eliminar_instructor(ci):
    eliminar_instructor(ci)
    return jsonify({"message": "Instructor eliminado exitosamente"})

# ------------------------- Alumnos -------------------------
@app.route("/api/alumnos", methods=["POST"])
def api_registrar_alumno():
    data = request.json
    ci_alumno = data.get("ci_alumno")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    registrar_alumno(ci_alumno, nombre, apellido)
    return jsonify({"message": "Alumno registrado exitosamente"}), 201

@app.route("/api/alumnos/<ci>", methods=["GET"])
def api_obtener_alumno(ci):
    alumno = obtener_alumno(ci)
    return jsonify(alumno)

@app.route("/api/alumnos/<ci>", methods=["PUT"])
def api_actualizar_alumno(ci):
    data = request.json
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    actualizar_alumno(ci, nombre, apellido)
    return jsonify({"message": "Alumno actualizado exitosamente"})

@app.route("/api/alumnos/<ci>", methods=["DELETE"])
def api_eliminar_alumno(ci):
    eliminar_alumno(ci)
    return jsonify({"message": "Alumno eliminado exitosamente"})

# ------------------------- Clases -------------------------
@app.route("/api/clases", methods=["POST"])
def api_crear_clase():
    data = request.json
    id_clase = data.get("id_clase")
    id_actividad = data.get("id_actividad")
    id_turno = data.get("id_turno")
    dictada = data.get("dictada")
    grupal = data.get("grupal")
    crear_clase(id_clase, id_actividad, id_turno, dictada, grupal)
    return jsonify({"message": "Clase creada exitosamente"}), 201

@app.route("/api/clases/<id_clase>", methods=["GET"])
def api_obtener_clase(id_clase):
    clase = obtener_clase(id_clase)
    return jsonify(clase)

@app.route("/api/clases/<id_clase>", methods=["PUT"])
def api_actualizar_clase(id_clase):
    data = request.json
    id_actividad = data.get("id_actividad")
    id_turno = data.get("id_turno")
    dictada = data.get("dictada")
    grupal = data.get("grupal")
    actualizar_clase(id_clase, id_actividad, id_turno, dictada, grupal)
    return jsonify({"message": "Clase actualizada exitosamente"})

@app.route("/api/clases/<id_clase>", methods=["DELETE"])
def api_eliminar_clase(id_clase):
    eliminar_clase(id_clase)
    return jsonify({"message": "Clase eliminada exitosamente"})

# ------------------------- Turnos -------------------------
@app.route("/api/turnos", methods=["GET"])
def api_obtener_turnos():
    turnos = obtener_turnos()
    return jsonify(turnos)

@app.route("/api/turnos", methods=["POST"])
def api_crear_turno():
    data = request.json
    turno = data.get("turno")
    crear_turno(turno)
    return jsonify({"message": "Turno creado exitosamente"}), 201

@app.route("/api/turnos/<id_turno>", methods=["DELETE"])
def api_eliminar_turno(id_turno):
    eliminar_turno(id_turno)
    return jsonify({"message": "Turno eliminado exitosamente"})

# ------------------------- Actividades -------------------------
@app.route("/api/actividades", methods=["GET"])
def api_obtener_actividades():
    actividades = obtener_actividades()
    return jsonify(actividades)

@app.route("/api/actividades", methods=["POST"])
def api_crear_actividad():
    data = request.json
    actividad = data.get("actividad")
    crear_actividad(actividad)
    return jsonify({"message": "Actividad creada exitosamente"}), 201

@app.route("/api/actividades/<id_actividad>", methods=["DELETE"])
def api_eliminar_actividad(id_actividad):
    eliminar_actividad(id_actividad)
    return jsonify({"message": "Actividad eliminada exitosamente"})

# ------------------------- Alumno Clase -------------------------
@app.route("/api/alumno_clase/registrar", methods=["POST"])
def api_registrar_equipamiento_alumno():
    data = request.json
    id_clase = data.get("id_clase")
    ci_alumno = data.get("ci_alumno")
    alquilado = data.get("alquilado")
    id_equipamiento = data.get("id_equipamiento", None)
    registrar_equipamiento_alumno(id_clase, ci_alumno, alquilado, id_equipamiento)
    return jsonify({"message": "Equipamiento registrado para el alumno"}), 201

@app.route("/api/alumno_clase/ver", methods=["GET"])
def api_ver_equipamiento_alumno():
    id_clase = request.args.get("id_clase")
    ci_alumno = request.args.get("ci_alumno")
    equipamiento = ver_equipamiento_alumno(id_clase, ci_alumno)
    return jsonify(equipamiento)

if __name__ == "__main__":
    app.run(debug=True)