import threading
import time
import random
import os

esperando = 0 #Número de personas esperando
mutex = threading.Semaphore(1) #Mutex para modificar el número de personas esperando
metrobus = threading.Barrier(1) #Barrera para dejar entrar en el metrobús
abordo = threading.Semaphore(0) #Semáforo para las personas que hayan abordado

#Función que indica que un metrobús ha partido y con cuántos pasajeros
def partir(n):
	print("El metrobús ha partido. Pasajeros: %d" % n)

#Función que indica que el pasajero ha llegado a abordar y cuántas personas están esperando.
def abordar():
	global esperando
	print("El pasajero está llegando. Esperando: %d" % esperando)

#Función del metrobús
def metrobus_llega():
	global esperando
	
	#Se utiliza mutex para manipular esperando
	mutex.acquire()
	n = min(esperando, 10) #Cantidad de pasajeros que tendrá el metrobús
	metrobus = threading.Barrier(n) #Nueva barrera de gente esperando
	for i in range(n):
		abordo.acquire() #Se espera a que los pasajeros entren

	esperando = max(esperando-10, 0) #Se calcula el nuevo número de esperando
	mutex.release()

	partir(n) #El metrobús se va de la estación

def pasajeros_abordan():
	global esperando

	#Mutex para modificar la variable de esperando. 
	mutex.acquire()
	esperando += 1
	mutex.release()
	
	#Se espera a la barrera del metrobús
	metrobus.wait()
	abordar() #El pasajero está llegando
	abordo.release() #Se aborda en el metrobús


#Interfaz de usuario
while True:
	os.system('clear') #Se limpia la pantalla. Comando de Linux y MacOS

	#Se generan entre 1 y 15 pasajeros nuevos que llegarán a la estación.
	n = random.randint(1, 15) 
	print("Llegada de %d pasajero(s)" % n)
	for i in range(n):
		threading.Thread(target = pasajeros_abordan()).start()
	
	#Se genera entre 1 y 2 metrobuses para el uso de los pasajeros
	n = random.randint(1, 2)
	print("Llegada de %d metrobus" % n)
	for i in range(n):
		threading.Thread(target = metrobus_llega()).start()
	
	#Después de la llegada de los metrobuses se imprime las personas esperando.
	print("Personas esperando: %d" % esperando)
	
	#Línea para que el usuario decida el flujo del programa.
	if(input("Pulsar enter para continuar. Ingresar q para salir: ") == 'q'):
		break;

