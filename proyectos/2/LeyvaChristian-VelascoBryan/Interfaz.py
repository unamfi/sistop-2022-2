from tkinter import *


def btn_clicked():
    print("Button Clicked")

def createGUI():
    root_window = Tk()

    root_window.geometry("1000x600")
    # root_window.configure(bg = "")
    backgroundImage = PhotoImage(file = "assets/background.png")
    # backg = PhotoImage(file = "assets/BackgroundPrue.png",width=1000,height=600)
    # Se muestra el bg con un label
    # label1 = Label( root_window, image = backgroundImage,bg="#0d0d0d")
    # label1.place(x = 0, y = 0)

    # Con canvas:
    canvas = Canvas( root_window,bg="#0d0d0d",width=1000,height=600,relief = "ridge",bd=0)
    canvas.place(x=0,y=0)
    canvas.create_image( 0, 0, image = backgroundImage, anchor = "nw")

    entryTComercial = Entry(root_window)
    entryTComercial.place(x=775, y=75)
    entryCargero = Entry(root_window)
    entryCargero.place(x=775, y=125)

    botonInicio = Button(text="Iniciar")
    botonInicio.place(x=850,y=160)

    root_window.resizable(False, False)
    root_window.mainloop()

createGUI()