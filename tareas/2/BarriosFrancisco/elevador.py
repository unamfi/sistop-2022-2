import threading
import random
import time
num_personas = 10;
num_pisos = 5
personas_en_elevador = []
multiplex = threading.Semaphore(5)
mutex = threading.Semaphore(1)
torniquete = threading.Semaphore(1)
piso_actual = 1
piso_a_llegar = []

def caja():
	global sube
	global piso_actual
	while True:
		if len(piso_a_llegar) != 0:
			piso_siguiente = piso_a_llegar.pop(0)
			if piso_siguiente < piso_actual:
				while piso_actual > piso_siguiente:
					piso_actual = piso_actual - 1
				print 'Llegando a piso ', piso_actual
			elif piso_siguiente > piso_actual:		
				while piso_actual < piso_siguiente:
					piso_actual = piso_actual + 1
				print 'Llegando a piso ', piso_actual
def persona(id):
	global piso_a_llegar
	global piso_actual
	while True:
		torniquete.acquire()
		torniquete.release()
		piso_de_persona = random.randrange(0, num_pisos)
		mutex.acquire()
		print 'P ', id, 'toca elevador en piso' , piso_de_persona
		piso_a_llegar.append(piso_de_persona)
		while piso_actual != piso_de_persona:
			time.sleep(0.01)
		mutex.release()

		multiplex.acquire()
		mutex.acquire()
		print 'P ',id, ': Ya tome el elevador'
		personas_en_elevador.append(id)
		piso_destino = random.randrange(0, num_pisos)
		while piso_destino == piso_actual:
			piso_destino = random.randrange(0, num_pisos)
		print 'P ',id, ': Voy para el piso',piso_destino
		piso_a_llegar.append(piso_destino)
		mutex.release()

		mutex.acquire()
		while piso_actual != piso_destino:
			time.sleep(0.01)
		print 'P ',id,': Llegue al piso', piso_actual
		personas_en_elevador.remove(id)
		mutex.release()
		multiplex.release()
		
personas = [threading.Thread(target = persona, args = [i]).start() for i in range(num_personas)]
elevador = threading.Thread(target = caja).start()
		
