import sys

#Diccionario de cada uso de memoria con su respectivo color.
color_uso = {
    "Heap":"\033[32mHeap\033[m",
    "Stack":"\033[31mStack\033[m",
    "Datos":"\033[34mDatos\033[m",
    "Texto":"\033[35mTexto\033[m",
    "BibD":"\033[36mBib Datos\033[m",
    "BibT":"\033[37mBib Texto\033[m",
    "Vacio":"Vacio",
    "Mapeo Anon.":"\033[33mMapeo Anon.\033[m",
    "Sys. Calls":"\033[33mSys. Calls\033[m",
    "Kernel Vars.":"\033[33mKernel Vars.\033[m",
    "Reserva":"\033[33mReserva\033[m"
}

#Variable global que nos permite saber si hemos pasado por el heap
paso_heap = False

#Variables que define el espacio de los bloques que se muestran en pantalla
espacio_uso = 18
espacio_memoria_64 = 27
espacio_memoria_32 = 13
espacio_tamanio = 12
espacio_numpags = 15
espacio_permisos = 5
espacio_usomapeo = 11


#Funcion que comprueba si la memoria es de 32 o 64 bits
def comprobar_tamanio(memoria):
    if (len(memoria) >= 24):
        return True
    else:
        return False


#Función que permite dar un formato a cosas generales de la salida
def mostrar_encabezado(es_64):
    if(es_64):
        espacio_memoria = espacio_memoria_64
    else:
        espacio_memoria = espacio_memoria_32

    print("╔"+'═'*espacio_uso+"╦",end='')
    print('═'*(espacio_memoria) + "╦",end='')
    print('═'*(espacio_tamanio) + "╦",end='')
    print('═'*(espacio_numpags) + "╦",end='')
    print('═'*(espacio_permisos) + "╦",end='')
    print('═'*(espacio_usomapeo) + "╗")
    print("║"+'Uso'.center(espacio_uso),end='')
    print("║"+'Inicio-Fin'.center(espacio_memoria),end='')
    print("║"+'Tamaño'.center(espacio_tamanio),end='')
    print("║"+'Num. págs.'.center(espacio_numpags),end='')
    print("║"+'Perm.'.center(espacio_permisos),end='')
    print("║"+'Uso/Mapeo'.center(espacio_usomapeo) + "║")
    print("╠"+'═'*espacio_uso+"╬",end='')
    print('═'*(espacio_memoria) + "╬",end='')
    print('═'*(espacio_tamanio) + "╬",end='')
    print('═'*(espacio_numpags) + "╬",end='')
    print('═'*(espacio_permisos) + "╬",end='')
    print('═'*(espacio_usomapeo) + "╣")
    #Notar que las multiplicaciones ayudan a concatenar más facilmente la cantidad
    #de signos iguales que se usan para el formato


#Función para mostrar el pie o final de la tabla de memoria
def mostrar_pie(es_64):
    #Verificamos si la memoria es de 64 o 32 bits y asignamos el valor correspondiente
    #al espacio que ocupara en pantalla dicho atributo
    if(es_64):
        espacio_memoria = espacio_memoria_64
    else:
        espacio_memoria = espacio_memoria_32

    print("╚"+'═'*espacio_uso+"╩",end='')
    print('═'*(espacio_memoria) + "╩",end='')
    print('═'*(espacio_tamanio) + "╩",end='')
    print('═'*(espacio_numpags) + "╩",end='')
    print('═'*(espacio_permisos) + "╩",end='')
    print('═'*(espacio_usomapeo) + "╝")
    #Notar que las multiplicaciones ayudan a concatenar más facilmente la cantidad
    #de signos iguales que se usan para el formato



#Obtenemos el archivo con el contenido de la memoria a partir de /proc/$pid/maps
def lectura_archivo(pid):
    try:
        direccionArch = '/proc/'+pid+'/maps'
        archivo = open(direccionArch, 'r')

        return archivo.readlines()

    #Si no encontramos el archivo del proceso, entonces tendremos una excepcion
    #de tipo FileNotFoundError
    except FileNotFoundError:
        print("\n¡Algo salio mal!")
        print("\nError: El proceso no fue encontrado -", sys.exc_info()[0])
        print("Por favor, intentalo de nuevo")

        return "ERROR"

    #Si el sistema nos indica que no tenemos permisos para acceder al archivo del
    #proceso, entonces tendremos una excepcion PermissionError
    except PermissionError:
        print("\n¡Algo salio mal!")
        print("\nError: No cuenta con permisos suficientes -", sys.exc_info()[0])
        print("Por favor, intentelo de nuevo con un proceso al cual tenga permitido acceder")

        return "ERROR"

    #Notar que en el manejo de excepciones no finalizamos el programa, sino que
    #la manejamos para poder seguir la ejecución del programa    


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
    #Obtenemos los permisos para saber si el tipo de uso es de Reserva
    permisos = obtener_permisos(datosSeparados)

    #Obtenemos la ruta para analizar a que pertenece el uso de memoria
    ruta = obtener_ruta(datosSeparados)
    
    #Indicamos al interprete que en esta función tome la variable paso_heap
    #como una variable global
    global paso_heap

    if('/' in ruta):
        if('x' in permisos):
            uso = 'Texto'
        elif(not ('r' in permisos) and not('w' in permisos)):
            uso = 'Reserva'
        else:
            uso = 'Datos'
    elif(ruta == '[stack]'):
        uso = 'Stack'
    elif(ruta == '[heap]'):
        uso = 'Heap'
    elif(ruta == '[anon]'):
        uso = 'Mapeo Anon.'
    elif(ruta == '[vsyscall]'):
        uso = 'Sys. Calls'
    elif(ruta == '[vdso]'):
        uso = 'Sys. Calls'
    elif(ruta == '[vvar]'):
        uso = 'Kernel Vars.'
    elif(ruta == 'Vacio'):
        uso = '...'
    else:
        uso = ruta

    #Si explicitamente nos indica que es Heap encendemos la bandera
    if(uso == 'Heap'):
        paso_heap = True

    #Si tenemos un heap ímplicito entonces el uso de Texto y Datos va a cambiar
    if(paso_heap):
        if(uso == 'Texto'):
            uso = 'BibT'
        if(uso == 'Datos'):
            uso = 'BibD'

    return uso


#Funcion que permite obtener la direccion con el formato deseado
#eliminando los 0's innecesarios en la última dirección
def obtener_direccion(datosSeparados):
    #Obtenemos las partes que conforman a la memoria
    partes = datosSeparados[0].split('-')

    #Cada parte obtenida la asignamos a una variable para operar con ella
    primer_parte = partes[0]
    segunda_parte = partes[1]

    #Inicializamos el string de dirección para poder concatenarle caracteres
    #sin problemas de integridad
    direccion = ''

    #Verificamos si la dirección de memoria corresponde a 32 o 64 bits:

    #64 bits
    if (len(datosSeparados[0]) >= 25):
        for i in range(12):
            direccion += primer_parte[i]
        direccion += '-'
        for i in range(12):
            direccion += segunda_parte[i]
    #32 bits
    else:
        for i in range(5):
            direccion += primer_parte[i]
        direccion += '-'
        for i in range(5):
            direccion += segunda_parte[i]

    return direccion


#Función para obtener el numero de páginas
def obtener_pags(datosSeparados):
    #Obtenemos las partes que conforman a la memoria
    partes = datosSeparados[0].split('-')

    #Cada parte obtenida la asignamos a una variable para operar con ella
    primer_parte = partes[0]
    segunda_parte = partes[1]

    #Obtenemos el número de páginas con la sustracción de la segunda parte
    #de la memoria con la primera, esto con el casteo del string (que esta
    #en ---hexadecimal---) a un entero
    num_pag = int(segunda_parte,16) - int(primer_parte,16)

    return num_pag


#Función para obtener el tamaño de la memoria    
def obtener_tamanio(num_pag):
        #Obtenemos el tamaño a partir del numero de paginas
        tam = 4*num_pag

        #Definimos una lista que a partir de un contador, nos dará la
        #unidad de medida de la memoria
        unidades = ['KB','MB','GB','TB','PB','EB','ZB','YB','BB']

        #Inicializamos el contador para no tener problemas de integridad
        contUnidad = 0

        #Bucle que permite ir dividiendo el tamaño obtenido hasta llegar
        #a su maxima unidad con un contador
        while( (tam / 1024) >= 1 ):
            contUnidad += 1
            tam = tam/1024

        #Regresamos el valor obtenido del tamaño reducido junto a su unidad
        #en forma de string para su formateo posterior
        return str(round(tam,1)) + unidades[contUnidad]


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

        #Variable que nos permite obtener la direccion de memoria
        #para comprobar si es de 32 o 64 bits
        memoria_aux = contenido[0].split()

        #Variable booleana que nos indica si la memoria es de 32 o 64 bits
        es_64 = comprobar_tamanio(memoria_aux[0])

        #Se muestra el encabezado del programa, SOLAMENTE al leer correctamente 
        #la informacion de un proceso
        mostrar_encabezado(es_64)

        for linea in contenido:
            #Separamos los datos de cada linea en una lista
            #Esta separación se hara por espacios en blanco
            datosSeparados = linea.split()

            #Obtenemos los diferentes datos de la línea en iteración
            uso = obtener_uso(datosSeparados)
            direccion = obtener_direccion(datosSeparados)
            num_pag = obtener_pags(datosSeparados)
            tamTxt = obtener_tamanio(num_pag)
            
            #Realizamos la salida en pantalla de los datos
            print("║"+color_uso.get(uso,uso).center(26),end='')
            print("║"+direccion.center(26+1),end='')
            print("║"+tamTxt.center(12),end='')
            print("║"+str(num_pag).center(15))

        #Una vez mostrado el contenido de memoria formateamos el final de la tabla
        mostrar_pie(es_64)