from mimetypes import init
from tkinter import *


def createGUI():
    root_window = Tk()

    root_window.geometry("1000x600")
    # root_window.configure(bg = "")
    backgroundImage = PhotoImage(file = "assets/background.png")


    # Con canvas:
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
    ConsolaCargero=Frame()
    ConsolaCargero.config(bg = "white")
    ConsolaCargero.config(width = "185", height = "325")
    ConsolaCargero.place(x=786,y=252)
    # Input tiempo de espera entre aviones comerciales
    entryTComercial = Entry(root_window)
    entryTComercial.place(x=775, y=75)
    # Input tiempo de espera entre aviones cargeros
    entryCargero = Entry(root_window)
    entryCargero.place(x=775, y=125)
    # Boton para iniciar programa
    botonInicio = Button(text="Iniciar")
    botonInicio.place(x=850,y=160)

    root_window.resizable(False, False)
    root_window.mainloop()

def only_numbers(char):
    return char.isdigit()
