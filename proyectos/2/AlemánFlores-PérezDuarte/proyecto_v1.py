import threading
import time
import random


num_cajas = 20
cajas_x_camion = 6
buena_caja = 0.3
barr_camion = threading.Barrier(cajas_x_camion)
salida_camion = threading.Semaphore(0)
caja_en_camion = threading.Semaphore(0)
balsa_i=[]
mutex_camion = threading.Semaphore(1)

def pasajeros(id:int):
    global balsa_i
    while True:
        time.sleep(5 * random.random())
        if random.random() < buena_caja:
            print('Se carga caja %d' % id)
            with mutex_camion:
                #balsa.append(id)
                balsa_i.append('Caja %d' %id)
            barr_camion.wait()
            with mutex_camion:
                #if id == balsa[0]:
                    salida_camion.release()
            caja_en_camion.acquire()

def asientos():
    global balsa_i
    while True:
        print('*** Camión: Cargando')
        salida_camion.acquire()
        print('*** Camión: Solicitando salida')
        mutex_camion.acquire()
        if (len(balsa_i) == 6):
            print('*** Camión: Solicitud aceptada, saliendo')
            while len(balsa_i) > 0:
                #pasajeros = balsa.pop(0)
                pasajeros = balsa_i.pop(0)
                print('*** Camión: Entregando al cliente la %s...' % pasajeros)
                caja_en_camion.release()
            mutex_camion.release()
        elif (len(balsa_i)==0):
            print("Esperando cargamento...")
            mutex_camion.release()
#         else:
#             print('*** Camión: solicitud denegada, cargamento insuficiente')
#             while len(balsa_i) > 0:
#                 #pasajeros = balsa.pop(0)
#                 pasajeros = balsa_i.pop(0)
#                 print('*** B: Bajando  %s...' % pasajeros)
#                 caja_en_camion.release()
#             mutex_camion.release()
            



threading.Thread(target=asientos).start()
for i in range(num_cajas):
    threading.Thread(target=pasajeros,args=[i]).start()
