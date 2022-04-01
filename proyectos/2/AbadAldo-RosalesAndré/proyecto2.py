# Proyecto 2: 

import threading
import time
import random

comiendo = 0
haciendoSobremesa = 0
listoParaIrse = Semaphore(0)
mutex = Semaphore(1)

def comensal(num):
    
    obtenerComida(num)
    
    mutex.acquire()
    comiendo+=1
    
    if comiendo == 2 and haciendoSobremesa == 1:
        listoParaIrse.release()
        haciendoSobremesa -= 1
    mutex.release()

    comer(num)
    
    mutex.acquire()
    comiendo -= 1
    haciendoSobremesa += 1

    if comiendo == 1 and haciendoSobremesa == 1:
        mutex.release()
        listoParaIrse.release()

    elif comiendo == 0 and haciendoSobremesa == 2:
        listoParaIrse.release()
        haciendoSobremesa -= 2
        mutex.release()

    else:
        haciendoSobremesa -= 1
        mutex.release()

    retirarse(num)




