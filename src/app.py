from flask import Flask, jsonify, request
from config import config
from flask_mysqldb import MySQL


app = Flask(__name__)
conexion = MySQL(app)

#primer metodo para interactuar con la bd (GET) listar o mostrar

@app.route('/animales', methods=['GET'])

def listar_animales():
    
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id_animal, nombre_comun, estado, descripcion, fecha_registro from animales"
        cursor.execute(sql)
        datos = cursor.fetchall() #los datos de la consulta se almacenan en esta variable 
        animales = []
        
        for fila in datos:
            
            animal = {
                'id_animal': fila[0],
                'nombre_comun': fila[1],
                'estado': fila[2],
                'descripcion': fila[3],
                'fecha_registro': fila[4]
            }
            
            animales.append(animal)
        return jsonify({'animal':animal, 'Mensaje': 'Animales listados'})
    
    except Exception as ex:
        return jsonify({'Mensaje': 'Error'})
    
    
#segundo metodo para interactuar con la bd (POST) insertar o agregar
@app.route('/animales', methods=['POST'])

def agregar_animal():
    
    try:
       # print(request.json)  
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO animales (nombre_comun, estado, descripcion, fecha_registro)
        VALUES ('{0}', '{1}', '{2}', '{3}')""".format(request.json['nombre_comun'], request.json['estado'], request.json['descripcion'], request.json['fecha_registro'])
        cursor.execute(sql)
        conexion.connection.commit() #se guardan los cambios en la base de datos
        return jsonify({'Mensaje': 'Animal agregado'})  
    
    except Exception as ex:
        return jsonify({'Mensaje': 'Error'})
    
def pagina_no_encontrada(error):
    return "<h1> La pagina que intentas buscar no existe...</h1>" , 404

if __name__ == '__main__':
    
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
   