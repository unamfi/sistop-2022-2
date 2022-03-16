import threading
import time
import random
import time

num_hackers = 0
num_serfs = 0
barrera_balsa = threading.Barrier(4)
mutex = threading.Semaphore(1)
hackerQueue = threading.Semaphore(0)
serfQueue = threading.Semaphore(0)
balsa_num = 0

def abordando(id):
  print("Ha llegado un: " + id)

def navegar():
  global balsa_num
  print("Listo para navegar!!! Balsa %d" % balsa_num)
  balsa_num += 1

def hackers():
  global num_hackers, num_serfs
  lider = False

  mutex.release()
  num_hackers += 1
  if num_hackers == 4:
    hackerQueue.acquire(4)
    num_hackers = 0
    lider = True
  elif num_hackers == 2 and num_serfs >= 2:
    hackerQueue.acquire(2)
    serfQueue.acquire(2)
    num_serfs -= 2
    num_hackers = 0
    lider = True
  else:
    mutex.release()
  
  hackerQueue.release()

  abordando("hacker")
  barrera_balsa.wait()

  if lider:
  	navegar()
  	mutex.acquire()

def serfs():
  global num_hackers, num_serfs
  lider = False

  mutex.release()
  num_serfs += 1
  if num_serfs == 4:
    serfQueue.acquire(4)
    num_serfs = 0
    lider = True
  elif num_serfs == 2 and num_hackers >= 2:
    serfQueue.acquire(2)
    hackerQueue.acquire(2)
    num_hackers -= 2
    num_serfs = 0
    lider = True
  else:
    mutex.release()
  
  serfQueue.release()

  abordando("serf")
  barrera_balsa.wait()

  if lider:
  	navegar()
  	mutex.acquire()

while True:
  if random.randint(0,9) >= 6:
  	threading.Thread(target = hackers, args = ()).start()
  else:
  	threading.Thread(target = serfs, args = ()).start()
  time.sleep(1)
