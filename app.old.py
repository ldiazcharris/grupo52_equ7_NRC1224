from logging import DEBUG
from flask import Flask, jsonify, request
from productos import productos

app = Flask(__name__)

@app.route('/productos')
def get_productos():
    return jsonify({"productos":productos, "Mensaje":"Listado de Articulos"})

@app.route('/productos/<nombre>')
def get_producto(nombre):
    listaProductos = [producto for producto in productos if producto['nombre'] == nombre]
    if len(listaProductos) > 0:
        return(jsonify({
            "Mensaje": "Se encontró el producto",
            "producto": listaProductos[0]
        }))
    else: 
        return (jsonify({'mensaje': "No se ha encontrado ningún producto"}))

@app.route("/productos", methods=['POST'])
def add_producto():
    producto = request.json
    productos.append(producto)

    return (jsonify({
        "Mensaje": "Elemento creado correctamente",
        "Productos": productos
    }))

@app.route('/productos/<nombre>', methods=['PUT'])
def update_producto(nombre):
    listaProductos = [producto for producto in productos if producto['nombre'] == nombre]
    if len(listaProductos) > 0:
        producto = listaProductos[0]
        producto['nombre'] = request.json['nombre']
        producto['precio'] = request.json['precio']
        producto['cantidad'] = request.json['cantidad']
        return(jsonify({
            "Mensaje": "Producto actualizado correctamente",
            "producto": listaProductos[0]
        }))
    else: 
        return (jsonify({'mensaje': "No se ha encontrado ningún producto"}))

@app.route('/productos/<nombre>', methods=['DELETE'])
def delete_producto(nombre):
    listaProductos = [producto for producto in productos if producto['nombre'] == nombre]
    if len(listaProductos) > 0:
        productos.remove(listaProductos[0])
        return(jsonify({
            "Mensaje": "Producto eliminado correctamente",
            "producto": listaProductos[0]
        }))
    else: 
        return (jsonify({'mensaje': "No se ha encontrado ningún producto"}))

def index():
    return '<h1>Hola!</h1>'

if __name__=="__main__":
    app.run(debug = True, port = 5000)