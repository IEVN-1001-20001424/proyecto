from flask import Flask, jsonify, json
from flask import render_template, request, redirect, Response, url_for, session
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb
from config import config, obtener_conexion
import controlador_peliculas
import pymysql

app = Flask(__name__,template_folder='template')

#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'proyecto'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#mysql = MySQL(app)
con=MySQL(app)

#@app.route('/')
#def home():
#    return render_template('index.html')   

#@app.route('/admin')
#def admin():
#    return render_template('admin.html')   

@app.route('/user')
def user():
    peliculas = controlador_peliculas.obtener_peliculas()
    return render_template('user.html',pelis= peliculas, limpiarFiltroBtn = False,filtro='titulo')

@app.route("/user/buscar", methods=["GET"])
def user_buscar_pelicula_categoria():
    dato = request.args.get('dato')
    categoria = request.args.get('categoria')
    print(categoria)
    peliculas = controlador_peliculas.buscar_pelicula_categoria(dato, categoria)
    return render_template("user.html", pelis= peliculas, limpiarFiltroBtn = True, filtro=categoria)

@app.route('/user/comprar', methods=['POST'])
def comprar():
    print("comprar")
    code = request.form['code']
    cantidad = request.form['cantidad']
    peliculas = controlador_peliculas.comprar_pelicula_por_id(code)
    controlador_peliculas.restarCantidad(cantidad, code)
    return render_template("compra.html", pelis=peliculas)

#@app.route('/acceso-login', methods= ["GET", "POST"])
#def login():
#   
#    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
#       
#        _correo = request.form['txtCorreo']
#        _password = request.form['txtPassword']
#
#        cur = mysql.connection.cursor()
#        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s', (_correo, _password,))
#        account = cur.fetchone()
#      
#        if account:
#            session['logueado'] = True
#            session['id'] = account['id']
#            session['id_rol'] = account['id_rol']
#            
#            if session['id_rol']==1:
#                return render_template("admin.html")
#            elif session['id_rol']==2:
#                return render_template("user.html")
#        else:
#            return render_template('index.html',mensaje="Usuario o contraseña incorrectas")

@app.route("/agregar_pelicula")
def form_agregar_pelicula():
    return render_template("agregar_pelicula.html")

@app.route('/guardar_pelicula', methods=['POST'])
def guardar_pelicula():
    titulo = request.form['titulo']
    publicacion = request.form['publicacion']
    director = request.form['director']
    genero = request.form['genero']
    sipnosis = request.form['sipnosis']
    imagen = request.form['imagen']
    cantidad = request.form['cantidad']
    precio = request.form['precio']
    controlador_peliculas.insertar_pelicula(titulo,publicacion,director,genero,sipnosis,imagen,cantidad,precio)
    """ return render_template('/peliculas', pelis = peliculas) """ 
    return redirect("/peliculas")

""" Acceso por roles (Admin y usuario) """
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/acceso-login', methods= ["GET", "POST"])
def login():
    
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
       
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']

        cur = con.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s', (_correo, _password,))
        account = cur.fetchone()
      
        if account:
            session['logueado'] = True
            session['id'] = account[0]
            session['id_rol'] = account[3]
            
            if session['id_rol']==1:
                return redirect("/peliculas")
            elif session['id_rol']==2:
                return redirect("/user")
        else:
            return render_template('index.html',mensaje="Usuario o contraseña incorrectas")
""" Fin de acceso por roles (Admin y usuario) """

@app.route("/peliculas")
def peliculas():
    peliculas = controlador_peliculas.obtener_peliculas()
    return render_template("peliculas.html", pelis= peliculas, limpiarFiltroBtn = False, filtro='titulo')

def pagina_no_encontrada(error):
    return "<h1>Pagina no encontrada</h1>", 404

@app.route("/eliminar_pelicula", methods=["POST"])
def eliminar_pelicula():
    controlador_peliculas.eliminar_pelicula(request.form["id_pelicula"])
    return redirect("/peliculas")

@app.route("/form_editar_pelicula/<int:id_pelicula>")
def editar_pelicula(id_pelicula):
    # Obtener pelicula por ID
    pelicula = controlador_peliculas.obtener_pelicula_por_id(id_pelicula)
    return render_template("editar_pelicula.html", pelicula=pelicula)

@app.route("/actualizar_pelicula", methods=["POST"])
def actualizar_pelicula():
    id_pelicula = request.form['id_pelicula']
    titulo = request.form['titulo']
    publicacion = request.form['publicacion']
    director = request.form['director']
    genero = request.form['genero']
    sipnosis = request.form['sipnosis']
    imagen = request.form['imagen']
    cantidad = request.form['cantidad']
    precio = request.form['precio']
    controlador_peliculas.actualizar_pelicula(titulo,publicacion,director,genero,sipnosis,imagen,cantidad,precio, id_pelicula)
    return redirect("/peliculas")

@app.route("/buscar_pelicula", methods=["GET"])
def buscar_pelicula():
    titulo = request.args.get('titulo_pelicula')
    peliculas = controlador_peliculas.buscar_pelicula(titulo)
    return render_template("peliculas.html", pelis= peliculas, limpiarFiltroBtn = True)

@app.route("/peliculas/<string:categoria>")
def categoria(categoria):
    peliculas = controlador_peliculas.obtener_peliculas()
    return render_template("peliculas.html", pelis= peliculas, limpiarFiltroBtn = True, filtro=categoria)

@app.route("/buscar_pelicula/<string:categoria>", methods=["GET"])
def buscar_pelicula_categoria(categoria):
    dato = request.args.get('dato')
    print(dato)
    print(categoria)
    peliculas = controlador_peliculas.buscar_pelicula_categoria(dato, categoria)
    return render_template("peliculas.html", pelis= peliculas, limpiarFiltroBtn = True, filtro=categoria)

if __name__ == '__main__':
   app.config.from_object(config['development'])
   app.register_error_handler(404, pagina_no_encontrada)
   app.secret_key = "llave"
   app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
