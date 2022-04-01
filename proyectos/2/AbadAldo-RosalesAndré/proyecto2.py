# Proyecto 2: 

import threading
import time
import random

comiendo = 0
haciendoSobremesa = 0
listoParaIrse = threading.Semaphore(0)
mutex = threading.Semaphore(1)

def comensal(num):
   
    global comiendo, haciendoSobremesa
    obtenerComida(num)
    
    mutex.acquire()
    comiendo+=1
    
    print("Comensal #%d verificando si se puede sentar..." % num)
    if comiendo == 2 and haciendoSobremesa == 1:
        listoParaIrse.release()
        haciendoSobremesa -= 1
    mutex.release()

    comer(num)
    
    mutex.acquire()
    comiendo -= 1
    haciendoSobremesa += 1

    if comiendo == 1 and haciendoSobremesa == 1:
       
        print("Comensal #%d esperando a que otro comensal termine de comer..." % num)
        mutex.release()
        listoParaIrse.acquire()

    elif comiendo == 0 and haciendoSobremesa == 2:
        print("Comensal #%d notificando que ha terminado al comensal que lo esté esperando..." % num)
        listoParaIrse.release()
        haciendoSobremesa -= 2
        mutex.release()

    else:
        print("Comensal #%d se ha quedado solo... mejor irse" % num)
        haciendoSobremesa -= 1
        mutex.release()

    retirarse(num)

def obtenerComida(num):
    print("Comensal #%d consiguiendo comida..." % num)
    time.sleep(random.random() / 100)

def comer(num):
    print("Comensal #%d sentandose a comer..." % num)
    time.sleep(random.random() / 100)

def retirarse(num):
    print("Comensal #%d retirándose..." %num)
    time.sleep(random.random() / 100)

for i in range(4):
    threading.Thread(target=comensal, args=[i]).start()
