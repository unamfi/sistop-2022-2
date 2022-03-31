import threading
import time

pasajeros = 0
mutex = threading.Semaphore(1) #Utilizado para acceder a pasajeros
multiplex = threading.Semaphore(10) #Para que no haya más de 50 pasajeros en la zona de abordaje
metrobus = threading.Semaphore(1) #
metrobusLleno = threading.Semaphore(0)

def partir():
	print("El metrobús ha partido.")

def metrobus_llega():
	global pasajeros
	metrobus.release()

	mutex.acquire()

	if pasajeros > 0:
		metrobusLleno.acquire()
		partir()

	mutex.release()

def pasajeros_abordan():
	global pasajeros

	multiplex.acquire()
	mutex.acquire()

	pasajeros += 1

	mutex.release()
	metrobus.acquire()
	multiplex.release()

	pasajeros -= 1
	if pasajeros == 0:
		metrobusLleno.release()
	else:
		metrobus.release()

while True:
	print("Llegada de metrobus")
	threading.Thread(target = metrobus_llega(), args = ()).start()
	for i in range(15):
		print("Pasajero %d" % i)
		threading.Thread(target = pasajeros_abordan(), args = ()).start()
