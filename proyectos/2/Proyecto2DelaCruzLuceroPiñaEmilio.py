import threading
import time
import random

mutex=threading.Semaphore(1)
lugares_comida= threading.Semaphore(9)
sem_salsa= threading.Semaphore(2)
pagar= threading.Semaphore(1)

orden=0


#función encargada de procesar la orden del cliente si hay lugar disponible
def cliente_tacos():
	global mutex
	global lugares_comida
	


	num_random=0

	print('Quiero comer con el Champion')
	lugares_comida.acquire()  
	print('Si hay lugar, me sentare')
	mutex.acquire()
	time.sleep(5 * random.random())
	print('Deme 5 porfa')
	champion()
	num_random=random.randrange(0,2,1)
	if num_random == 1:
		print('Quiero salsa')
		salsa()
	pagar()
	print('Gracias me voy')
	mutex.release()
	lugares_comida.release()

def champion():
	global mutex
	global orden
	global lugares_comida
	

	print('Claro que si CHAMPIOOOOOOOOON, SALEN 5 <3')
	time.sleep(5 * random.random())
	orden += 1
	print('Ya van', orden)
	

def salsa():
	global sem_salsa

	sem_salsa.acquire()
	print('Poniendo salsa')
	sem_salsa.release()

def pagar():
	global pagar
	num_random=0
	num_random = 30
	print('toma', num_random)

try: 
	while True:
		time.sleep(5* random.random())
		threading.Thread(target=cliente_tacos).start()

except:
	print('')