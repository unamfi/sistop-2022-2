# Tarea 2 Christian Leyva: El servidor web

El ejercicio que decidí realizar fue el ejercicio 6 *"El servidor web"*, el cual consiste en la idea de un servidor web donde hay un "jefe" que espera a que lleguen solicitudes a este para repartir el trabajo entre sus *k* trabajadores.

## Entorno de desarrollo
El programa fue desarrollado en el lenguaje de programación **Python 3** , por lo cual se necesita tener este instalado para poder ejecutarlo.

## Estrategia de sincronización

### Señalización
La estrategia que utilize para resolver el problema fue principalmente la **Señalización** debido a que el hilo Jefe consta de un semáforo el cual esta inicializado en 0 y cuando el jefe realiza un acquire, este espera a que un hilo Pagina solicite una conexión al servidor para "despertar" al Jefe.

~~~
def Pagina(nombre):
    global fila_solicitudes
    while True:
        time.sleep(3 * random.random())
        if random.random() < p_conexion:
            print('{}: Nueva solicitud.'.format(nombre))
            with mutex_conexion:
                fila_solicitudes.append(nombre)
                nueva_solicitud.release()

def Jefe():
    while True:
        print("Jefe: Esperando solicitudes...")
        nueva_solicitud.acquire()
        print("Jefe: Atendiendo solicitud...")
        semaforo_trabajadores.release()
~~~

Lo mismo sucede con los hilos **Trabajador**, estos utilizan un semáforo inicializado en 0, donde al comienzo los *k* trabajadores duermen al no tener trabajo con un acquire en el semáforo y esperan a que alguien los despierte.

El Jefe los despierta al momento de que se le solicita a este una solicitud:
~~~
def Trabajador(id:int):
    global fila_solicitudes
    while True:
        print('T%d: No hay trabajo, a mimir. zzz...'%id)
        semaforo_trabajadores.acquire()
        print('T%d: Aghh mas trabajo...'%id)
        # El trabajador se tarda en realizar la conexion...
        time.sleep(2*random.random())
        with mutex_conexion:
            pagina = fila_solicitudes.pop(0)
        print('T{}: Pagina {} cargada correctamente '.format(id,pagina))
~~~

### Mutex

Ademas de utilizar la señalización, también utilice la estrategia de mutex, debido a que por mi forma de resolver el problema se tiene una *n* cantidad de hilos *Pagina* , los cuales solicitan *j* cantidades de conexiones. Cuando una pagina solicita una conexión, guarda su solicitud en una lista (mediante un mutex), y esta lista la utilizan los trabajadores para obtener el nombre de la pagina a la que van a crear la conexión.

El mutex es necesario ya que muchos hilos a la vez acceden a la misma lista.

## Refinamientos
Dentro del ejercicio se plantea el siguiente refinamiento:

> "Seguimiento del sistema: ¿Cómo implementarías lo necesario para
> mantener información de contabilidad?
> → Cada hilo debe notificar antes de terminar su ejecución, entregando información de su rendimiento.
> → Por ejemplo, qué página fue solicitada."

El cual implemente (ya usted me dirá si fue de la manera correcta) haciendo que al momento de que un hilo *Trabajador* "termine" de realizar una conexión, indique el nombre de la página que cargo el trabajador y el estado de la conexión (La cual debe ser terminada).
Esto lo hice con las siguientes líneas de código:
~~~
	# El trabajador se tarda en realizar la conexión...

	time.sleep(2*random.random())

	with mutex_conexion:

		pagina = fila_solicitudes.pop(0)

	print('T{}: Pagina {} cargada correctamente '.format(id,pagina))
~~~
Como se puede apreciar, el trabajador tarda en realizar la tarea un tiempo y después mediante un mutex hace un pop() en la lista que contiene el nombre de las paginas que solicitaron conexión al servidor y resuelve la primera de la fila. 
En esta parte utilicé un mutex para obtener el primer elemento de la fila, debido a que al mismo tiempo que el trabajador esta realizando la conexión, mas páginas pueden estar solicitando una conexión en la misma lista ( o otro trabajador puede estar trabajando).
Finalmente el trabajador indica el nombre de la pagina que fue cargada.
