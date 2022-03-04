import threading
import time
import random
mutex = threading.Semaphore(1)
elementos = threading.Semaphore(0)
maximo = threading.Semaphore(7)
buffer = []

class Evento:
    def __init__(self):
        self.ident = random.random()
        print("Generando evento %1.3f" % self.ident)
        time.sleep(0.5)
    def process(self):
        time.sleep(0.5)
        print("Procesando evento %1.3f; hay %d en el buffer" % (self.ident, len(buffer)))


def productor():
    while True:
        event = Evento()
        maximo.acquire()
        mutex.acquire()
        buffer.append(event)
        mutex.release()
        elementos.release()

def consumidor():
    while True:
        elementos.acquire()
        mutex.acquire()
        event = buffer.pop()
        maximo.release()
        mutex.release()
        event.process()

threading.Thread(target=productor, args=[]).start()
threading.Thread(target=consumidor, args=[]).start()
threading.Thread(target=consumidor, args=[]).start()
threading.Thread(target=consumidor, args=[]).start()
