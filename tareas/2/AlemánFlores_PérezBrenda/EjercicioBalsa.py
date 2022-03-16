import threading
import time
import random


num_pasajeros = 40
pasajeros_para_salir = 4
p_tipo = 0.3
barr_pasajeros = threading.Barrier(pasajeros_para_salir)
salida_balsa = threading.Semaphore(0)
pasajero_en_balsa = threading.Semaphore(0)
#balsa = []
balsa_i=[]
mutex_balsa = threading.Semaphore(1)

def pasajeros(id:int):
    global balsa_i
    while True:
        time.sleep(5 * random.random())
        if random.random() < p_tipo:
            print('Aborda hacker %d' % id)
            with mutex_balsa:
                #balsa.append(id)
                balsa_i.append("hacker")
            barr_pasajeros.wait()
            with mutex_balsa:
                #if id == balsa[0]:
                    salida_balsa.release()
            pasajero_en_balsa.acquire()
        else:
            print('Aborda serf %d' % id)
            with mutex_balsa:
                #balsa.append(id)
                balsa_i.append("serf")
            barr_pasajeros.wait()
            with mutex_balsa:
                #if id == balsa[0]:
                    salida_balsa.release()
            pasajero_en_balsa.acquire()

def asientos():
    global balsa_i
    while True:
        print('*** Balsa: Abordar')
        salida_balsa.acquire()
        print('*** Balsa: Solicitando salida')
        mutex_balsa.acquire()
        if ((len(balsa_i) == 4) and ((balsa_i.count("hacker")==4) or (balsa_i.count("serf")==4) or (balsa_i.count("serf")==2) and (balsa_i.count("hacker")==2))):
            print('*** Balsa: Solicitud aceptada, saliendo')
            while len(balsa_i) > 0:
                #pasajeros = balsa.pop(0)
                pasajeros = balsa_i.pop(0)
                print('*** B: Dejando en el encuentro al pasajero %s...' % pasajeros)
                pasajero_en_balsa.release()
            mutex_balsa.release()
        elif (len(balsa_i)==0):
            print("Esperando pasajeros...")
            mutex_balsa.release()
        else:
            print('*** Balsa: solicitud denegada, balsa no balanceada, todos abajo')
            while len(balsa_i) > 0:
                #pasajeros = balsa.pop(0)
                pasajeros = balsa_i.pop(0)
                print('*** B: Bajando al pasajero %s...' % pasajeros)
                pasajero_en_balsa.release()
            mutex_balsa.release()
            



threading.Thread(target=asientos).start()
for i in range(num_pasajeros):
    threading.Thread(target=pasajeros,args=[i]).start()