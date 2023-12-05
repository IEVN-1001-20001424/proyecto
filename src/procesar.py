@app.route('/guardar_pelicula', methods=['POST'])
def guardar_pelicula():
    id_pelicula = request.form['id_pelicula']
    titulo = request.form['titulo']
    fecha_publicacion = request.form['fecha_publicacion']
    director = request.form['director']
    genero = request.form['genero']
    sipnosis = request.form['sipnosis']
    imagen = request.form['imagen']
    controlador_peliculas.insertar_pelicula(id_pelicula,titulo,fecha_publicacion,director,genero,sipnosis,imagen)
    return render_template('peliculas.html') 