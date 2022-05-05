import sys

#Obtenemos el archivo con el contenido de la memoria a partir de /proc/$pid/maps
def lectura_archivo(pid):
    try:
        direccionArch = '/proc/'+pid+'/maps'
        archivo = open(direccionArch, 'r')

        return archivo.readlines()

    except:
        print("Algo salio mal!")
        print("\nError: ", sys.exc_info()[0])

        return "ERROR"

#def obtener_datos(pid)

#Proceso principal del programa (permite realizar varias consultas)
while(1):
    pid = input("\nIngresa el PID ('s' para salir): ")
    
    #Salida del programa
    if pid.lower() == "s":
        print("\nHasta la proxima!")
        break

    #Asignamos a una variable el contenido obtenido del archivo
    contenido = lectura_archivo(pid)

    #Verificamos si la lectura del archivo nos dio error para comenzar de nuevo,
    #de no ser así procedemos con el programa
    if contenido != "ERROR":


        print("║"+'Uso'.center(18),end='')
        print("║"+'Inicio-Fin'.center((13*2)+1),end='')
        print("║"+'Tamaño'.center(12),end='')
        print("║"+'Num. págs.'.center(10),end='')
        print("║"+'Perm.'.center(5),end='')
        print("║"+' Uso/Mapeo')

        for linea in contenido:
            print(linea)
            #Separamos los datos de cada linea en una lista
            #Esta separación se hara por espacios en blanco
            datosSeparados = linea.split()
