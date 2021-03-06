# Proyecto 3 Bryan Velasco & Christian Leyva

Hola profesor, este es nuestro proyecto 3, este README es para aclarar la estructura de los archivos.

## Ejecuci贸n

Para ejecutar el proyecto tiene que utilizar la siguiente linea en la terminal:

~~~console
python3 proyecto3_chrisco {PID}
~~~

Donde el {PID} es el que se desea mapear. Por ejemplo

```console
python3 proyecto3_chrisco 9
```

Y al mismo tiempo puede ver un ejemplo de salida de esta ejecuci贸n con el PID 9 [aqu铆](https://chrisley304.github.io/sistop-2022-2/proyectos/3/LeyvaChristian-VelascoBryan/EJEMPLO_Pmap_PID_9.html) el cual es el archivo *EJEMPLO_Pmap_PID_9.html* hosteado con Github Pages :octocat: en nuestro repo.

Dejamos este ejemplo por si por alguna raz贸n el programa falla y no muestra la salida correctamente, sin embargo no esperamos que suceda pero por si las dudas jaja 馃榾.

## Documentaci贸n

La documentaci贸n la puede encontrar en el archivo [Documentacion proyecto 3.pdf](./Documentacion%20proyecto%203.pdf).

## Algunas puntos a destacar:

1. El programa requiere instalar la biblioteca *tabulate*, esta se puede instalar mediante *pip* con el siguiente comando:
   ```console
   pip install tabulate
   ```
2. Al ejecutar el programa, este genera un archivo *.html* el cual abre automaticamente en su navegador predeterminado. **Si esto llega a generar problemas** puede desactivar esta opcion comentando la linea **127** del archivo  `proyecto3_chrisco.py`, la cual es la siguiente:
   ```python
    # Se abre autom谩ticamente el archivo generado:
    # Si no se desea que se abra autom谩ticamente puede comentar la siguiente linea:
    webbrowser.open_new_tab(filename)
   ```
3. El archivo `PmaptoHTLM_chrisco.py` contiene las funciones para generar el archivo `.html` de salida, pero el codigo principal se encuentra en el archivo `proyecto3_chrisco.py`. 馃槈