from flask import Flask, render_template, request, url_for, redirect
#importar el modulo sqlite3
import sqlite3
#importar modulo de error de sqlite3
from sqlite3 import Error
from flask.helpers import flash
from jinja2.utils import object_type_repr
#from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = "1234"

sesion = dict()  

#-------------------------------Funciones especificas-----------------------

#Conexion a la base de datos
def sql_connection():
    try:
        con = sqlite3.connect('database.db')
        return con;
    except Error:
        flash(Error)

# Ver todos los usuarios en la base de datos
def sql_select_usuarios():
    strsql = "select * from usuario;";
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    usuarios = cursorObj.fetchall()
    return usuarios
#validar usuario
def validar_usuario(usuario):
    query = "select * from usuario where usuario='"+usuario+"'";
    con = sql_connection()
    cursorObj = con.cursor()
    try:
        cursorObj.execute(query)
        user = cursorObj.fetchall()
        return user
    except:
        flash('Usuario o Contrasena no válido')
        return redirect(url_for('index'))
    

#agregar usuario
def sql_agregar_usuario(nombre, usuario, contrasena, estado):
    crypt_pass = generate_password_hash(contrasena)
    strsql = "insert into usuario (nombre, usuario, contrasena, estado) values('"+nombre+"', '"+usuario+"', '"+crypt_pass+"', '"+estado+"');"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    con.commit()
    con.close()


# ---------------------------Contraoladores------------------------------------

@app.route('/')
def index():
    return render_template('modulos/login.html')

@app.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['user']
        contrasena = request.form['pass']
        sesion['usuario'] = usuario
        sesion['contrasena'] = contrasena
        user = validar_usuario(sesion['usuario'])
        if user[0][3] == contrasena: #check_password_hash(contrasena)
            sesion['rol'] = user[0][5]
            return redirect(url_for('inicio'))
        else:
            flash('Contrasena no valida')
            return redirect(url_for('index'))
    else: 
        flash('Metodo de acceso no valido')
        return redirect(url_for('index'))
 
@app.route('/inicio') 
def inicio():
    if 'rol' in sesion:
        return render_template('modulos/inicio.html', usuario = sesion['usuario'], rol = sesion['rol'])
    else: 
        flash('Debe iniciar sesion primero')
        return render_template('modulos/login.html') 
     

@app.route('/logout', methods = ['POST'])
def logout():
    sesion.clear()
    return redirect(url_for('index'))
    

@app.route('/usuarios')
def verUsuarios():
    if 'rol' in sesion and sesion['rol'] == 'Superadministrador':
        verUsuarios = sql_select_usuarios()
        return render_template('modulos/usuarios.html', verUsuarios = verUsuarios, rol = sesion['rol'] )
    else: 
        flash('Debe iniciar sesion como Superadministrador para acceder a la administracion de usuarios')
        return redirect(url_for('inicio'))   
    

#@app.route('/nuevoUsuario', methods=['GET', 'POST'])

app.route('/nuevoUsuario', methods=['POST', 'GET'])
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


@app.route('/<ruta>')
def ruta(ruta):
    if (ruta == "inicio" or ruta == "usuarios" or ruta == "proveedores" or ruta == "proveedores-detalle" or ruta == "productos"):
        return render_template(('/modulos/' + ruta + '.html'))
    else:
        return redirect('notFound')
        

@app.route('/notFound')
def notFound():
    return render_template('/modulos/404.html')

if __name__=="__main__":
    app.run(debug = True, port = 5000)