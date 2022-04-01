import threading
import time
import random
import interfaz as inte

N = 6  # Maximo de colegas que soportta nuestro programador
W = 4  # Maximo de colegas esperando por desbloqueo
E = 5  # Errores minimos que deben de haber

# Variables auxiliares
puertaCerrada = False
numCompaneros = 7
programadorMali = True
jefePresente = False
jefeCamino = False

# Semaforos y estructuras a utilizar
salidaProg = threading.Semaphore(0)  # Señal de salida del programador
alertaApagada = threading.Semaphore(0) # Señal de apagado de la alarma
puertaMagnetica = threading.Semaphore(1)  # Torniquete de entrada
mutex = threading.Semaphore(1)  # Protector de todas las variables de condicion.
mutex2 = threading.Semaphore(1) # Protector de variables de condicion
puedeEntrar = threading.Semaphore(1) #Apagador para evitar que el programador malicioso este en la sala a la vez que el jefe
barrReparacion = threading.Barrier(numCompaneros) #Barrera para que los colegas vallan juntos a reparar el error de la alarma

# Varables de condicion
colegasPresentes = 0 # Contador de colegas esperando el ingreso en la sala
colegasEsperando = 0  # Colegas esperando por el desbloqueo
numErrores = 0  #Contador de errores totales en la sala
activarAlarma = False # Alarma que desaloja a los colegas de la sala

# definicion del comportamiento del jefe
def jefe():

	# Variables globales usadas en jefe
	global  jefePresente, jefeEnSala, jefeCamino

	# Inicio de ciclo infinito
	while True:

		# Comportamiento del jefe frente a una alarma
		if activarAlarma:
			refrescarPantalla('El jefe fue a ver la alarma')
			alertaApagada.acquire()

		# Comportamiento del jefe sin la alarma
		else:
			time.sleep(random.random() * 15)

			puedeEntrar.acquire()
			refrescarPantalla('El jefe esta en camino')
			jefeCamino = True # Aviso para que el programador malicioso pueda salir
			salidaProg.acquire()

			# Comportamiento del jefe en la sala
			puertaMagnetica.acquire()
			refrescarPantalla('Jefe entrando a la sala')
			puertaMagnetica.release()
			jefePresente = True
			time.sleep(random.random())

			# Tiempo el cual el jefe permanecera en la sala
			refrescarPantalla('El jefe esta supervisando el trabajo')
			time.sleep(random.random() * 5)
			refrescarPantalla('El jefe termino la supervision y va a salir')
			jefePresente = False
			refrescarPantalla('El jefe se fue de la sala')
			puedeEntrar.release()
			jefeCamino = False

# Definicion del comportamiento del programador malicioso
def progMalicioso():
	global colegasPresentes, numErrores, jefeCamino, activarAlarma, colegasEsperando, puertaCerrada,programadorMali
	while True:

		# Comportamiento que va a tener el programador malicioso frente a la disminucion de los errores por debajo del limite
		if numErrores < E:
			#Activacion de la alarma
			refrescarPantalla('Activando la alarma')
			activarAlarma = True

			# Comportamiento del programador malicioso cuando la alarma esta activa pero sus colegas no han desalojado la sala
			while colegasPresentes != 0:
				time.sleep(random.random())
				mutex.acquire()
				numErrores = numErrores + 1
				mutex.release()
				refrescarPantalla('Programando errores')

			# Cierre del torniquete para evitar el ingreso
			puertaMagnetica.acquire()
			puertaCerrada = True
			refrescarPantalla('Cerrando la puerta para evitar el ingreso')

			# Comportamiento del programador malicioso cuando no hay compañeros o cuando los errores son menores a 20 
			while colegasEsperando < W or numErrores < 20:
				time.sleep(random.random()*0.5)
				mutex.acquire()
				numErrores = numErrores + 1
				refrescarPantalla('Programando errores')
				mutex.release()

			# Liberacion del torniquete para el acceso de los compañeros a la sala
			puertaMagnetica.release()
			puertaCerrada = False
			refrescarPantalla('Abriendo la puerta para el ingreso de colegas')

		# Comportamiento frente a la llegada del jefe por parte del programador malicioso
		elif jefeCamino:
			refrescarPantalla('Saliendo rapidamente de la sala')
			puertaMagnetica.acquire()
			puertaMagnetica.release()
			programadorMali = False
			refrescarPantalla('Tomando descanso para evitar ser descubierto')
			salidaProg.release()

			# Espera por el apagador para poder entrar a la sala
			puedeEntrar.acquire()
			refrescarPantalla('Regresando del descanso')
			puertaMagnetica.acquire()
			puertaMagnetica.release()
			programadorMali = True
			refrescarPantalla('Volviendo a programar errores')
			puedeEntrar.release()

		#Comportamiento normal del programador malicioso
		else:
			time.sleep(random.random())
			mutex.acquire()
			numErrores = numErrores + 1
			mutex.release()
			refrescarPantalla('Programando errores')

# Definicion del comportamiento de los colegas
def colega (id:int):

	# Variables globales que utiliza colega
	global colegasPresentes, colegasEsperando, numErrores, activarAlarma

	# Ingreso de los colegas por primera vez a la sala
	mutex2.acquire()
	colegasPresentes = colegasPresentes + 1
	mutex2.release()
	refrescarPantalla('Colega %d ingresando a la sala' % id)
	puertaMagnetica.acquire()
	puertaMagnetica.release()

	# Comportamiento definido de los colegas una vez que ya ingresaron a la sala
	while True:
		# Comportamiento de los colegas cuando la alarma esta activa
		if activarAlarma:
			puertaMagnetica.acquire()
			mutex2.acquire()
			colegasPresentes = colegasPresentes - 1
			mutex2.release()
			puertaMagnetica.release()
			refrescarPantalla('Programador %d fue a solucionar el problema' % id)
			barrReparacion.wait()

			refrescarPantalla('Programador %d llendo a solucionar el problema' % id)
			time.sleep(10*random.random())
			mutex2.acquire()
			if colegasPresentes == 0 and activarAlarma == True:
				activarAlarma = False
				alertaApagada.release()
			mutex2.release()

			mutex2.acquire()
			colegasEsperando = colegasEsperando + 1
			mutex2.release()
			refrescarPantalla('Programador %d regresando a la sala' % id)
			puertaMagnetica.acquire()
			mutex2.acquire()
			colegasEsperando = colegasEsperando - 1
			colegasPresentes = colegasPresentes + 1
			mutex2.release()
			refrescarPantalla('Programador %d en la sala' % id)
			puertaMagnetica.release()

		#Comportamiento de los colegas cuando la alarma esta desactivada
		else:
			time.sleep(10*random.random())
			mutex.acquire()
			numErrores = numErrores - 1
			mutex.release()
			refrescarPantalla('Programador %d resolvio un error' % id)

# Definicion de como se refrescara la pantalla
def refrescarPantalla(msg):

	# Variables usadas en el desarrollo del manejo de pantalla
	global puertaCerrada, numErrores, colegasPresentes, colegasEsperando, activarAlarma, programadorMali

	# Actualizacion de los colegas adentro y fuera de la sala, asi mismo se actualiza la cantidad de errores que se tiene
	inte.escena[0] = " " + ("Colegas Presentes = %d" % colegasPresentes) + " " +("Numero de Errores = %d" % numErrores)
	inte.escena[8] = " " + ("C"*colegasEsperando) + (" "*(20-colegasEsperando))
	inte.escena[2] = "|" + ("C"*colegasPresentes) + (" "*(20-colegasPresentes)) + "|"

	# Cambio en la escena en caso de que la puerta este cerrada
	if puertaCerrada:
		inte.escena[7] = "°---------------------------°"
	else:
		inte.escena[7] = "°------------   ------------°"

	# Cambio en la escena si el jefe se encuentra adentro
	if jefePresente:
		inte.escena[5] = "|             J             |"
	else:
		inte.escena[5] = "|                           |"

	#Cambio de la escena si el programador malicioso se encuentra adentro
	if programadorMali:
		inte.escena[3] = "|P                          |"
		inte.escena[6] = "|                           |"
	else:
		inte.escena[6] = "|                           |P"
		inte.escena[3] = "|                           |"

	inte.escena[9] = msg

	#Señal de uno de los hilos para actualizar
	inte.senalHilos.release()

	#Espera para poder enviar su actualizacion
	inte.senalActu.acquire()
