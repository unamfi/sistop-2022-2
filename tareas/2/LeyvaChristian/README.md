# Tarea 2 Christian Leyva: El servidor web

El ejercicio que decidí realizar fue el ejercicio 6 *"El servidor web"*, el cual consiste en la idea de un servidor web donde hay un "jefe" que espera a que lleguen solicitudes a este para repartir el trabajo entre sus *k* trabajadores.

## Entorno de desarrollo
El programa fue desarrollado en el lenguaje de programación **Python 3** , por lo cual se necesita tener este instalado para poder ejecutarlo.

## Estrategia de sincronización
....

## Refinamientos
Dentro del ejercicio se plantea el siguiente refinamiento:

> "Seguimiento del sistema: ¿Cómo implementarías lo necesario para
> mantener información de contabilidad?
> → Cada hilo debe notificar antes de terminar su ejecución, entregando información de su rendimiento.
> → Por ejemplo, qué página fue solicitada."

El cual implemente (ya usted me dirá si fue de la manera correcta) haciendo que al momento de que un hilo *Trabajador* "termine" de realizar una conexión, indique el nombre de la página que cargo el trabajador y el estado de la conexión (La cual debe ser terminada).
Esto lo hice con las siguientes líneas de código:
~~~
	# El trabajador se tarda en realizar la conexion...

	time.sleep(2*random.random())

	with mutex_conexion:

		pagina = fila_solicitudes.pop(0)

	print('T{}: Pagina {} cargada correctamente '.format(id,pagina))
~~~
Como se puede apreciar, el trabajador tarda en realizar la tarea un tiempo y después mediante un mutex hace un pop() en la lista que contiene el nombre de las paginas que solicitaron conexión al servidor y resuelve la primera de la fila. 
En esta parte utilicé un mutex para obtener el primer elemento de la fila, debido a que al mismo tiempo que el trabajador esta realizando la conexión, mas páginas pueden estar solicitando una conexión en la misma lista ( o otro trabajador puede estar trabajando).
Finalmente el trabajador indica el nombre de la pagina que fue cargada.
