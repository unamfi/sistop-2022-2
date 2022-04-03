import threading
import time
import random


num_camiones= 6
cajas_x_camion = 5
barr_camiones = threading.Barrier(num_camiones)
salida_camion = threading.Semaphore(0)
caja_en_camion = threading.Semaphore(0)
lst_cajas=[[],[],[],[],[],[]]
mutex_camion = threading.Semaphore(1)

def camiones(id:int):
    while True:
        llenado(id)
        barr_camiones.wait()
        if (len(lst_cajas[0]) == cajas_x_camion and len(lst_cajas[1]) == cajas_x_camion and len(lst_cajas[2]) == cajas_x_camion and len(lst_cajas[3]) == cajas_x_camion and len(lst_cajas[4]) == cajas_x_camion and len(lst_cajas[5]) == cajas_x_camion):
            print("Camión",id,"solicitando la salida")
            salida_camion.release()

def llenado(id:int):
    time.sleep(5 * random.random())
    with mutex_camion:
        for i in range (cajas_x_camion):
            print("Añadiendo la caja",i,"al camión",id)
            lst_cajas[id].append(i)

def salida():
    global lst_cajas
    while True:
        print('*** Camión: Esperando cargamento...')
        salida_camion.acquire()
        mutex_camion.acquire()
        if (len(lst_cajas[0]) == cajas_x_camion and len(lst_cajas[1]) == cajas_x_camion and len(lst_cajas[2]) == cajas_x_camion and len(lst_cajas[3]) == cajas_x_camion and len(lst_cajas[4]) == cajas_x_camion and len(lst_cajas[5]) == cajas_x_camion):
            print("!!!!!!!!!!!!!!!Los 6 camiones están saliendo!!!!!!!!!!!!!!!!!")
            for i in range (num_camiones):
                while len(lst_cajas[i]) > 0:
                    caja = lst_cajas[i].pop(0)
                    print('*********** Camión',i,': Entregando al cliente la caja',caja)
                    caja_en_camion.release()
                print("*** Camión",i,": Regresando a origen")
            mutex_camion.release()
        elif (len(lst_cajas[0])==0 and len(lst_cajas[1])==0 and len(lst_cajas[2])==0 and len(lst_cajas[3])==0 and len(lst_cajas[4])==0 and len(lst_cajas[5])==0):
            mutex_camion.release()


threading.Thread(target=salida).start()
for i in range(num_camiones):
    threading.Thread(target=camiones,args=[i]).start()