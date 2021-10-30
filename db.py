#Salio un Foco y le di importar
import sqlite3
from sqlite3 import Error

#conectar a la base de datos
def get_db():
    try:
        con = sqlite3.connect('flask/database.db')
        return con;
    # Por si falla la conexion
    except Error:
        print(Error)

#Cerrar conexion base de datos
def close_db():
    con = sqlite3.connect('flask/database.db')
    con.close
