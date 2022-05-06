import sys

#Diccionario de cada uso de memoria con su respectivo color.
color_uso = {
    "Heap":"\033[32mHeap\033[m",
    "Stack":"\033[31mStack\033[m",
    "Datos":"\033[34mDatos\033[m",
    "Texto":"\033[35mTexto\033[m",
    "Bib Datos":"\033[36mBib \033[34mDatos\033[m",
    "Bib Texto":"\033[36mBib \033[35mTexto\033[m",
    "Vacio":"Vacio",
    "Mapeo Anon.":"\033[33mMapeo Anon.\033[m",
    "Sys. Calls":"\033[33mSys. Calls\033[m",
    "Kernel Vars.":"\033[33mKernel Vars.\033[m",
    "Reserva":"\033[33mReserva\033[m"
}


#Función que permite dar un formato a cosas generales de la salida
def mostrar_encabezado():
    print("╔"+'═'*18+"╦",end='')
    print('═'*((13*2)+1) + "╦",end='')
    print('═'*(12) + "╦",end='')
    print('═'*(10) + "╦",end='')
    print('═'*(5) + "╦",end='')
    print('═'*(11) + "╗")
    print("║"+'Uso'.center(18),end='')
    print("║"+'Inicio-Fin'.center((13*2)+1),end='')
    print("║"+'Tamaño'.center(12),end='')
    print("║"+'Num. págs.'.center(10),end='')
    print("║"+'Perm.'.center(5),end='')
    print("║"+'Uso/Mapeo'.center(11) + "║")
    print("╠"+'═'*18+"╬",end='')
    print('═'*((13*2)+1) + "╬",end='')
    print('═'*(12) + "╬",end='')
    print('═'*(10) + "╬",end='')
    print('═'*(5) + "╬",end='')
    print('═'*(11) + "╣")
    #Notar que las multiplicaciones ayudan a concatenar más facilmente la cantidad
    #de signos iguales que se usan para el formato


#Función para mostrar el pie o final de la tabla de memoria
def mostrar_pie():
    print("╚"+'═'*18+"╩",end='')
    print('═'*((13*2)+1) + "╩",end='')
    print('═'*(12) + "╩",end='')
    print('═'*(10) + "╩",end='')
    print('═'*(5) + "╩",end='')
    print('═'*(11) + "╝")
    #Notar que las multiplicaciones ayudan a concatenar más facilmente la cantidad
    #de signos iguales que se usan para el formato



#Obtenemos el archivo con el contenido de la memoria a partir de /proc/$pid/maps
def lectura_archivo(pid):
    try:
        direccionArch = '/proc/'+pid+'/maps'
        archivo = open(direccionArch, 'r')

        return archivo.readlines()

    except FileNotFoundError:
        print("\n¡Algo salio mal!")
        print("\nError: El proceso no fue encontrado -", sys.exc_info()[0])
        print("Por favor, intentalo de nuevo")

        return "ERROR"

    except PermissionError:
        print("\n¡Algo salio mal!")
        print("\nError: No cuenta con permisos suficientes -", sys.exc_info()[0])
        print("Por favor, intentelo de nuevo con un proceso al cual tenga permitido acceder")

        return "ERROR"


#Función que permite obtener los permisos de cada linea leída
def obtener_permisos(datosSeparados):
    #Los permisos se encuentran en la primera posicion de la lista de
    #datos separados, y de ahí son los primeros cuatro caracteres
    #leídos
    return datosSeparados[1][0:3]


#Función que permite obtener la ruta de cada linea leída
def obtener_ruta(datosSeparados):
    #Si tenemos más de 5 elementos en la lista de los datos separados
    #entonces la ruta estara en la última posición (indice 5), si no 
    #es así, entonces la ruta sera [anon] ya que no estará definida
    if(len(datosSeparados) > 5):
        return datosSeparados[5]
    else:
        return '[anon]'


#Funcion que obtiene el uso de memoria
def obtener_uso(datosSeparados):
    permisos = obtener_permisos(datosSeparados)
    ruta = obtener_ruta(datosSeparados)

    if('/' in ruta):
        if('x' in permisos):
            return 'Texto'
        elif(not ('r' in permisos) and not('w' in permisos)):
            return 'Reserva'
        else:
            return 'Datos'
    elif(ruta == '[stack]'):
        return 'Stack'
    elif(ruta == '[heap]'):
        return 'Heap'
    elif(ruta == '[anon]'):
        return 'Mapeo Anon.'
    elif(ruta == '[vsyscall]'):
        return 'Sys. Calls'
    elif(ruta == '[vdso]'):
        return 'Sys. Calls'
    elif(ruta == '[vvar]'):
        return 'Kernel Vars.'
    elif(ruta == 'Vacio'):
        return '...'
    else:
        return ruta


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

        #Se muestra el encabezado del programa, SOLAMENTE al leer correctamente 
        #la informacion de un proceso
        mostrar_encabezado()

        for linea in contenido:
            #Separamos los datos de cada linea en una lista
            #Esta separación se hara por espacios en blanco
            datosSeparados = linea.split()
            uso = obtener_uso(datosSeparados)
            print("║"+color_uso.get(uso,uso).center(26))

        #Una vez mostrado el contenido de memoria formateamos el final de la tabla
        mostrar_pie()