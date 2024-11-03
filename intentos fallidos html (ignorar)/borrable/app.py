import os
import ast
import re
import random

from usuario import Usuario
from libros import libros as LB
from grafos_libreria_propia import G, explorar_grafo, mostrar_grafo

from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def mostrar_pagina_A():
    return render_template('pagina_A.html')

@app.route('/crear_cuenta', methods=['GET', 'POST'])
def crear_cuenta():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        confirmar_contraseña = request.form['confirmar_contraseña']

        if contraseña != confirmar_contraseña:
            return render_template('crear_cuenta.html', error='Las contraseñas no coinciden')

        file_path = 'datos.txt'
        if not os.path.exists(file_path):
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(f'["{nombre}", "{apellido}", "{usuario}", "{contraseña}", "{None}", "{None}"]\n')
        else:
            datos = []
            with open(file_path, 'r', encoding='utf-8') as file:
                for linea in file:
                    linea = linea.strip()
                    datos.append(ast.literal_eval(linea))
            
            usuario_existe = any(info[2] == usuario for info in datos)
            if usuario_existe:
                return render_template('crear_cuenta.html', error='El usuario ya existe')

            if not re.fullmatch(r'^.{3,40}$', contraseña):
                return render_template('crear_cuenta.html', error='La contraseña no es válida')
            
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(f'["{nombre}", "{apellido}", "{usuario}", "{contraseña}", "{None}", "{None}"]\n')
        
        return redirect(url_for('mostrar_pagina_A'))
    
    return render_template('crear_cuenta.html')

@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']

        file_path = 'datos.txt'
        datos = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for linea in file:
                linea = linea.strip()
                datos.append(ast.literal_eval(linea))

        for info in datos:
            if usuario == info[2] and contraseña == info[3]:
                nombre = info[0]
                apellido = info[1]
                historial = info[4]
                libro_actual = info[5]

                file_path = 'flag.txt'
                with open(file_path, 'a', encoding='utf-8') as file:
                    file.write(f'["{nombre}", "{apellido}", "{usuario}", "{contraseña}", "{historial}", "{libro_actual}"]')

                if historial == 'None':
                    historial = None
                else:
                    historial = ast.literal_eval(historial)
                if libro_actual == 'None':
                    libro_actual = None
                else:
                    libro_actual = int(libro_actual)
                
                logear_usuario = Usuario(nombre, apellido, usuario, contraseña, historial, libro_actual)
                return mostrar_pagina_B(logear_usuario)

        return render_template('iniciar_sesion.html', error='Usuario o contraseña incorrectos')

    return render_template('iniciar_sesion.html')

def mostrar_pagina_B(usuario):
    # Implement this function to render the user's page
    return render_template('pagina_B.html', usuario=usuario)

@app.route('/buscar_libros', methods=['GET', 'POST'])
def buscar_libros():
    usuario = obtener_usuario()  # Asume que tienes una forma de obtener el usuario actual.
    libros_recomendados = []

    if request.method == 'POST':
        # Lógica de búsqueda de libros
        if usuario.historial:
            ultimo_libro_id = usuario.historial[-1]
            for libro in LB:
                if ultimo_libro_id == libro[0]:
                    print(f'Último libro leído: ID: {libro[0]}, Título: {libro[1]}')
        
        # Recomendaciones de libros
        print('Libros recomendados: ')
        if usuario.libro_actual is None and (usuario.historial is None or len(usuario.historial) == 0):
            lista_libros = LB.copy()
            random.shuffle(lista_libros)
            libros_recomendados = lista_libros  # Usamos una lista aleatoria de libros
        elif usuario.libro_actual is not None:
            tabla = explorar_grafo(G, usuario.libro_actual)
            for libro_objetivo in tabla:
                for libro in LB:
                    if libro_objetivo == libro[0]:
                        libros_recomendados.append(libro)
        elif usuario.historial is not None:
            tabla = explorar_grafo(G, usuario.historial[-1])
            for libro_objetivo in tabla:
                for libro in LB:
                    if libro_objetivo == libro[0]:
                        libros_recomendados.append(libro)

    return render_template('buscar_libros.html', libros=libros_recomendados)

def obtener_usuario():
    # Implementa la lógica para recuperar el usuario actual desde el archivo flag.txt o una sesión.
    # Ejemplo simple:
    with open('flag.txt', 'r', encoding='utf-8') as file:
        datos = ast.literal_eval(file.readline().strip())
    return Usuario(*datos)  # Asumiendo que el constructor de Usuario toma esos datos.

@app.route('/devolver_libro')
def devolver_libro(usuario):
    if usuario.libro_actual is not None:
        usuario.historial.insert(len(usuario.historial), usuario.libro_actual)
        usuario.libro_actual = None

@app.route('/ver_historial')
def ver_historial(usuario):
    if usuario.historial is not None:
        for id_libro in usuario.historial:
            for libro in LB:
                if id_libro == libro[0]:
                    print(f'ID: {libro[0]}, Título: {libro[1]}. Autores: {libro[2]}, {libro[3]}, {libro[4]}. Año: {libro[5]}. Materia: {libro[6]}')


@app.route('/logout')
def logout():
    file_path = 'flag.txt'
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for('mostrar_pagina_A'))

if __name__ == '__main__':
    app.run(debug=True)