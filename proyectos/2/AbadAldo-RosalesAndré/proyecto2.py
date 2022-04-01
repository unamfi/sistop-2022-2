# Proyecto 2: Una situación cotidiana paralelizable 

# Bibliotecas
import threading
import time
import random

# Variables
bandera = True
comiendo = 0
haciendoSobremesa = 0

# Semáforos
listoParaIrse = threading.Semaphore(0)
mutex = threading.Semaphore(1)

# Función 'comensal': Modela el comportamiento que tendrá un comensal según cada situación de tal forma que cumpla con la regla de "no dejar a nadie comiendo solo".
def comensal(num):
   
    global comiendo, haciendoSobremesa
    
    # Primero buscamos llenar el plato y verificar si hay alguien a quien acompañar
    obtenerComida(num)
    mutex.acquire()
    comiendo+=1
    
    print("Comensal #%d verificando si se puede sentar..." % num)
    # Si hay dos comiendo (incluido el hilo en ejecución) y uno en espera de irse
    # entonces libera al que ya se quiere ir.
    if comiendo == 2 and haciendoSobremesa == 1:
        listoParaIrse.release()
        haciendoSobremesa -= 1
    mutex.release()
    
    # El comensal degusta sus alimentos
    comer(num)
   
    # El comensal termina sus alimentos y se pregunta que hacer
    mutex.acquire()
    
    # cambio de estado de comiendo a esperando para irse
    comiendo -= 1
    haciendoSobremesa += 1

    # Si hay alguien comiendo aún y queda solo este hilo en espera,
    # entonces debe aguantarse hasta que el otro comensal termine para retirarse
    # al mismo tiempo
    if comiendo == 1 and haciendoSobremesa == 1:
       
        print("Comensal #%d esperando a que otro comensal termine de comer..." % num)
        mutex.release()
        listoParaIrse.acquire()
    
    # Si estaban esperando a este hilo para retirse, notifica y se retiran ambos.
    elif comiendo == 0 and haciendoSobremesa == 2:
        print("Comensal #%d notificando que ha terminado al comensal que lo esté esperando..." % num)
        listoParaIrse.release()
        haciendoSobremesa -= 2
        mutex.release()
    
    # Si el comensal se sentó solo y nadie llegó a acompañarlo, mejor irse (caso especial)
    else:
        print("Comensal #%d se ha quedado solo... mejor irse" % num)
        haciendoSobremesa -= 1
        mutex.release()
    
    # El comensal se retira sin mayor complicación
    retirarse(num)

# ------------------

# ---  Funciones para simular acciones por parte de cada comensal
def obtenerComida(num):
    print("Comensal #%d consiguiendo comida..." % num)
    time.sleep(random.random() / 100)

def comer(num):
    print("Comensal #%d sentandose a comer..." % num)
    time.sleep(random.random() / 100)

def retirarse(num):
    print("Comensal #%d retirándose..." %num)
    time.sleep(random.random() / 100)

# ------------------

# --- Menú de usuario
# Nada muy especial, un menú extremadamente sencillo para habilitar la interacción
# por parte del usuario. No consideramos que fuese necesario hacerlo más "robusto".

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

# ------------------
