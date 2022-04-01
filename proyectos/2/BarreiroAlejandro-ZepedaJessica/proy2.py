import threading
import time
import random
import os

esperando = 0
mutex = threading.Semaphore(1)
metrobus = threading.Barrier(1)
abordo = threading.Semaphore(0)

def partir(n):
	print("El metrobús ha partido. Pasajeros: %d" % n)

def abordar():
	global esperando
	print("El pasajero está llegando. Esperando: %d" % esperando)

def metrobus_llega():
	global esperando

	mutex.acquire()
	n = min(esperando, 10)
	metrobus = threading.Barrier(n)
	#for i in range(n):
		#abordo.acquire()

	esperando = max(esperando-10, 0)
	mutex.release()

	partir(n)

def pasajeros_abordan():
	global esperando

	mutex.acquire()
	esperando += 1
	mutex.release()

	metrobus.wait()
	abordar()
	#abordo.release()


while True:
	print("Llegada de metrobus")
	threading.Thread(target = metrobus_llega(), args = ()).start()
	for i in range(15):
		print("Pasajero %d" % i)
		threading.Thread(target = pasajeros_abordan(), args = ()).start()
