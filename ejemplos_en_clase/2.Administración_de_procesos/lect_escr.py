import time
import threading
lectores = 0
mutex = threading.Semaphore(1)
cuarto_vacio = threading.Semaphore(1)
flujo_justo = threading.Semaphore(1)

def escritor(num):
    print('Escritor %d iniciando...' % num)
    flujo_justo.acquire()
    cuarto_vacio.acquire()
    escribe()
    cuarto_vacio.release()
    flujo_justo.release()
    print('Escritor %d ya se va' % num)

def escribe():
    print('Estoy escribiendo...')
    time.sleep(2)
    print('Ya escribi.')

def lector(num):
    global lectores
    print('Lector %d iniciando' % num)
    flujo_justo.acquire()
    flujo_justo.release()

    mutex.acquire()
    lectores = lectores + 1
    if lectores == 1:
        cuarto_vacio.acquire()
    mutex.release()
    print('Lector %d ya se va' % num)

    lee()

    mutex.acquire()
    lectores = lectores - 1
    if lectores == 0:
        cuarto_vacio.release()
    mutex.release()

def lee():
    print('Estoy leyendo')
    time.sleep(0.5)
    print('Ya lei')

def lanza_lectores():
    num=0
    while True:
        threading.Thread(target=lector, args=[num]).start()
        time.sleep(0.3)
        num += 1

def lanza_escritores():
    num=0
    while True:
        threading.Thread(target=escritor, args=[num]).start()
        time.sleep(1)
        num += 1

threading.Thread(target=lanza_lectores).start()
threading.Thread(target=lanza_escritores).start()
