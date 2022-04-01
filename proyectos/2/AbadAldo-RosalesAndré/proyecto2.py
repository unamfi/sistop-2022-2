# Proyecto 2: 

import threading
import time
import random

bandera = True
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


print("### Proyecto 2: Una situación cotidiana parelizable ###")
print("\n Bienvenido! Este programa modela el comportamiento en un comedor Japonés en dónde se considera de mala educación dejar a alguien solo en la mesa. Para más detalles favor de revisar la documentación adjunta. ")
menu = {'1':"Indicar el número de comensales", '2':"Salir"}

while bandera:
    
    print("\nPor favor, selecciona alguna de las siguientes opciones:\n")
    opciones = menu.keys()
    sorted(opciones)

    for opcion in opciones:
        print (opcion, ".- ", menu[opcion])

    seleccion = input("\nOpción elegida: ")

    if seleccion == '1':
        
        instancias =int(input("Dime, ¿Con cuántos comensales quieres que trabaje?: "))
        print("Entendido, comenzando...\n")
        for i in range(instancias):
            threading.Thread(target=comensal, args=[i]).start()
        
        time.sleep(instancias*.41)
        print("Trabajo terminado...\n")
    elif seleccion == '2':
        print("Gracias por ejecutarme!")
        bandera = False

    else:
        print("Opción incorrecta, intenta nuevamente")
