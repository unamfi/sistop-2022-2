from threading import Semaphore, Thread
from time import sleep
import random

###--El servidor web--###

#Lista donde se almacenarán los trabajadores
trabajadores = []

conexion = Semaphore(0)
#Se empieza con 8 trabajadores
disponibles = noTrabajadores = 8
mutexDisponibles = Semaphore(1)

def jefe():
    global conexion, mutexDisponibles, disponibles, noTrabajadores
    #La carga de trabajo para este instante es K
    disponibles = k = random.randrange(3,noTrabajadores)
    print("El día de hoy la carga laboral está en promedio con " + str(k) + " conexiones")
    #El jefe lanza a k trabajadores a estar al pendiente de de la carga de trabajo (cualquier conexion)
    for i in range(0,k):#Se suma uno debido a que range no incluye k
        trabajadores[i].start()
    print("Se tienen ya a " + str(disponibles) + " trabajadores al pendiente")
    print("***ENCIENDAN EL SERVER!***")
    
    while True:
        recibirConexiones(k)
        mutexDisponibles.acquire()
        if disponibles <= 0 and k != noTrabajadores:
            print(">>HABLA EL JEFE, despierten al compañero " + str(k) + "!")
            trabajadores[k].start()
            k += 1
        elif disponibles <= 0 and k == noTrabajadores:
            contrataciones = disponibles * -1
            print(">>HABLA EL JEFE, tenemos exceso de conexiones, contratemos " + str(contrataciones) + " trabajadores!")
            for i in range(0,contrataciones):
                trabajadores.append(Thread(target = trabajador, args=[k+i+1]))
                noTrabajadores += 1
        mutexDisponibles.release()
        
def trabajador(idTrabajador:int):
    global conexion, mutexDisponibles, disponibles
    print("***Trabajador "+ str(idTrabajador) + " reportandose!***")
    while True:
        conexion.acquire()
        print("\t\tTrabajador " + str(idTrabajador) + ", te habla el jefe")
        atenderConexion()
        print("\t**Conexión atendida por el trabajador " + str(idTrabajador) + "\n\t\tEl trabajador " + str(idTrabajador) + " procede a dormir")
        mutexDisponibles.acquire()
        disponibles += 1
        mutexDisponibles.release()

def atenderConexion():
    sleep(random.randrange(2,6))

def recibirConexiones(k:int):
    global disponibles,conexion, mutexDisponibles
    sleep(random.randrange(2,5))
    numConexiones = random.randint(1, k//2)
    mutexDisponibles.acquire()
    print(">>HABLA EL JEFE, llegaron " + str(numConexiones) + " conexiones nuevas!\nSe tienen " + str(disponibles) + " trabajadores disponibles")
    mutexDisponibles.release()
    for i in range(0,numConexiones):
        mutexDisponibles.acquire()
        conexion.release()
        disponibles -= 1
        mutexDisponibles.release()

for i in range(0,noTrabajadores):    
    trabajadores.append(Thread(target = trabajador, args=[i+1]))

jefe()

    
    