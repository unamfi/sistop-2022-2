import sys

#Obtenemos el archivo con el contenido de la memoria a partir de /proc/$pid/maps
def lectura_archivo(pid):
    try:
        direccionArch = '/proc/'+pid+'/maps'
        archivo = open(direccionArch, 'r')

        return archivo.readlines()

    except:
        print("Algo salio mal!")
        print("Error: ", sys.exc_info()[0])

        return "ERROR"
        
#Proceso principal del programa (permite realizar varias consultas)
while(1):
    pid = input("Ingresa el PID ('s' para salir): ")
    #Salida del programa
    if pid == "s":
        print("Hasta la proxima!")
        break

    contenido = lectura_archivo(pid)

    if contenido != "ERROR":
        for linea in contenido:
            print(linea)



