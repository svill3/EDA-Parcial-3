# FUNCIONAMIENTO:

### (A) 
Dar doble click en `EJECUTABLE.exe` para correr el programa sin necesidad de compilarlo.  
   (Sin embargo, esto no permite cambiar los libros existentes por otros nuevos ya que se encuentran compilados dentro de la información enlazada al ejecutable.)

### (B) 
El profe ya sabe como ejecutar esto si quiere probar con otros libros:
   - Abrir este directorio en **VS Code** u otro editor de código.
   - Abrir la terminal y escribir `python app.py`.
   - Instalar las siguientes librerías usando estos comandos:
     ```bash
     pip install ast
     pip install os  # (puede que venga por defecto)
     pip install re  # (puede que venga por defecto)
     pip install random  # (puede que venga por defecto)
     pip install termcolor
     pip install networkx
     pip install matplotlib
     pip install numpy
     ```

   - Se pueden cambiar los libros manualmente en `libros.py`. Dar `CTRL+S` y luego escribir `python app.py` en la terminal.

### (C) 
La lógica de algoritmos de creación de grafos y búsqueda en grafos se encuentra en `grafos_libreria_propia.py`.

---

# DISCULPAS:
   Entiendo perfectamente si la implementación no es calificada porque entregué esto un día tarde.

   Mi motivo es que intenté hacer esto en HTML con Flask pero no pude. Cambié la lógica varias veces.  
   (No sé HTML, hice 2 intentos).

   Al final, me quedé con un ejecutable e interacción por consola. Adjunto la carpeta con intentos fallidos en HTML (ignorar).