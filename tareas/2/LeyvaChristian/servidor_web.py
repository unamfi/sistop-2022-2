# Imports   --------------
import threading
import time
import random

# Variables globales    -----------------
n_trabajadores = 3
hilos_conexiones = 5
p_conexion = .4
semaforo_trabajadores = threading.Semaphore(0)
mutex_conexion = threading.Semaphore(1)
nombre_paginas = ['Google', 'Facebook', 'YouTube','Github','Wikipedia']
fila_solicitudes = []
nueva_solicitud = threading.Semaphore(0)

# Comienza la diversion --------------

# Funcion que genera las solicitudes de paginas, va a haber un thread por cada nombre de pagina
def Pagina(nombre):
    global fila_solicitudes
    while True:
        time.sleep(3 * random.random())
        if random.random() < p_conexion:
            print('{}: Nueva solicitud.'.format(nombre))
            with mutex_conexion:
                fila_solicitudes.append(nombre)
                nueva_solicitud.release()

# Jefe -> Listener que reparte trabajo a los trabajadores
def Jefe():
    while True:
        print("Jefe: Esperando solicitudes...")
        nueva_solicitud.acquire()
        print("Jefe: Atendiendo solicitud...")
        semaforo_trabajadores.release()

# Hilo que espera a que su jefe lo despierte para atender solicitudes
# Nota: Se incluyo un tiempo de tardanza del trabajador para evitar 
# que termine un hilo muy rapido y atienda mas solicitudes que los demas
def Trabajador(id:int):
    global fila_solicitudes
    while True:
        print('T%d: No hay trabajo, a mimir. zzz...'%id)
        semaforo_trabajadores.acquire()
        print('T%d: Aghh mas trabajo...'%id)
        # El trabajador se tarda en realizar la conexion...
        time.sleep(2*random.random())
        with mutex_conexion:
            pagina = fila_solicitudes.pop(0)
        print('T{}: Pagina {} cargada correctamente '.format(id,pagina))

def main():
    threading.Thread(target=Jefe).start()
    for i in nombre_paginas:
        threading.Thread(target=Pagina,args=[i]).start()
    for i in range(n_trabajadores):
        threading.Thread(target=Trabajador, args=[i]).start()

main()