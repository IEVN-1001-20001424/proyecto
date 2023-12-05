from flask import Flask, jsonify
from flask import render_template, request, redirect, Response, url_for, session
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb
from config import config
from config import obtener_conexion
import pymysql

def insertar_pelicula(titulo,publicacion,director,genero,sipnosis,imagen,cantidad,precio):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""INSERT INTO peliculas(titulo,publicacion,director,genero,sipnosis,imagen,cantidad,precio)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (titulo,publicacion,director,genero,sipnosis,imagen,cantidad,precio))
    conexion.commit()

def obtener_peliculas():
    conexion = obtener_conexion()
    peliculas=[]
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_pelicula,titulo,publicacion,director,genero,sipnosis,imagen,cantidad,precio FROM peliculas")
        peliculas = cursor.fetchall()
    return peliculas

def eliminar_pelicula(id_pelicula):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM peliculas WHERE id_pelicula = %s", (id_pelicula))
    conexion.commit()

def obtener_pelicula_por_id(id_pelicula):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id_pelicula,titulo,publicacion,director,genero,sipnosis,imagen,cantidad,precio FROM peliculas WHERE id_pelicula = %s", (id_pelicula))
        pelicula = cursor.fetchone()
    return pelicula

def comprar_pelicula_por_id(id_pelicula):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id_pelicula,titulo,publicacion,director,genero,sipnosis,imagen,cantidad,precio FROM peliculas WHERE id_pelicula = %s", (id_pelicula))
        pelicula = cursor.fetchall()
    return pelicula

def actualizar_pelicula(titulo,publicacion,director,genero,sipnosis,imagen, cantidad,precio, id_pelicula):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE peliculas SET titulo = %s, publicacion = %s, director = %s, genero = %s, sipnosis = %s, imagen = %s, cantidad = %s, precio = %s WHERE id_pelicula = %s",
                       (titulo,publicacion,director,genero,sipnosis,imagen,cantidad,precio, id_pelicula))
    conexion.commit()

def buscar_pelicula(titulo):
    conexion = obtener_conexion()
    peliculas=[]
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_pelicula,titulo,publicacion,director,genero,sipnosis,imagen,cantidad,precio FROM peliculas where titulo like '%{0}%'".format(titulo))
        peliculas = cursor.fetchall()
    return peliculas

def buscar_pelicula_categoria(cat):
    conexion = obtener_conexion()
    peliculas=[]
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_pelicula,titulo,publicacion,director,genero,sipnosis,imagen,cantidad,precio FROM peliculas where titulo like '%{0}%'".format(cat))
        peliculas = cursor.fetchall()
    return peliculas

def buscar_pelicula_categoria(titulo, cat):
    conexion = obtener_conexion()
    peliculas=[]
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_pelicula,titulo,publicacion,director,genero,sipnosis,imagen,cantidad,precio FROM peliculas where {0} like '%{1}%'".format(cat, titulo))
        peliculas = cursor.fetchall()
    return peliculas

def restarCantidad(cantidad, code):
    conexion = obtener_conexion()
    peliculas=[]
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE peliculas SET cantidad = (%s-1) WHERE id_pelicula = %s", (cantidad, code))
        peliculas = cursor.fetchall()
    return peliculas