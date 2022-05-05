import sys

#Obtenemos el archivo con el contenido de la memoria de /proc/$pid/maps
pid = input("Ingresa el PID: ")

try:
    direccionArch = '/proc/'+pid+'/maps'
    archivo = open(direccionArch, 'r')

    contenido = archivo.readlines()

    for linea in contenido:
        print(linea)

except:
    print("Algo salio mal!")
    print("Error: ", sys.exc_info()[0])