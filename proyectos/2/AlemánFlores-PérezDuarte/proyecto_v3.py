import threading
import time
import random


num_cajas = 20
num_camiones= 6
cajas_x_camion = 4
buena_caja = 0.3
barr_camion = threading.Barrier(cajas_x_camion)
barr_camiones = threading.Barrier(num_camiones)
salida_camion = threading.Semaphore(0)
caja_en_camion = threading.Semaphore(0)
lst_cajas=[[],[],[],[],[],[]]
mutex_cajas = threading.Semaphore(1)

def cajas(idcaj:int,idcam:int):
    global lst_cajas
    while True:
        time.sleep(5 * random.random())
        if random.random() < buena_caja:
            print('Se carga caja',idcaj,'al camión',idcam)
            with mutex_cajas:
                #balsa.append(id)
                lst_cajas[idcam].append('Caja',idcaj)
            barr_camion.wait()
#             with mutex_cajas:
#                 #if id == balsa[0]:
#                     salida_camion.release()
            caja_en_camion.acquire()
def camiones(idcam:int):
    global lst_cajas
    while True:
#         print("**************************************************",idcam)
#         print("/////////////////////////////////////////",type(idcam))
#         idcamion = id(idcam)
#         print("#####################",idcamion)
#         print("$$$$$$$$$$$$$$$$$$$$$",type(idcamion))
        cajas(int,idcam)
        barr_camiones.wait()
        if idcam==1:
            print('Solicitando la salida')
            salida_camion.release()
        
def salida():
    global lst_cajas
    while True:
        print('*** Camión: Esperando cargamento...')
        salida_camion.acquire()
        mutex_cajas.acquire()
        if (len(lst_cajas[0]) == cajas_x_camion and len(lst_cajas[1]) == cajas_x_camion and len(lst_cajas[2]) == cajas_x_camion and len(lst_cajas[3]) == cajas_x_camion and len(lst_cajas[4]) == cajas_x_camion and len(lst_cajas[5]) == cajas_x_camion):
            for i in range (num_camiones):
                print('*** Camión',i,': Saliendo')
                while len(lst_cajas[i]) > 0:
                    caja = lst_cajas[i].pop(0)
                    print('*** Camión',i,': Entregando al cliente la',caja)
                    caja_en_camion.release()
                mutex_cajas.release()
                print("*** Camión",i,": Regresando a origen")
        elif ((len(lst_cajas[0])==0) or (len(lst_cajas[1])==0) or (len(lst_cajas[2])==0) or (len(lst_cajas[3])==0) or (len(lst_cajas[4])==0) or (len(lst_cajas[5])==0)):
            mutex_cajas.release()
        else:
            print("Revisando faltantes de caja en camiones")
            for i in range (num_camiones):
                print('*** Camión %d: Saliendo' %i)
                while len(lst_cajas[i]) > 0:
                    caja = lst_cajas[i].pop(0)
                    #print('*** Camión',i': Entregando al cliente la',caja)
                    caja_en_camion.release()
            mutex_cajas.release()


threading.Thread(target=salida).start()
for i in range(num_cajas):
    threading.Thread(target=cajas,args=[i,int]).start()
for i in range(num_camiones):
    threading.Thread(target=camiones,args=[i]).start()