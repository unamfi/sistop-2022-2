# Proyecto: Asignación de memoria en un sistema real

## Fundamentos

De manera corta, tomé como base la salida que linux da sobre el archivo '/proc/{PID}/maps'.
Este archivo muestra varias cosas interesantes:

![archivo maps](/proyectos/3/BarriosFrancisco/Imagenes/maps.png)

1. dirección de inicio 
2. dirección final
3. permisos: lectura, escritura, ejecutable, o compartido/privado
4. ruta

para este caso, los otros campos no nos serán de utilidad para el proyecto

Por otra parte, encontré que cuando en la ruta se especifica:
- [Heap]: Referente al Heap del proceso. Este puede o no especificarse de forma explicita
- [Stack]: La pila del proceso
- [vvar]: Referente a variables del Kernel
- [vsyscall], [vectors], ó [vdso]: Especifican llamadas al sistema
- Una ruta como tal: Esta región de memoria puede estar dedicada a *datos* o *Texto*, aunque también a un archivo ya eliminado, o a espacio reservado
  - Texto: Cuando tiene 'x' en los permisos
    - Bib Texto: Cuando en el archivo *maps* ya se especifico un *heap*, ó el archivo esta dentro de *lib*
  - Datos: Cuando tiene 'r' en los permisos
    - Bid Datos: Cuando en el archivo *maps* ya se especifico un *heap*, ó el archivo esta dentro de *lib*
  - Reserva: Esta zona de la memoria no tiene permisos de escritura ni lectura

Y finalmente, en el programa se lanza la salida por colores, usando ANSI:
- deleted: Con rojo oscuro \033[31m
- Texto: Verde \033[92m
- Datos: Amarilo \033[93m
- Stack: Azul \033[94m
- Heap: Rojo brillante \033[91m
- vvar: Magenta \033[95m
- vsyscall, vectors y vdso: Cian \033[96m
- Color de RESET: \033[0m

## Estrategia implementada

Una vez dicho lo anterior, ahora al programa. Como primer punto, se define a *main()*, en donde se le pide al usuario que ingrese el número PID del proceso para su posterior mapeo. Una vez terminado el mapeo (o error), se da la posibilidad de ingresar otro número PID
En *openFile(num_PID)* dentro de un bloque *try... except*, se trata de abrir el archivo usando el número ingresado. Si el archivo existe, se proceden a leer sus lineas. En caso contrario, se lanza un error.
Podrá observar que aproveché un poco sobre las facilidades que da Python sobre el poder hacer *return* con más de un valor regresado. Esto es porque vi que es más fácil obtener, en  *calcularSize*, el tamaño de la región de memoria y a su vez el número de páginas que esta usa. A su vez, en getMapeo, se pueden obtener tanto el color (usado posteriormente para la salida), el uso (la ruta o uso que se le da a la región de memoria), y el mapeo (el uso especifico).
Una vez obtenidos cada uno de los campos del renglón analizado, se guardan en una lista que posteriormente será usada para imprimir y obtener los espacios vacíos.

En *getMapeo* se define como valores iniciales a *mapeo = 'Anonymus'*, *uso = '[Anon]'*, y *color = '0m'*. En caso de encontrar una ruta especifica, o un uso especifico, estos valores se irán ajustando de acuerdo al uso de la región de memoria
En *getMemory(lista)*, se manda una lista de todas las filas encontradas en el archivo, con todos los campos encontrados y/o calculados. En esta función se hacen dos cosas: se identifican espacios en blanco, y se identifican a *Bid Datos* y *Bid Texto*. Por cada línea se hace la resta de la dirección inicial del renglón actual, menos la dirección final del renglón anterior, con el fin de encontrar vacios en la memoria. Si fuese el caso, se insertá una nueva fila en la lista, cuyos permisos no existirán y cuyo uso será *---vacio---*
Por último, solo se manda a imprimir la lista final obtenida de *getMemory*, en orden inverso. Dentro de esta función se encuentran otras que le dan un poco más de presentación a cada línea y campo a imprimir.

Como se mencionó, por último se vuelve a llamar a *main()* para que el usuario pueda ingresar otro PID

## Entorno de desarrollo

**Lenguaje de programación** Python 3.8
**Sistema Operativo** El programa fue escrito y ejecutado en Zorin OS 16.1

## ¿Cómo ejecutar?

Necesita tener instalado Python 3.8, y al abrir el archivo [proyecto3.py](/proyectos/3/BarriosFrancisco/proyecto3.py) se le pedirá ingresar el número PID

## Pantallazo

PD: No encontré un proceso con menos lineas en maps, así que le doy estas capturas, que no incluyen a todo el proceso, pero funciona (según yo jaja)

![Ejecución1](/proyectos/3/BarriosFrancisco/Imagenes/Ejecucion1.png)
![Ejecución2](/proyectos/3/BarriosFrancisco/Imagenes/Ejecucion2.png)

## Referencias
[Gestión de memoria](https://ocw.uc3m.es/ingenieria-informatica/sistemas-operativos/material-de-clase-1/mt_t4_l9.pdf)
[Implementing Virtual System Calls](https://lwn.net/Articles/615809/)
[Understanding the Linux /proc/id/maps File](https://www.baeldung.com/linux/proc-id-maps?msclkid=b99f0a63cf3f11ecaa0fb30fc95612a4)