from os import system
import struct
archivos=[]
print("Sistema de archivos de la FI\n")
ruta=input("Escriba la ruta en la que se encuentra la imagen del sistema de archivos: ")
#system("hd"+ruta+"> contenido.txt")
SA=open("pruebas proy4.txt","r")
lineas=SA.readlines()
for i in range(6,22,4):
        archivos.append(lineas[i][-18:-3])
def ls(lineas):
    for i in range(6,22,4):
        print(lineas[i][-18:-3])
def mv2PC():
    try:
        imagen=open("fiunamfs.img","r+b")
        arch=input("Escriba el nombre del archivo a copiar: ")
        if arch.rjust(15) in archivos:
            archimg=imagen.read()
            if arch.encode() in archimg:
                nuevo = open(arch,"wb")
                index=archimg.index(arch.encode())
                data=archimg[index:index+57]
                nuevo.write(data)
                nuevo.close()
        else:
            print("Archivo no encontrado")
    except:
        print("Compruebe que la imagen del sistema se encuentre en el mismo directorio que este programa")

opc=int(input("Seleccione el número de la opcion deseada:\n\t1.-ls: listar los archivos del sistema\n\t2.-mv2PC: copiar un archivo de fiunamfs a su PC\n"))
if(opc==1):
    ls(lineas)
elif(opc==2):
    mv2PC()
SA.close()

