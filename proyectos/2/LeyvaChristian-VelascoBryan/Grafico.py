
#Aeropuerto Felipe Ángeles#
from threading import Semaphore, Thread
from time import sleep, time
import random
from tkinter import *

pistaDeAviacion = Semaphore(0)
mutexRadioAvion = Semaphore(1)
mensaje = 0
mutexRadioTorreDeControl = Semaphore(0)
andenPasajeros = None
andenMercancia = None
mutexEscritura = Semaphore(1)

# A partir de aquí esta medio revuelto el codigo debido a la creacion de la GUI con Tkinter,
# si el tiempo da abasto se pondra bonito, si no disculpe las molestias ⚠️😅

root_window = Tk()
root_window.geometry("1000x600")
# root_window.configure(bg = "")
backgroundImage = PhotoImage(file = "assets/background.png")
# Se crea el background:
canvas = Canvas( root_window,bg="#0d0d0d",width=1000,height=600,relief = "ridge",bd=0)
canvas.place(x=0,y=0)
canvas.create_image( 0, 0, image = backgroundImage, anchor = "nw")

# Se crea el frame donde se colocara la salida de la torre
ConsolaTorre=Frame()
ConsolaTorre.config(bg = "white")
ConsolaTorre.config(width = "185", height = "325")
ConsolaTorre.place(x=354,y=252)
# Se crea el frame donde se colocara la salida del avion comercial
ConsolaComercial=Frame()
ConsolaComercial.config(bg = "white")
ConsolaComercial.config(width = "185", height = "325")
ConsolaComercial.place(x=570,y=252)
# Se crea el frame donde se colocara la salida de la torre
ConsolaCarguero=Frame()
ConsolaCarguero.config(bg = "white")
ConsolaCarguero.config(width = "185", height = "325")
ConsolaCarguero.place(x=786,y=252)
# Input tiempo de espera entre aviones comerciales
entryTComercial = Entry(root_window)
entryTComercial.place(x=775, y=75)
# Input tiempo de espera entre aviones cargeros
entryCargero = Entry(root_window)
entryCargero.place(x=775, y=125)

textoTorre = Text(ConsolaTorre, width = 22, height = 20)
textoTorre.grid(row = 1, column = 0, padx = 2, pady = 2)
textoComercial = Text(ConsolaComercial, width = 22, height = 20)
textoComercial.grid(row = 1, column = 0, padx = 2, pady = 2)
textoCarguero = Text(ConsolaCarguero, width = 22, height = 20)
textoCarguero.grid(row = 1, column = 0, padx = 2, pady = 2)

#Scroll bars para desplazarse entre los mensajes
scrollTorre = Scrollbar(ConsolaTorre, command = textoTorre.yview)
scrollTorre.grid(row = 1,column = 1, sticky = "nsew")
textoTorre.config(yscrollcommand = scrollTorre.set)

scrollComercial = Scrollbar(ConsolaComercial, command = textoComercial.yview)
scrollComercial.grid(row = 1,column = 1, sticky = "nsew")
textoComercial.config(yscrollcommand = scrollComercial.set)

scrollCarguero = Scrollbar(ConsolaCarguero, command = textoCarguero.yview)
scrollCarguero.grid(row = 1,column = 1, sticky = "nsew")
textoCarguero.config(yscrollcommand = scrollCarguero.set)

def only_numbers(char):
    return char.isdigit()

def avionComercial(ref:int):
    global pistaDeAviacion
    start = time()
    with mutexEscritura:
        textoComercial.insert(INSERT,"🛩️ Aquí avión comercial No. " + str(ref) + ", solicita permiso para aterrizar.")
    comunicacion(ref)
    pistaDeAviacion.acquire()
    with mutexEscritura:
        textoComercial.insert(INSERT,"Avión " + str(ref) + " en tierra.")
    descargaPAX(ref)
    cargaPAX(ref)
    #Avión en zona de espera terrestre
    comunicacion(ref)
    pistaDeAviacion.acquire()
    finish = time() - start
    with mutexEscritura:
        textoComercial.insert(INSERT,">>Avión comercial No. " + str(ref) + " en aire, {0:.1f} horas en aeropuerto.<<".format(finish))

def descargaPAX(ref:int):
    global pistaDeAviacion,andenPasajeros
    andenPasajeros.acquire()
    sleep(random.randrange(2,5))
    with mutexEscritura:
        textoComercial.insert(INSERT,"Avión comercial No. " + str(ref) + " desembarcó todos sus tripulantes.")

def cargaPAX(ref:int):
    global andenPasajeros
    sleep(random.randrange(2,5))
    andenPasajeros.release()
    with mutexEscritura:
        textoComercial.insert(INSERT,"Avión comercial No. " + str(ref) + " tripulado, solicita permiso para despegar.")

def avionCarguero(ref:int):
    global pistaDeAviacion
    start = time()
    with mutexEscritura:
        textoCarguero.insert(INSERT,"Aquí avión carguero No. " + str(ref) + ", solicita permiso para aterrizar.")
    comunicacion(ref)
    pistaDeAviacion.acquire()
    with mutexEscritura:
        textoCarguero.insert(INSERT,"Avión carguero No. " + str(ref) + " en tierra.")
    descargaMERCH(ref)
    cargaMERCH(ref)
    #Avión en zona de espera terrestre
    comunicacion(ref)
    pistaDeAviacion.acquire()
    finish = time() - start
    with mutexEscritura:
        textoCarguero.insert(INSERT,">>Avión carguero No. " + str(ref) + " en aire, {0:.1f} horas en aeropuerto.<<".format(finish))

def descargaMERCH(ref:int):
    global pistaDeAviacion, andenMercancia
    andenMercancia.acquire()
    sleep(random.randrange(4,7))
    with mutexEscritura:
        textoCarguero.insert(INSERT,"Cargamento de avión carguero No. " + str(ref) + " entregado")

def cargaMERCH(ref:int):
    global andenMercancia
    sleep(random.randrange(4,7))
    andenMercancia.release()
    with mutexEscritura:
        textoCarguero.insert(INSERT,"Avion carguero No. " + str(ref) + " cargado, solicita permiso para despegar.")

def comunicacion(ref:int):
    global mutexRadioAvion, mutexRadioTorreDeControl, mensaje
    mutexRadioAvion.acquire()
    mensaje = ref
    mutexRadioTorreDeControl.release()

def torreDeControl():
    global pistaDeAviacion, mutexRadioTorreDeControl,mutexRadioAvion, mensaje
    with mutexEscritura:
        textoTorre.insert(INSERT,"**🗼Aquí torre de control, iniciamos operaciones.**")
    while True:
        mutexRadioTorreDeControl.acquire()
        with mutexEscritura:
            textoTorre.insert(INSERT,"** 🗼 Aquí torre de control, avion No. {} puede ocupar la pista**".format(mensaje))
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

def Inicio():

    global andenPasajeros
    global andenMercancia
    tiempoComercial = entryTComercial.get()
    tiempoCarguero = entryCargero.get()

    # Se verifica que los valores ingresados sean NUMEROS
    if only_numbers(tiempoComercial) and only_numbers(tiempoCarguero):
        if int(tiempoComercial) > 0 and int(tiempoCarguero) > 0:
            Thread( target = torreDeControl, args=[]).start()
            andenPasajeros = Semaphore(int(tiempoComercial))
            andenMercancia = Semaphore(int(tiempoCarguero))
            traficoAereo()

# Boton para iniciar programa
botonInicio = Button(text="Iniciar",command=Inicio)
botonInicio.place(x=850,y=160)

root_window.resizable(False, False)
root_window.mainloop()
