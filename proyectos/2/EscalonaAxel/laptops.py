# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 02:39:22 2022

@author: axel_
"""

from threading import Semaphore, Thread, Lock

LaptopsTerminadas=0

#cont de componentes independientes

MotherBoard = 0  
RAM= 0
SeccionUsb = 0
UsbConector = 0
Procesadores = 0

#cont de uniones

MotherboardRam = 0  
SeccionUSB_Conector = 0
LaptopsSinCPU = 0
LaptopsTerminadas = 0

#total componentes ind.

suma_MotherBoard = 0  
suma_RAM = 0
suma_SeccionUsb= 0
suma_UsbConector= 0
suma_Procesadores = 0

#total uniones

suma_MotherboardRam = 0  
suma_SeccionUSB_Conector = 0
suma_LaptopsSinCPU = 0
suma_LaptopsTerminadas = 0

#mutex componetnes ind.

mutex_MotherBoard = Semaphore(1) 
mutex_RAM = Semaphore(1)
mutex_SeccionUsb = Semaphore(1)
mutex_UsbConector = Semaphore(1)
mutex_Procesadores = Semaphore(1)

#mutex para las uniones

mutex_MotherboardRam = Semaphore(1) 
mutex_SeccionUSB_Conector = Semaphore(1)
mutex_LaptopsSinCPU = Semaphore(1)
mutex_LaptopsTerminadas = Semaphore(1)

#barreras componentes independeientes

existe_MotherBoard = Semaphore(0)  
existe_RAM = Semaphore(0)
existe_SeccionUsb = Semaphore(0)
existe_UsbConector = Semaphore(0)
existe_Procesador = Semaphore(0)

#barreras de unioes

existe_MotherboardRam = Semaphore(0)  
existe_SeccionUSB_Conector = Semaphore(0)
existe_LaptopsSinCPU = Semaphore(0)

#barrera de finalizacion

mutex_terminado = Semaphore(0) 

#mutex para imprimir

mutex_imprimir = Semaphore(1) 



print("\n\n <<<<<<<<<<<<<<<<<<<<< Fabricación de Laptops >>>>>>>>>>>>>>>>>>>>>>>>\n\n")

LaptopsTerminadas = int(input("\n Ingresa el número de laptops para fabricar:\n"))

def Fabricar_MotherBoard(): 
    global mutex_MotherBoard, MotherBoard, suma_MotherBoard, mutex_imprimir, existe_MotherBoard

    mutex_MotherBoard.acquire()  #bloqueo de variables de contadores y suma

    MotherBoard = MotherBoard + 1
    suma_MotherBoard = suma_MotherBoard + 1

    mutex_imprimir.acquire()
    print("\nSe fabricó la Tarjeta Madre #:",suma_MotherBoard) 
    mutex_imprimir.release()

    mutex_MotherBoard.release()
    
    #señalización de que hay motherboard disponible

    existe_MotherBoard.release()  


def Fabricar_RAM():
    global mutex_RAM, RAM, suma_RAM, existe_RAM, mutex_imprimir

    mutex_RAM.acquire()

    RAM = RAM + 1
    suma_RAM = suma_RAM + 1

    mutex_imprimir.acquire()
    print("\nSe fabricó la RAM #:",suma_RAM)
    mutex_imprimir.release()
    
    #torniquete
    if(RAM > 1):
        
        existe_RAM.release()  

    mutex_RAM.release()


def Fabricar_SeccionUsb():
    global mutex_SeccionUsb, SeccionUsb, suma_SeccionUsb, existe_SeccionUsb, mutex_imprimir

    mutex_SeccionUsb.acquire()

    SeccionUsb = SeccionUsb + 1
    suma_SeccionUsb = suma_SeccionUsb + 1

    mutex_imprimir.acquire()
    print("\n Se Fabricó la seccion USB #:",suma_SeccionUsb)
    mutex_imprimir.release()

    if(SeccionUsb > 2):
        existe_SeccionUsb.release()

    mutex_SeccionUsb.release()


def Fabricar_UsbConector():
    global mutex_UsbConector, UsbConector, suma_UsbConector, mutex_imprimir, existe_UsbConector

    mutex_UsbConector.acquire()

    UsbConector = UsbConector + 1
    suma_UsbConector = suma_UsbConector + 1

    mutex_imprimir.acquire()
    print("\nSe fabrico el conector usb c #: ",suma_UsbConector)
    mutex_imprimir.release()

    if(UsbConector > 2):
        existe_UsbConector.release()

    mutex_UsbConector.release()


def Fabricar_Procesador():
    global mutex_Procesadores, Procesadores, suma_Procesadores, mutex_imprimir, existe_Procesador

    mutex_Procesadores.acquire()

    Procesadores = Procesadores + 1
    suma_Procesadores = suma_Procesadores + 1

    mutex_imprimir.acquire()
    print("\n Se fabricó el procesador #: ",suma_Procesadores)
    mutex_imprimir.release()

    mutex_Procesadores.release()

    existe_Procesador.release()


def Unir_TarjetaMadre_RAMS():
    global existe_MotherBoard, existe_RAM, MotherBoard, RAM, suma_MotherboardRam, mutex_MotherboardRam, mutex_MotherBoard, mutex_RAM, MotherboardRam, mutex_imprimir, existe_MotherboardRam

    existe_MotherBoard.acquire()
    #se debe esperar a que los elementos independientes esten ready.
    existe_RAM.acquire()   
    
    #se protege este componente armado
    mutex_MotherboardRam.acquire()   

    suma_MotherboardRam = suma_MotherboardRam + 1

    mutex_MotherBoard.acquire()
    mutex_RAM.acquire()

    mutex_imprimir.acquire()
    print("\n Hay",MotherBoard,"tarjetas madre y",RAM,"memorias ram.")   
    print("\n Se ensamblo 1 tarjeta madre con 2 memorias ram. Se ensamblo la tarjeta madre con memoria #:",suma_MotherboardRam)
    mutex_imprimir.release()

    MotherBoard = MotherBoard - 1
    #se restan 
    RAM = RAM - 2   #se decrementan los valores de los elementos independientes no sin antes haberlos protegido
    
    #se aumenta la cuenta del componente armado
    MotherboardRam = MotherboardRam + 1   

    mutex_RAM.release()
    mutex_MotherBoard.release()

    existe_MotherboardRam.release()

    mutex_MotherboardRam.release()


def Soldar_ConectorUSB():
    global existe_SeccionUsb, existe_UsbConector, SeccionUsb, UsbConector, suma_SeccionUSB_Conector, mutex_SeccionUSB_Conector, mutex_SeccionUsb, mutex_UsbConector, SeccionUSB_Conector, mutex_imprimir, existe_SeccionUSB_Conector

    existe_SeccionUsb.acquire()
    existe_UsbConector.acquire()

    mutex_SeccionUSB_Conector.acquire()

    suma_SeccionUSB_Conector = suma_SeccionUSB_Conector + 1

    mutex_SeccionUsb.acquire()
    mutex_UsbConector.acquire()


    mutex_imprimir.acquire()
    
    print("\nHay",SeccionUsb,"secciones para soldar y",UsbConector,"conectores.")
    
    print("\nSe ensamblaron 3 secciones para soldar con 3 conectores. grupos conector usbC #: ",suma_SeccionUSB_Conector)
    mutex_imprimir.release()

    SeccionUsb = SeccionUsb - 3
    
    UsbConector = UsbConector - 3

    SeccionUSB_Conector = SeccionUSB_Conector + 1

    mutex_UsbConector.release()
    
    mutex_SeccionUsb.release()

    existe_SeccionUSB_Conector.release()

    mutex_SeccionUSB_Conector.release()


def ensamble_MotherboardRam_SeccionUSB_Conector():
    global existe_MotherboardRam, existe_SeccionUSB_Conector, LaptopsSinCPU, suma_LaptopsSinCPU, MotherboardRam, SeccionUSB_Conector, mutex_LaptopsSinCPU, mutex_MotherboardRam, mutex_SeccionUSB_Conector, mutex_imprimir, existe_LaptopsSinCPU

    existe_MotherboardRam.acquire()
    existe_SeccionUSB_Conector.acquire()

    mutex_LaptopsSinCPU.acquire()

    suma_LaptopsSinCPU = suma_LaptopsSinCPU + 1

    mutex_MotherboardRam.acquire()
    mutex_SeccionUSB_Conector.acquire()

    mutex_imprimir.acquire()
    print("\nHay",MotherboardRam,"tarjetas madre con ram y",SeccionUSB_Conector,"secciones usb con conector")
    print("\nSe ensamblo 1 tarjeta madre con ram con 1 seccion usb con conector. Se armó la laptop sin procesador",suma_LaptopsSinCPU)
    mutex_imprimir.release()

    MotherboardRam = MotherboardRam - 1
    SeccionUSB_Conector = SeccionUSB_Conector - 1

    mutex_SeccionUSB_Conector.release()
    mutex_MotherboardRam.release()

    existe_LaptopsSinCPU.release()

    mutex_LaptopsSinCPU.release()


def Montar_Procesador():
    global existe_LaptopsSinCPU, existe_, Procesadores, suma_LaptopsTerminadas, mutex_LaptopsTerminadas, mutex_terminado, LaptopsTerminadas, mutex_imprimir

    existe_LaptopsSinCPU.acquire()
    existe_Procesador.acquire()

    mutex_LaptopsTerminadas.acquire()


    suma_LaptopsTerminadas = suma_LaptopsTerminadas + 1  #laptops listas

    mutex_imprimir.acquire()
    print("\n se le montó procesador a la laptop",suma_LaptopsTerminadas,"y esta terminada.")
    mutex_imprimir.release()

    if(suma_LaptopsTerminadas > LaptopsTerminadas - 1):
        
        mutex_terminado.release()#torniquete

    mutex_LaptopsTerminadas.release()
    






#Para observar el funcionamiento 
for i in range(LaptopsTerminadas*4):    
    if (i%4==0):
                        
        thread_Fabricar_MotherBoard = Thread(target=Fabricar_MotherBoard,args=[])
        thread_Fabricar_MotherBoard.start()

        thread_Unir_TarjetaMadre_RAMS = Thread(target=Unir_TarjetaMadre_RAMS,args=[])
        thread_Unir_TarjetaMadre_RAMS.start()

        thread_Soldar_ConectorUSB = Thread(target=Soldar_ConectorUSB,args=[])
        thread_Soldar_ConectorUSB.start()

        thread_procesador = Thread(target=Fabricar_Procesador,args=[])
        thread_procesador.start()

        thread_ensamble_MotherboardRam_SeccionUSB_Conector = Thread(target=ensamble_MotherboardRam_SeccionUSB_Conector,args=[])
        thread_ensamble_MotherboardRam_SeccionUSB_Conector.start()

        tarea_Montar_Procesador = Thread(target=Montar_Procesador,args=[])
        tarea_Montar_Procesador.start()

    if (i%2==0):
        t4 = Thread(target=Fabricar_RAM,args=[])
        t4.start()

    t5 = Thread(target=Fabricar_SeccionUsb,args=[])
    t5.start()

    t6 = Thread(target=Fabricar_UsbConector,args=[])
    t6.start()

#espera la señalizacion de completado
mutex_terminado.acquire()
   
mutex_imprimir.acquire()

print("\n\n Todas las laptops estan listas")

mutex_imprimir.release()