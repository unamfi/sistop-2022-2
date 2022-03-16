import threading
import time
import random

num_hackers = 5
num_serfs = 5
barr_hackers = threading.Barrier(2)
barr_serfs = threading.Barrier(2)
barr_barca = threading.Barrier(4)
barr_inicia = threading.Barrier(4)
barco = threading.Semaphore(4)


def hackers (id:int):
    while True:
        time.sleep(5 * random.random())
        print('Hacker %d quiere subirse a un barco \n' % id)
        barr_hackers.wait()
        print('Hacker %d esperando subirse al barco \n' % id)
        barr_barca.wait()
        barco.acquire()
        print('Hacker %d subiendo al barco y empezando el viaje \n' % id)
        viaje()
        print('Hacker %d termino su cruce \n' % id)
        barco.release()

def serfs (id:int):
    while True:
        time.sleep(5 * random.random())
        print('Serf %d quiere subirse a un barco \n' % id)
        barr_serfs.wait()
        print('Serf %d esperando subirse al barco \n' % id)
        barr_barca.wait()
        barco.acquire()
        print('Serf %d subiendo al barco y empezando el viaje \n' % id)
        viaje()
        print('Serf %d termino su cruce \n' % id)
        barco.release()


def viaje():
    barr_inicia.wait()
    print('Viajando al otro lado del rio \n')
    time.sleep(1)
    print('Viaje terminado \n')

for i in range (num_hackers):
    threading.Thread(target=hackers, args=[i]).start()
for i in range (num_serfs):
    threading.Thread(target=serfs, args=[i]).start()