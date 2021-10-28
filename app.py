#Entorno virtual... Creo
from flask import Flask, render_template, request
#importar el modulo sqlite3
import sqlite3
#importar modulo de error de sqlite3
from sqlite3 import Error

from werkzeug.utils import redirect

app = Flask(__name__)

#Conexion a la base de datos
def sql_connection():
    try:
        con=sqlite3.connect('database.db')
        return con;
    except Error:
        print(Error)

# controladores usuarios 

# Ver todos los usuarios en la base de datos
def sql_select_usuarios():
    strsql = "select * from usuario;";
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    usuarios = cursorObj.fetchall()
    return usuarios

#agregar usuario
def sql_agregar_usuario(nombre, usuario, contrasena, estado):
    strsql = "insert into usuario (nombre, usuario, contrasena, estado) values('"+nombre+"', '"+usuario+"', '"+contrasena+"', '"+estado+"');"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    con.commit()
    con.close()

#editar usuario
#def sql_editar_usuario():

# Contraoladores proveedores

@app.route('/usuarios')
def verUsuarios():
    verUsuarios = sql_select_usuarios()
    return render_template('/modulos/usuarios.html', verUsuarios=verUsuarios)

#@app.route('/nuevoUsuario', methods=['GET', 'POST'])
@app.route('/nuevoUsuario', methods=['POST'])
def nuevoUsuario():
    nombre = request.form["nuevoNombre"]
    usuario = request.form["nuevoUsuario"]
    contrasena =request.form["nuevoPassword"]
    estado = request.form["nuevoPerfil"]
    sql_agregar_usuario(nombre, usuario, contrasena, estado)
    #return "OK"
    return redirect('/usuarios')
    #return render_template('/modulos/usuarios.html', verUsuarios=verUsuarios)

@app.route('/editarUsuario')

@app.route('/')
def index():
    return render_template('/modulos/footer.html')

@app.route('/<ruta>')
def ruta(ruta):
    if (ruta == "inicio" or ruta == "usuarios" or ruta == "proveedores" or ruta == "proveedores-detalle" or ruta == "productos"):
        return render_template(('/modulos/' + ruta + '.html'))
    else:
        return render_template('/modulos/404.html')
        #return "Hola Miguel Hart"

@app.route('/login')
def login():
    return render_template('/modulos/login.html')

if __name__=="__main__":
    app.run(debug = True, port = 5000)


