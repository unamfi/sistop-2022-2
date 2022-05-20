from os import system
import struct
archivos=[] # se inicia una lista en la que se guardarán los nombres de los archivos
print("Sistema de archivos de la FI\n")
ruta=input("Escriba la ruta en la que se encuentra la imagen del sistema de archivos: ")
com="hd "+ruta+" > contenido.txt"
print(com)
system(com)#System funciona para ejecutar comandos de la terminal
SA=open("contenido.txt","r")
lineas=SA.readlines()
for i in range(6,518,4):#El rango indica donde inician y dónde terminan los archivos
        archivos.append(lineas[i][-18:-3])#Se agrega a la lista los nombres de los archivos, los indices nos regresan solo el nombre
def ls(lineas):
    for i in range(6,518,4):
        print(lineas[i][-18:-3])
def mv2PC():
    try:
        imagen=open("fiunamfs.img","r+b")
        arch=input("Escriba el nombre del archivo a copiar: ")
        if arch.rjust(15) in archivos:#Se comprueba la existencia del archivo
            archimg=imagen.read()
            if arch.encode() in archimg:
                nuevo = open(arch,"wb")
                index=archimg.index(arch.encode())
                data=archimg[index:index+57]#Se asigna la informacion del archivo a la variable
                nuevo.write(data)
                nuevo.close()
        else:
            print("Archivo no encontrado")
    except:
        print("Compruebe que la imagen del sistema se encuentre en el mismo directorio que este programa")

while True:
    opc=int(input("Seleccione el número de la opcion deseada:\n\t1.-ls: listar los archivos del sistema\n\t2.-mv2PC: copiar un archivo de fiunamfs a su PC\n\t3.-Salir\n"))
    if(opc==1):
        ls(lineas)
    elif(opc==2):
        mv2PC()
    elif(opc==3):
        break
    else:
        print("Opción no válida")
    SA.close()
