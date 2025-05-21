from flask import Flask, jsonify, request, render_template
from config import config
from flask_mysqldb import MySQL

app = Flask(__name__)
conexion = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

# Rutas API para obtener datos
@app.route('/api/animales', methods=['GET'])
def listar_animales():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id_animal, nombre_comun, estado, descripcion FROM animales ORDER BY id_animal DESC LIMIT 15"
        cursor.execute(sql)
        datos = cursor.fetchall()
        animales = [{
            'id': fila[0],
            'nombre': fila[1],
            'estado': fila[2],
            'descripcion': fila[3]
        } for fila in datos]
        return jsonify({'animales': animales})
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

@app.route('/api/plantas', methods=['GET'])
def listar_plantas():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id_planta, nombre_comun, estado, ubicacion FROM plantas ORDER BY id_planta DESC LIMIT 15"
        cursor.execute(sql)
        datos = cursor.fetchall()
        plantas = [{
            'id': fila[0],
            'nombre': fila[1],
            'estado': fila[2],
            'ubicacion': fila[3]
        } for fila in datos]
        return jsonify({'plantas': plantas})
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

@app.route('/api/produccion', methods=['GET'])
def listar_produccion():
    try:
        cursor = conexion.connection.cursor()
        sql = """SELECT p.id_produccion, a.nombre_comun, p.tipo_produccion, p.cantidad, p.fecha_recoleccion 
                 FROM produccion p JOIN animales a ON p.id_animal = a.id_animal 
                 ORDER BY p.fecha_recoleccion DESC LIMIT 10"""
        cursor.execute(sql)
        datos = cursor.fetchall()
        produccion = [{
            'id': fila[0],
            'animal': fila[1],
            'tipo': fila[2],
            'cantidad': float(fila[3]),
            'fecha': fila[4].strftime('%Y-%m-%d') if fila[4] else None
        } for fila in datos]
        return jsonify({'produccion': produccion})
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(debug=True)