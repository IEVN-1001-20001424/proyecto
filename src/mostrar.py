
@app.route("/peliculas")
def peliculas():
    peliculas = controlador_peliculas.obtener_peliculas()
    return render_template("peliculas.html", pelis= peliculas)