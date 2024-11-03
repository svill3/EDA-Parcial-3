# Libros en formato ['Título', 'Autor 1', 'Autor 2', 'Autor 3', Año, 'Materia' ]
#
# 1. Para cambiar los libros, modificar manualmentela lista de abajo siguiento el formato de arriba
# 2. Luego, eliminar datos.txt (si existe) y flag.txt (si existe)
# 3. Volver a ejecutar el app.exe
libros = [
    ['Estrategias de marketing en redes sociales', 'Ana Martínez', 'Pedro García', 'María González', 2005, 'Economía' ],
    ['El impacto de la globalización en la economía', 'Diego Pérez', 'Diego Martínez', 'Ana González', 2016, 'Economía' ],
    ['El papel de las energías renovables en la lucha contra el cambio climático', 'María Suárez', 'Isabel Sánchez', 'Luis Suárez', 2001, 'Economía' ],
    ['La importancia de la salud mental en el trabajo', 'Ana Álvarez', 'Laura García', 'Laura Sánchez', 2004, 'Salud' ],
    ['La importancia de la cultura en la sociedad actual', 'Juan García', 'Laura Sánchez', 'María Álvarez', 2008, 'Sociedad' ],
    ['Los desafíos de la inteligencia artificial', 'Ana Suárez', 'Laura García', 'Pedro González', 2009, 'Tecnología' ],
    ['El impacto de la tecnología en la educación', 'Ana Suárez', 'Diego Sánchez', 'María Sánchez', 2022, 'Tecnología' ],
    ['Nuevas tendencias en la industria alimentaria', 'Carlos Rodríguez', 'María Suárez', 'Pedro Rodríguez', 2022, 'Salud' ],
    ['Nuevas tendencias en la industria alimentaria', 'Pedro Romero', 'Isabel García', 'Ana Martínez', 2018, 'Salud' ],
    ['Estrategias de marketing en redes sociales', 'Laura Rodríguez', 'Isabel Pérez', 'Luis Romero', 2017, 'Economía' ]
]

# Actualizo los libros para que estén en formato ['id, 'Título', 'Autor 1', 'Autor 2', 'Autor 3', Año, 'Materia' ]
for id, libro in enumerate(libros, start=1):
    libro.insert(0, id)