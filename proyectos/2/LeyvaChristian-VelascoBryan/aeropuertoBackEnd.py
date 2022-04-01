
#Aeropuerto Felipe Ángeles#
from threading import Semaphore, Thread
from time import sleep, time
import random

pistaDeAviacion = Semaphore(0)
mutexRadioAvion = Semaphore(1)
mensaje = 0
mutexRadioTorreDeControl = Semaphore(0)
andenPasajeros = Semaphore(10)
andenMercancia = Semaphore(6)

def avionComercial(ref:int):
    global pistaDeAviacion
    start = time()
    print("\t 🛩️  Aquí avión comercial No. " + str(ref) + ", solicita permiso para aterrizar.")
    comunicacion(ref)
    pistaDeAviacion.acquire()
    print("\tAvión " + str(ref) + " en tierra.")
    descargaPAX(ref)
    cargaPAX(ref)
    #Avión en zona de espera terrestre
    comunicacion(ref)
    pistaDeAviacion.acquire()
    finish = time() - start
    print(">>Avión comercial No. " + str(ref) + " en aire, {0:.1f} horas en aeropuerto.<<".format(finish))

def descargaPAX(ref:int):
    global pistaDeAviacion,andenPasajeros
    andenPasajeros.acquire()
    sleep(random.randrange(2,5))
    print("\tAvión comercial No. " + str(ref) + " desembarcó todos sus tripulantes.")

def cargaPAX(ref:int):
    global andenPasajeros
    sleep(random.randrange(2,5))
    andenPasajeros.release()
    print("\tAvión comercial No. " + str(ref) + " tripulado, solicita permiso para despegar.")

def avionCarguero(ref:int):
    global pistaDeAviacion
    start = time()
    print("\tAquí avión carguero No. " + str(ref) + ", solicita permiso para aterrizar.")
    comunicacion(ref)
    pistaDeAviacion.acquire()
    print("\tAvión carguero No. " + str(ref) + " en tierra.")
    descargaMERCH(ref)
    cargaMERCH(ref)
    #Avión en zona de espera terrestre
    comunicacion(ref)
    pistaDeAviacion.acquire()
    finish = time() - start
    print(">>Avión carguero No. " + str(ref) + " en aire, {0:.1f} horas en aeropuerto.<<".format(finish))

def descargaMERCH(ref:int):
    global pistaDeAviacion, andenMercancia
    andenMercancia.acquire()
    sleep(random.randrange(4,7))
    print("\tCargamento de avión carguero No. " + str(ref) + " entregado.")

def cargaMERCH(ref:int):
    global andenMercancia
    sleep(random.randrange(4,7))
    andenMercancia.release()
    print("\tAvion carguero No. " + str(ref) + " cargado, solicita permiso para despegar.")

def comunicacion(ref:int):
    global mutexRadioAvion, mutexRadioTorreDeControl, mensaje
    mutexRadioAvion.acquire()
    mensaje = ref
    mutexRadioTorreDeControl.release()

def torreDeControl():
    global pistaDeAviacion, mutexRadioTorreDeControl,mutexRadioAvion, mensaje
    print("**🗼Aquí torre de control, iniciamos operaciones.**")
    while True:
        mutexRadioTorreDeControl.acquire()
        print("** 🗼 Aquí torre de control, avion No. {} puede ocupar la pista**".format(mensaje))
        pistaDeAviacion.release()
        mutexRadioAvion.release()
        

def traficoAereo():
    ref = 1
    while True:
        opcion = random.randint(0, 1)
        if opcion == 0 :
            Thread(target = avionComercial, args= [ref]).start()
            ref += 1
            sleep(random.randrange(1,3))
        else:
            Thread(target = avionCarguero, args = [ref]).start()
            ref +=1
            sleep(random.randrange(2,5))

def main():
    Thread( target = torreDeControl, args=[]).start()
    traficoAereo()

main()