import threading
import time
import random

personas_balsa = 0
hackers =  0
serfs = 0

mutex = threading.Semaphore(1)
mutex_balsa = threading.Semaphore(1)

def hack():
	global hackers
	global mutex
	global personas_balsa

	mutex.acquire()
	hackers += 1
	print('soy hacker y me quiero subir')
	time.sleep(5 * random.random())

	if hackers == 2 or hackers == 4:
		balsa()
	mutex.release()



def serf():
	global serfs
	global mutex
	global personas_balsa
	
	mutex.acquire()
	serfs += 1
	print('soy serf y me quiero subir')
	time.sleep(5 * random.random())
	
	if serfs == 2 or serfs == 4:
		balsa()
	mutex.release()



def balsa():
	global personas_balsa
	global hackers
	global serfs

	mutex_balsa.acquire()
	if hackers == 2 and serfs ==2 and personas_balsa==2:
		print ("La balsa está zarpando con 2 serfs y 2 hackers")
		personas_balsa = 0
		hackers = 0
		serfs = 0
	elif hackers == 2 and serfs != 2 and personas_balsa == 0:
		print('2 hackers esperando a 2 personas mas')
		personas_balsa += 2
	elif serfs == 2 and hackers != 2 and personas_balsa == 0:
		print('2 serfs esperando a 2 personas mas')
		personas_balsa += 2
	elif hackers == 4 or serfs == 4 and personas_balsa == 2:
		print ("La balsa está zarpando con 4 desarolladores iguales")
		personas_balsa = 0
		hackers = 0
		serfs = 0
	mutex_balsa.release()	


try:
	while True:
		for i in range(random.randrange(0,2,1)):
 			threading.Thread(target=hack).start()
		for i in range(random.randrange(0,2,1)):
			threading.Thread(target=serf).start()
except:
	print('')
