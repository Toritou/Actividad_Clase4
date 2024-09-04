from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Conexión a MongoDB
ClienteMongo = MongoClient('mongodb://localhost:27017/')
DB = ClienteMongo['lista_tareas']
ColeccionUsuarios = DB['usuarios']
ColeccionTareas = DB['tareas']

# Ruta para verificar la existencia de un usuario por RUT
@app.route('/usuarios/<rut>', methods=['GET'])
def verificar_usuario(rut):
    usuario = ColeccionUsuarios.find_one({'rut': rut})
    if usuario:
        return jsonify({'mensaje': 'Usuario encontrado'}), 200
    return jsonify({'error': 'Usuario no encontrado'}), 404

# Ruta para crear un nuevo usuario utilizando solo el RUT
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    if not data or 'rut' not in data:
        return jsonify({'error': 'RUT no proporcionado'}), 400

    rut = data['rut']
    if ColeccionUsuarios.find_one({'rut': rut}):
        return jsonify({'error': 'El RUT ya está registrado'}), 409

    nuevo_usuario = {'rut': rut}
    ColeccionUsuarios.insert_one(nuevo_usuario)
    return jsonify({'mensaje': 'Usuario creado exitosamente'}), 201

# Ruta para agregar una nueva tarea vinculada a un usuario por RUT
@app.route('/tareas', methods=['POST'])
def agregar_tarea():
    data = request.get_json()
    if not data or 'rut' not in data or 'titulo' not in data or 'descripcion' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400

    rut = data['rut']
    if not ColeccionUsuarios.find_one({'rut': rut}):
        return jsonify({'error': 'Usuario no encontrado'}), 404

    # Generar un nuevo ID para la tarea
    nuevo_id = ColeccionTareas.count_documents({}) + 1

    nueva_tarea = {
        'id': nuevo_id,
        'rut': rut,
        'titulo': data['titulo'],
        'descripcion': data['descripcion'],
        'completado': False
    }
    ColeccionTareas.insert_one(nueva_tarea)
    return jsonify({'mensaje': 'Tarea agregada exitosamente'}), 201

# Ruta para obtener las tareas de un usuario por RUT
@app.route('/tareas/<rut>', methods=['GET'])
def obtener_tareas_usuario(rut):
    tareas = list(ColeccionTareas.find({'rut': rut}, {'_id': 0}))
    return jsonify(tareas), 200

# Ruta para actualizar una tarea por ID (se requiere el RUT del usuario y el ID de la tarea)
@app.route('/tareas/<rut>/<id>', methods=['PUT'])
def actualizar_tarea(rut, id):
    data = request.get_json()
    tarea = ColeccionTareas.find_one({'rut': rut, 'id': int(id)})

    if not tarea:
        return jsonify({'error': 'Tarea no encontrada'}), 404

    actualizaciones = {}
    if 'titulo' in data:
        actualizaciones['titulo'] = data['titulo']
    if 'descripcion' in data:
        actualizaciones['descripcion'] = data['descripcion']
    if 'completado' in data:
        actualizaciones['completado'] = data['completado']

    ColeccionTareas.update_one({'rut': rut, 'id': int(id)}, {'$set': actualizaciones})
    return jsonify({'mensaje': 'Tarea actualizada exitosamente'}), 200

# Ruta para eliminar una tarea por ID (se requiere el RUT del usuario y el ID de la tarea)
@app.route('/tareas/<rut>/<id>', methods=['DELETE'])
def eliminar_tarea(rut, id):
    resultado = ColeccionTareas.delete_one({'rut': rut, 'id': int(id)})

    if resultado.deleted_count == 0:
        return jsonify({'error': 'Tarea no encontrada'}), 404

    return jsonify({'mensaje': 'Tarea eliminada exitosamente'}), 200

# Ejecución en Flask en el puerto 8080
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
