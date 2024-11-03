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




@app.route('/mostrar_pagina_B', methods=['POST'])
def cerrar_sesion():
    file_path = 'flag.txt'
    os.remove(file_path)
    return render_template('pagina_A.html')







@app.route('/mostrar_pagina_B', methods=['GET', 'POST'])
def mostrar_pagina_B():
    para_crear_usuario = []
    file_path = 'flag.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        for linea in file:
            print(linea)
            linea = linea.strip()
            para_crear_usuario.append(ast.literal_eval(linea))
    
    temp_nombre = para_crear_usuario[0][0]
    temp_apellido = para_crear_usuario[0][1]
    temp_usuario = para_crear_usuario[0][2]
    temp_contraseña = para_crear_usuario[0][3]
    temp_historial = para_crear_usuario[0][4]
    temp_libro_actual = para_crear_usuario[0][5]

    if temp_historial == 'None':
        temp_historial = None
    else:
        temp_historial = ast.literal_eval(temp_historial)
    if temp_libro_actual == 'None':
        temp_libro_actual = None
    else:
        temp_libro_actual = int(temp_libro_actual)


    usuario = Usuario(temp_nombre, temp_apellido, temp_usuario, temp_contraseña, temp_historial, temp_libro_actual)
    libro_info = None
    for libro in LB:
        if usuario.libro_actual == libro[0]:
            libro_info = f'Título: {libro[1]}. Autores: {libro[2]}, {libro[3]}, {libro[4]}. Año: {libro[5]}. Materia: {libro[6]}'
            break
    
    historial_nuevo = str(usuario.historial)
    libro_actual_nuevo = str(usuario.libro_actual)

    datos = []
    file_path = 'datos.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        for linea in file:
            linea = linea.strip()
            datos.append(ast.literal_eval(linea))
    datos_nuevos = []
    for info in datos:
        if usuario.usuario != info[2]:
            datos_nuevos.append(info)
        else:
            temp = []
            temp.append(usuario.nombre)
            temp.append(usuario.apellido)
            temp.append(usuario.usuario)
            temp.append(usuario.contraseña)
            temp.append(historial_nuevo)
            temp.append(libro_actual_nuevo)
            datos_nuevos.append(temp)
    with open(file_path, 'w', encoding='utf-8') as file:
        for linea in datos_nuevos:
            file.write(f'{str(linea)}\n')

    datos=[]
    file_path = 'flag.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        for linea in file:
            linea = linea.strip()
            datos.append(ast.literal_eval(linea))
    datos_nuevos = []
    for info in datos:
        if usuario.usuario != info[2]:
            datos_nuevos.append(info)
        else:
            temp = []
            temp.append(usuario.nombre)
            temp.append(usuario.apellido)
            temp.append(usuario.usuario)
            temp.append(usuario.contraseña)
            temp.append(historial_nuevo)
            temp.append(libro_actual_nuevo)
            datos_nuevos.append(temp)
    with open(file_path, 'w', encoding='utf-8') as file:
        for linea in datos_nuevos:
            file.write(f'{str(linea)}\n')
    if request.method == 'POST':



        
        print(f'Bienvenido, {usuario.nombre}') 
        print(f'Estado actual: {usuario.libro_actual}')
        print('Posibles botónes')
        print('1. Buscar libros')
        print('2. Devolver libro actual')
        print('3. Ver mi historial de libros')
        print('4. Cerrar sesión')
        opcion = input('Botón: ')
        if opcion == '1':
            if usuario.libro_actual is not None:
                return render_template('mostrar_pagina_B.html', error='Devuelve el libro que tienes antes de pedir otro')
            buscar_libros(usuario)
        if opcion == '2':
            devolver_libro(usuario)
        if opcion == '3':
            ver_historial(usuario)
        if opcion == '4':
            file_path = 'flag.txt'
            os.remove(file_path)
            mostrar_pagina_A()

    return render_template('pagina_B.html', libro_info=libro_info, usuario=usuario)











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
                return render_template('crear_cuenta.html', error='La contraseña debe tener entre 3 y 40 caracteres')
            
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
                return redirect(url_for('mostrar_pagina_B'))

        return render_template('iniciar_sesion.html', error='Usuario o contraseña incorrectos')
    return render_template('iniciar_sesion.html')




@app.route('/buscar_libros', methods=['GET', 'POST'])
def buscar_libros(usuario):

    print('Ultimo libro leido: ')
    for libro in LB:
        if usuario.historial[-1] == libro[0]:
            print(f'ID: {libro[0]}, Título: {libro[1]}. Autores: {libro[2]}, {libro[3]}, {libro[4]}. Año: {libro[5]}. Materia: {libro[6]}')

    print('Libros recomendados: ')
    # Esto debería ser scrolleable en la versión final
    if usuario.libro_actual is None and usuario.historial is None:
        lista_libros = LB
        random.shuffle(lista_libros)
        for libro in lista_libros:
            print(f'ID: {libro[0]}, Título: {libro[1]}. Autores: {libro[2]}, {libro[3]}, {libro[4]}. Año: {libro[5]}. Materia: {libro[6]}')
    elif usuario.libro_actual is not None:
        tabla = explorar_grafo(G, usuario.libro_actual)
        for libro_objetivo in tabla:
            for libro in LB:
                if libro_objetivo == libro[0]:
                    print(f'ID: {libro[0]}, Título: {libro[1]}. Autores: {libro[2]}, {libro[3]}, {libro[4]}. Año: {libro[5]}. Materia: {libro[6]}')

    elif usuario.historial is not None:
        tabla = explorar_grafo(G, usuario.historial[-1])
        for libro_objetivo in tabla:
            for libro in LB:
                if libro_objetivo == libro[0]:
                    print(f'ID: {libro[0]}, Título: {libro[1]}. Autores: {libro[2]}, {libro[3]}, {libro[4]}. Año: {libro[5]}. Materia: {libro[6]}')

    print('Escoger libro (equivalente a hacer click, selecciona la id): ')
    libro_escogido = int(input("Ingresa la id del libro: "))
    usuario.libro_actual = libro_escogido






@app.route('/devolver_libro', methods=['GET', 'POST'])
def devolver_libro():
    para_crear_usuario = []
    file_path = 'flag.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        for linea in file:
            print(linea)
            linea = linea.strip()
            para_crear_usuario.append(ast.literal_eval(linea))
    
    temp_nombre = para_crear_usuario[0][0]
    temp_apellido = para_crear_usuario[0][1]
    temp_usuario = para_crear_usuario[0][2]
    temp_contraseña = para_crear_usuario[0][3]
    temp_historial = para_crear_usuario[0][4]
    temp_libro_actual = para_crear_usuario[0][5]

    if temp_historial == 'None':
        temp_historial = None
    else:
        temp_historial = ast.literal_eval(temp_historial)
    if temp_libro_actual == 'None':
        temp_libro_actual = None
    else:
        temp_libro_actual = int(temp_libro_actual)


    usuario = Usuario(temp_nombre, temp_apellido, temp_usuario, temp_contraseña, temp_historial, temp_libro_actual)
    libro_info = None
    for libro in LB:
        if usuario.libro_actual == libro[0]:
            libro_info = f'Título: {libro[1]}. Autores: {libro[2]}, {libro[3]}, {libro[4]}. Año: {libro[5]}. Materia: {libro[6]}'
            break

    if usuario.libro_actual is not None:
        usuario.historial.insert(len(usuario.historial), usuario.libro_actual)
        usuario.libro_actual = None
    mostrar_pagina_B()
    return render_template('pagina_B.html', libro_info=libro_info, usuario=usuario)








@app.route('/ver_historial', methods=['GET', 'POST'])
def ver_historial(usuario):
    if usuario.historial is not None:
        for id_libro in usuario.historial:
            for libro in LB:
                if id_libro == libro[0]:
                    print(f'ID: {libro[0]}, Título: {libro[1]}. Autores: {libro[2]}, {libro[3]}, {libro[4]}. Año: {libro[5]}. Materia: {libro[6]}')

def main():
    file_path = 'flag.txt'
    if not os.path.exists(file_path):
        mostrar_pagina_A()
    else:
        datos = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for linea in file:
                linea = linea.strip()
                datos.append(ast.literal_eval(linea))
        usuario_actual = datos[0]
        nombre = usuario_actual[0]
        apellido = usuario_actual[1]
        usuario = usuario_actual[2]
        contraseña = usuario_actual[3]
        historial = usuario_actual[4]
        libro_actual = usuario_actual[5]

        if historial == 'None':
            historial = None
        else:
            historial = ast.literal_eval(historial)
        if libro_actual == 'None':
            libro_actual = None
        else:
            libro_actual = int(libro_actual)
        logear_usuario = Usuario(nombre, apellido, usuario, contraseña, historial, libro_actual)
        mostrar_pagina_B(logear_usuario)




if __name__ == '__main__':
    app.run(debug=True)