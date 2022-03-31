import threading
import time
import random


num_cajas = 20
cajas_x_camion = 6
buena_caja = 0.3
barr_camion = threading.Barrier(cajas_x_camion)
salida_camion = threading.Semaphore(0)
caja_en_camion = threading.Semaphore(0)
lst_cajas=[]
mutex_camion = threading.Semaphore(1)

def cajas(id:int):
    global lst_cajas
    while True:
        time.sleep(5 * random.random())
        if random.random() < buena_caja:
            print('Se carga caja %d' % id)
            with mutex_camion:
                #balsa.append(id)
                lst_cajas.append('Caja %d' %id)
            barr_camion.wait()
            with mutex_camion:
                #if id == balsa[0]:
                    salida_camion.release()
            caja_en_camion.acquire()

def camion():
    global lst_cajas
    while True:
        print('*** Camión: Esperando cargamento...')
        salida_camion.acquire()
        mutex_camion.acquire()
        if (len(lst_cajas) == 6):
            print('*** Camión: Saliendo')
            while len(lst_cajas) > 0:
                pasajeros = lst_cajas.pop(0)
                print('*** Camión: Entregando al cliente la %s...' % pasajeros)
                caja_en_camion.release()
            mutex_camion.release()
            print("*** Camión: Regresando a origen")
        elif (len(lst_cajas)==0):
            mutex_camion.release()


threading.Thread(target=camion).start()
for i in range(num_cajas):
    threading.Thread(target=cajas,args=[i]).start()
