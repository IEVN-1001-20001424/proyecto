@app.route("/agregar_pelicula")
def form_agregar_pelicula():
    return render_template("agregar_pelicula.html")