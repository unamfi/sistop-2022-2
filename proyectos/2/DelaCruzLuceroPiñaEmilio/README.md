#Proyecto 2. Una situación cotidiana paralelizable
***
##LOS TACOS DE CANASTA DEL CHAMPION
***

####Fecha de entrega: 31/03/2022
***
####Integrantes:
***
	-De la Cruz Lucero 
	-Piña Emiliano

##Identificacion y descripcion del problema
***
Al momento de nosotros ir por tacos de canasta, nos dimos cuenta que siempre había un problema al llegar puesto que no había organización, no hay lugar para sentarse y por más que el mexicano esté acostumbrado a comer parado, al ponerle salsa a tu taco de canasta corres el riesgo de perder el control y mancharte todo solo por no haberte podido sentar.Decidimos implementar éste código para ayudarle al Champion a tener una mejor organización y poder ofrecer un mejor servicio a los alumnos

##### Consecuencias de la concurrencia
***
Al no haber un lugar en donde sentarse a comer, el champion pierde clientes puesto que las personas que decidan esperar por un lugar pueden esperar por mucho tiempo, provocando que lleguen tarde a sus clases y por ende decidan nunca más complarle al champion.Otro escenario sería el que haya tanta gente esperando que la administración de la unam decida que el negocio de tacos del champion es ineficiente y estorboso, provocando que lo clausuren.

##### Eventos que quisieran controlarse
***
Que los alumnos lleguen tarde a sus clases y que el champion no se vaya a la quiebra


##Mecanismos de sincronización empleados:
***
hilos, mutex y semáforos

##Lógica de operación
***


###Identificación del estado compartido (variables o estructuras globales)
***
Se empleó una variable global llamada orden,se encarga de contar todos los pedidos que el champion reciba y venda, de ése modo, al final del día, con éste número, podría saber cuánto dinero generó. 

###Descripción algorítmica del avance de cada hilo/proceso
***
-El programa empieza en cliente_tacos, en donde se genera la demanda de clientes, llega gente esperando poder comer una orden de tacos, se adquiere el semáforo declarado tamaño 9, apartir de ello, el cliente ahora ya puede sentarse y se llama al mutex para que el cliente empiece a ordenar. Se llama a la función champion en la que se aumenta el contador de ordenes totales.Aun dentro de la funcion inicial de cliente, se genera un numero random entre cero y dos, si el número dado es 1, se asumirá que el cliente quiso ponerle salsa a sus tacos, llamando ahora a la funcion salsa en la que se adquiere en semaforo sem_salsa, se imprime el agregado de la salsa y despues se libera el semaforo.La ultima parte de esta funcion antes de liberar el mutex es pagar, en la que simplemente se imprime el total pagado de una orden de tacos. Se libera el mutex y se libera el semáforo lugares_comida

###Descripción de la interacción entre ellos (sea mediante los mecanismos de sincronización o de alguna otra manera)
***
los dos elementos más importantes fueron el mutex y el semáforo lugares_comida puesto que el mutex aseguraba que un cliente pudiera consumir su orden de tacos y el semaforo se encargaba de que no mas de n hilos(semaforo declarado de tamaño máximo de 9) accedieran al recurso que era comer con el champion. Se delimitó a 9 pero se sabe que al momento de que una persona terminara podia otra tomar su lugar, las personas no comen igual de rápido y el flujo de gente es constante

##Descripción del entorno de desarrollo, suficiente para reproducir una ejecución exitosa
***
No se ocupó ningun entorno de desarrolo para desarrollar éste programa, se optó por un procesador de textos básico, todas las ejecuciones se probaron en la terminal.

###¿Qué lenguaje emplean? ¿Qué versión?
***
Python 3.7.9 

###¿Qué bibliotecas más allá de las estándar del lenguaje?
***
TIME, RANDOM, THREADING

###¿Bajo qué sistema operativo / distribución lo desarrollaron y/o probaron?
***
MacOS y Windows

##Ejemplos o pantallazos de una ejecución exitosa
![Pantallazo] (sistop-2022-2/proyectos/2/DelaCruzLucero-PiñaEmilio/CapturaEJECUCIONEXITOSA.png)
