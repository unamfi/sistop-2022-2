import os
import time
import math

#Se inicia la conexión (lectura de la imagen) con el sistema de archivos
try:
	sistema = open('fiunamfs.img','r+b')
#Si el archivo no se encuentra, se le indica al usuario
except FileNotFoundError:
	print("\n¡Algo salio mal!\n")
	print("Error: El sistema de archivos no fue encontrado.")
	print("-> Por favor, comprueba que el programa y el sistema de archivos"
		+ " se encuentran en el mismo directorio e intenta de nuevo.")
	print("-> Verifique que el sistema de archivos tenga por nombre 'fiunamfs.img'.")
	exit()
#Si el usuario no cuenta con permisos, se le indica
except PermissionError:
	print("\n¡Algo salio mal!\n")
	print("Error: No cuenta con los permisos necesarios para acceder al sistema de archivos.")
	exit()
	

#Clase SuperBloque que mantendrá seguros y globales los datos del primer cluster
class SuperBloque:
	def __init__(self,
				nombre,
				version,
				et_volumen,
				tam_cluster,
				num_clusters_dir,
				num_clusters_uni):

		self.nombre = nombre
		self.version = version
		self.et_volumen = et_volumen
		self.tam_cluster = tam_cluster #Tamaño en bytes
		self.num_clusters_dir = num_clusters_dir
		self.num_clusters_uni = num_clusters_uni


#Class Entrada que guardará las entradas del directorio para su fácil recuperacion
class Entrada:
	def __init__(self,
				nombre,
				tamanio,
				tamanio_pref,
				cluster,
				creacion,
				modificacion):
		self.nombre = nombre
		self.tamanio = tamanio
		self.tamanio_pref = tamanio_pref
		self.cluster = cluster
		self.creacion = creacion
		self.modificacion = modificacion


#Método que permite leer los datos del superbloque y asignarlos a un objeto de este tipo
def generar_super_bloque():
	#En este método ocuparemos las funciones seek y read para archivos
	#Seek se encarga de establecer un cursor en la posición dada por parametro
	#Read se encarga de leer la cantidad de datos especificados como parametro

	#Leemos el nombre del sistema de archivos en las posiciones 0-8 de la imagen
	sistema.seek(0)
	nombre = sistema.read(8).decode(codif)

	if (nombre != "FiUnamFS"):
		raise Exception(
				"\n¡Algo salio mal!\n" +
				"Error: El sistema de archivos no es de tipo FiUnamFS."
			)
		exit()

	#Leemos la versión de implementación en las posiciones 10-13
	sistema.seek(10)
	version = sistema.read(3).decode(codif)

	#Leemos la etiqueta del volumen en las posiciones 20-35
	sistema.seek(20)
	et_volumen = sistema.read(15).decode(codif)

	#Leemos el tamaño del cluster (en bytes) en las posiciones 40-45
	sistema.seek(40)
	tam_cluster = int(sistema.read(5).decode(codif))

	#Leemos el número de clusters que mide el directorio en las posiciones 47-49
	sistema.seek(47)
	num_clusters_dir = int(sistema.read(2).decode(codif))

	#Leemos el número de clusters que mide la unidad completa en las posiciones 52-60
	sistema.seek(52)
	num_clusters_uni = int(sistema.read(8).decode(codif))

	return SuperBloque(nombre,
					version,
					et_volumen,
					tam_cluster,
					num_clusters_dir,
					num_clusters_uni)


#Método que obtiene una versión compacta del tamaño en bytes
def formatear_tamanio(tamanio):
	#Definimos una lista que a partir de un contador, nos dará la
    #unidad de medida de la memoria
    unidades = ['B','KB','MB','GB','TB','PB','EB','ZB','YB','BB']

    #Inicializamos el contador para no tener problemas de integridad
    contUnidad = 0

    #Bucle que permite ir dividiendo el tamaño obtenido hasta llegar
    #a su maxima unidad con un contador
    while( (tamanio / 1024) >= 1 ):
        contUnidad += 1
        tamanio = tamanio/1024

    #Regresamos el valor obtenido del tamaño reducido junto a su unidad
    #en forma de string para su formateo posterior
    return str(round(tamanio,1)) + " " + unidades[contUnidad]


#Método que permite formatear la fecha dado el formato dentro del sistema de archivos
def formatear_fecha(fecha):
	#Separamos los datos de la fecha en distintas variables
	anio = fecha[0:4]
	mes = fecha[4:6]
	dia = fecha[6:8]
	hora = fecha[8:10]
	minutos = fecha[10:12]
	segundos = fecha[12:14]

	#Empleamos la concatenacion de las variables con un formato amigable
	fecha_formateada = dia + "/" + mes + "/" + anio
	hora_formateada = hora + ":" + minutos + ":" + segundos

	return fecha_formateada + " " + hora_formateada


# Método que permite inicializar el directorio del sistema de archivos
def generar_directorio(info_sistema, directorio, nombres_archivos):
	directorio.clear()
	tam_entrada = 64 #Tamaño de cada entrada del directorio
	num_entradas_cluster = int(info_sistema.tam_cluster/tam_entrada) #Número de entradas por cluster
	
	#Mostramos las entradas en los 4 diferentes clusters
	for i in range(4):
		#Obtenemos la dirección de cada cluster a partir de su tamaño y número de cluster
		direccion_cluster = info_sistema.tam_cluster*(i+1)

		#Dirijimos el cursor hacia la direccion previamente obtenida
		sistema.seek(direccion_cluster)

		for i in range(num_entradas_cluster):
			nombre = sistema.read(15).decode(codif)
			sistema.read(1).decode(codif) #Movemos el cursor del espacio vacio

			#Si el nombre corresponde con una entrada no utilizada pasamos a la siguiente
			if(nombre == "..............."):
				sistema.read(48).decode(codif) #Movemos el cursor hasta la siguiente entrada
				continue

			nombre = nombre.replace(" ", "") #Eliminamos los espacios en blanco del nombre
			nombres_archivos.add(nombre) #Almacenamos el nombre del archivo al conjunto de unicidad
			
			tamanio = int(sistema.read(24-16).decode(codif))
			sistema.read(1).decode(codif) #Movemos el cursor del espacio vacio
			tamanio_pref = formatear_tamanio(tamanio) #Obtenemos el tamaño con su prefijo
			
			cluster = int(sistema.read(30-25).decode(codif))
			sistema.read(1).decode(codif) #Movemos el cursor del espacio vacio

			creacion = sistema.read(45-31).decode(codif)
			sistema.read(1).decode(codif) #Movemos el cursor del espacio vacio
			creacion = formatear_fecha(creacion)

			modificacion = sistema.read(60-46).decode(codif)
			sistema.read(65-61).decode(codif) #Movemos el cursor del espacio vacio
			modificacion = formatear_fecha(modificacion)

			entrada_aux = Entrada(nombre,tamanio,tamanio_pref,cluster,creacion,modificacion)

			directorio.append(entrada_aux)
			

#Método que permite mostrar el contenido del directorio
def mostrar_directorio(directorio):
	#Variables para el formateo de la salida
	f_nombre = "{:<16}"
	f_tamanio = "{:<14}"
	f_cluster = "{:<13}"
	f_creacion = "{:<25}"
	f_modificacion = "{:<24}"

	#Formateamos el encabezado del listado
	print("\n",f_nombre.format("Nombre"),end='')
	print(f_tamanio.format("Tamaño"),end='')
	print(f_cluster.format("Cluster"),end='')
	print(f_creacion.format("Creación:"),end='')
	print(f_modificacion.format("Última modificación:"))

	#Por cada entrada en el directorio, mostramos sus datos
	for entrada in directorio:
		print(f_nombre.format(entrada.nombre),end='')
		print(f_tamanio.format(entrada.tamanio_pref),end='')
		print(f_cluster.format(entrada.cluster),end='')
		print(f_creacion.format(entrada.creacion),end='')
		print(f_modificacion.format(entrada.modificacion))


#Método que copia un archivo del sistema FiUnamFS al sistema host
def copiar_externo(directorio, nombre_archivo, nombres_archivos, info_sistema):
	if(nombre_archivo in nombres_archivos):
		#Creamos el archivo destino en el sistema host
		try:
			destino = open(nombre_archivo,mode='w+b') #Importante especificar y trabajar con codififación ASCII
		#Si surge algún error, se le indica al usuario
		except IOError:
			print("\n¡Algo salio mal!\n")
			print("Error: El archivo no pudo ser copiado.")
			print("-> Por favor, intentalo de nuevo.")
			return "ERROR"

		for entrada in directorio:
			if(entrada.nombre == nombre_archivo):
				cluster_archivo = entrada.cluster
				tamanio_archivo = entrada.tamanio
				break

		direccion_archivo = info_sistema.tam_cluster * cluster_archivo
		sistema.seek(direccion_archivo)
		destino.write(sistema.read(tamanio_archivo))
		destino.close()

		print("\n->Se ha transferido correctamente el archivo.\n")

	else:
		print("\nError: El archivo no existe dentro de FiUnamFS.")


#Método que copia un archivo del sistema host al sistema FiUnamFS
def copiar_interno(ruta, directorio, nombres_archivos, info_sistema):
	nombre_archivo = os.path.basename(ruta)

	#Verificamos las posibles excepciones en el nombre del archivo
	if(nombre_archivo in nombres_archivos):
		print("\nError: El nombre del archivo ya existe en el sistema de archivos.")
		print("-> Por favor, modifica el nombre e intentalo de nuevo.")
		return "ERROR"
	elif(len(nombre_archivo) > 15):
		print("\nError: El nombre del archivo supera el límite del sistema de archivos (15 caracteres).")
		print("-> Por favor, modifica el nombre e intentalo de nuevo.")
		return "ERROR"

	#Obtenemos los datos en crudo con llamadas al sistema
	tamanio_archivo = os.path.getsize(ruta)
	creacion_archivo_epoch = os.path.getctime(ruta)
	modificacion_archivo_epoch = os.path.getmtime(ruta)

	#Formateamos las fechas obtenidas para que coincidan con el sistema
	nombre_archivo = nombre_archivo.rjust(15, ' ').encode(codif)
	tamanio_archivo_format = str(tamanio_archivo).rjust(8, '0').encode(codif)
	creacion_archivo = fecha_en_sistema(creacion_archivo_epoch).encode(codif)
	modificacion_archivo = fecha_en_sistema(modificacion_archivo_epoch).encode(codif)
	
	#Obtenemos el número de clusters que ocupara el archivo
	num_clusters_archivo = int(math.ceil(tamanio_archivo/info_sistema.tam_cluster))

	#Obtenemos el cluster inicial del archivo para sus datos
	cluster_inicial = buscar_espacio_disponible(num_clusters_archivo,info_sistema)

	#Verificamos si tenemos algún cluster inicial disponible
	if(cluster_inicial == -1):
		print("\nError: El sistema de archivos no tiene espacio suficiente.")
		print("-> Por favor, libera espacio en el sistema e intentalo de nuevo.")
		print("-> También podrías desfragmentar e intentarlo de nuevo.")
		return "ERROR"

	#Obtenemos el indice del directorio que esta disponible
	indice_directorio = buscar_entrada_disponible(directorio)

	if(cluster_inicial == -1):
		print("\nError: El directorio no tiene entradas disponibles.")
		print("-> Por favor, libera espacio en el sistema e intentalo de nuevo.")
		return "ERROR"

	#Dirijimos el cursor hacia la parte del sistema que corresponde al índice obtenido
	sistema.seek(1*info_sistema.tam_cluster + 64*indice_directorio)

	#Escribimos los datos de la entrada en el directorio
	sistema.write(nombre_archivo)
	sistema.write(b'\x00')
	sistema.write(tamanio_archivo_format)
	sistema.write(b'\x00')
	sistema.write(str(cluster_inicial).rjust(5,'0').encode('ASCII') )
	sistema.write(b'\x00')
	sistema.write(creacion_archivo)
	sistema.write(b'\x00')
	sistema.write(modificacion_archivo)
	sistema.write(b'\x00')

	#Escribimos los datos del archivo
	#Se inicia la conexión (lectura de la imagen) con el sistema de archivos
	try:
		archivo_nuevo = open(ruta,'rb')
	#Si el archivo no se encuentra, se le indica al usuario
	except IOError:
		print("\n¡Algo salio mal!\n")
		print("Error: El archivo no pudo ser copiado.")
		print("-> Por favor, intentalo de nuevo.")
		return "ERROR"

	#Dirijimos el cursor hacia la posición inicial que calculamos previamente
	sistema.seek(info_sistema.tam_cluster*cluster_inicial)

	#Escribimos el contenido del archivo fuente en el sistema FiUnamFS
	sistema.write(archivo_nuevo.read())

	#Cerramos la conexión
	archivo_nuevo.close()

	print("-> Se ha completado exitosamente la copia del archivo.")
	generar_directorio(info_sistema, directorio, nombres_archivos)


#Método que transforma el tiempo epoch en fechas con formato para el sistema
def fecha_en_sistema(tiempo_epoch):
	fecha_sistema = time.strftime("%Y%m%d%H%M%S", time.localtime(tiempo_epoch))

	return fecha_sistema


#Método que genera un bitmap de los clusters disponibles en el sistema
def generar_bitmap(bitmap, directorio):

	for entrada in directorio:
		#Numero de clusters que ocupa el archivo
		num_clusters = int(math.ceil(entrada.tamanio / info_sistema.tam_cluster))
		
		#Empleamos el numero de clusters que ocupa el archivo para marcarlos como
		#true en el bitmap y así considerarlos como no disponibles
		for i in range(entrada.cluster,entrada.cluster+num_clusters):
			bitmap[i] = True


#Método que busca un bloque disponible en el sistema de archivos para los datos de una nueva entrada
def buscar_espacio_disponible(num_clusters, info_sistema):

	global bitmap 

	cuentaCluster = 0
	for i in range(len(bitmap)):
		if(bitmap[i] == False):
			#Cuenta el número de clusters disponibles contiguos encontrados
			cuentaCluster += 1

			if cuentaCluster == num_clusters:
				cluster_inicial = i - num_clusters + 1

				for j in range(cluster_inicial, cluster_inicial+num_clusters):
					bitmap[j] = True
				return cluster_inicial
		else:
			cuentaCluster = 0

	return -1 


#Método que busca una entrada disponible en el directorio del sistema
def buscar_entrada_disponible(directorio):
	contador = 0
	tam_entrada = 64
	num_entradas_cluster = int(info_sistema.tam_cluster/tam_entrada) #Número de entradas por cluster

	#Mostramos las entradas en los 4 diferentes clusters
	for i in range(4):
		#Obtenemos la dirección de cada cluster a partir de su tamaño y número de cluster
		direccion_cluster = info_sistema.tam_cluster*(i+1)

		#Dirijimos el cursor hacia la direccion previamente obtenida
		sistema.seek(direccion_cluster)

		for i in range(num_entradas_cluster):
			nombre = sistema.read(15).decode(codif)
			sistema.read(1).decode(codif) #Movemos el cursor del espacio vacio

			#Si el nombre corresponde con una entrada no utilizada devolvemos el indice
			if(nombre == "..............."):
				return contador
			else:
				contador += 1
				sistema.read(48).decode(codif) #Movemos el cursor hasta la siguiente entrada

	return -1


#Método para obtener el indice de la entrada de un archivo en el directorio
def buscar_entrada_nombre(nombre_archivo,info_sistema, directorio):
	contador = 0
	tam_entrada = 64
	num_entradas_cluster = int(info_sistema.tam_cluster/tam_entrada) #Número de entradas por cluster

	#Mostramos las entradas en los 4 diferentes clusters
	for i in range(4):
		#Obtenemos la dirección de cada cluster a partir de su tamaño y número de cluster
		direccion_cluster = info_sistema.tam_cluster*(i+1)

		#Dirijimos el cursor hacia la direccion previamente obtenida
		sistema.seek(direccion_cluster)

		for i in range(num_entradas_cluster):
			nombre = sistema.read(15).decode(codif)
			sistema.read(1).decode(codif) #Movemos el cursor del espacio vacio

			#Si el nombre corresponde con una entrada no utilizada devolvemos el indice
			if(nombre == nombre_archivo.rjust(15, ' ')):
				return contador
			else:
				contador += 1
				sistema.read(48).decode(codif) #Movemos el cursor hasta la siguiente entrada

	return -1


#Método para eliminar un archivo del sistema FiUnamFS
def eliminar_archivo(nombre_archivo, directorio, info_sistema):
	#ELIMINAMOS EL ARCHIVO DEL DIRECTORIO

	indice_directorio = buscar_entrada_nombre(nombre_archivo, info_sistema, directorio)
	if(indice_directorio == -1):
		print("\nError: El directorio no cuenta con el archivo especificado.\n")
		return "ERROR"
	
	#Dirijimos el cursor hacia la parte del sistema que corresponde al índice obtenido
	sistema.seek(1*info_sistema.tam_cluster + 64*indice_directorio)

	#Modificamos el nombre del archivo por el de la nomenclatura empleada por el sistema
	#para entradas disponibles
	sistema.write("...............".encode(codif))


	#ELIMINAMOS LOS DATOS DEL ARCHIVO
	for entrada in directorio:
		if (entrada.nombre == nombre_archivo):
			cluster_inicial = int(entrada.cluster)
			num_clusters_archivo = int(math.ceil(entrada.tamanio/info_sistema.tam_cluster))

	for i in range(cluster_inicial, cluster_inicial+num_clusters_archivo):
		bitmap[i] = False

	print("\nArchivo eliminado correctamente.\n")


#Método que realiza la desfragmentación del sistema de archivos
def desfragmentar(directorio, bitmap):
	for entrada in directorio:
		cursor_cluster = 5 #Variable que va almacenando el cluster que estamos analizando

		cluster_inicial = entrada.cluster
		num_clusters_archivo = int(math.ceil(entrada.tamanio/info_sistema.tam_cluster))
		disponible = False

		while(cluster_inicial > cursor_cluster):
			contador_disponibles = 0
			for i in range(cursor_cluster,len(bitmap)):
				#Por cada bloque disponible en el bitmap
				if(bitmap[i] == False):
					contador_disponibles += 1
				else:
					cursor_cluster = i + 1
					break

				if(contador_disponibles == num_clusters_archivo):
					disponible = True
					break
				i += 1

			if(disponible == True):
				break

		if(disponible == True):
			sistema.seek(cluster_inicial*info_sistema.tam_cluster)
			datos = sistema.read(entrada.tamanio)

			#Liberamos en el bitmap los espacios que fueron modificados
			for i in range(cluster_inicial, cluster_inicial+num_clusters_archivo):
				bitmap[i] = False

			entrada.cluster = cursor_cluster
			sistema.seek(entrada.cluster*info_sistema.tam_cluster)
			sistema.write(datos)

			#Marcamos como ocupados las nuevas posiciones de los datos en el bitmap de clusters
			for i in range(entrada.cluster, entrada.cluster+num_clusters_archivo):
				bitmap[i] = True

			#Ahora buscamos la entrada del archivo en el directorio del sistema y modificamos
			#su cluster inicial
			indice_entrada = buscar_entrada_nombre(entrada.nombre,info_sistema, directorio)
			sistema.seek(1*info_sistema.tam_cluster + 64*indice_entrada + 25)
			sistema.write(str(entrada.cluster).rjust(5, ' ').encode(codif))

	print("\n-> Desfragmentación concluida correctamente.")


#Método para actualizar los objetos que guardan información sobre el sistema de archivos
def actualizar_info(info_sistema, directorio, nombres_archivos, bitmap):
	generar_directorio(info_sistema, directorio, nombres_archivos) #Generación recurrente del directorio
	generar_bitmap(bitmap, directorio)


#VARIABLES GLOBALES
codif = 'ASCII' #La decodificación que se empleará en el sistema sera ASCII
directorio = [] #Lista de entradas que conforman el directorio de nuestro sistema de archivos
nombres_archivos = {None} #Conjunto de nombres de archivos que permite verificar su unicidad
info_sistema = generar_super_bloque() #Asignación de la información del sistema de archivos a partir del superbloque
bitmap = 5*[True] + (info_sistema.num_clusters_uni-5)*[False]

#Una vez iniciado el programa se actualiza el directorio y el bitmap
actualizar_info(info_sistema, directorio, nombres_archivos, bitmap) 

while(True):
	actualizar_info(info_sistema, directorio, nombres_archivos, bitmap)

	print("\n\t-> Bienvenido <-")
	print("1) Mostrar directorio")
	print("2) Copiar archivo del FiUnamFS a tu computadora")
	print("3) Copiar archivo de tu computadora al FiUnamFS")
	print("4) Eliminar archivo del FiUnamFS")
	print("5) Desfragmentar sistema")
	print("6) Salir")

	try:
		opcion = int(input("Ingresa la opción de tu elección: "))
	except ValueError:
		print("\nError: Tipo de dato equivocado.")
		print("-> Por favor, ingresa un valor númerico.")
		continue

	if(opcion == 1):
		mostrar_directorio(directorio)
	elif(opcion ==  2):
		nombre_archivo = input("Ingresa el nombre del archivo (incluyendo extension): ")
		copiar_externo(directorio, nombre_archivo, nombres_archivos, info_sistema)
	elif(opcion ==  3):
		nombre_archivo = input("Ingresa el nombre del archivo (incluyendo extension): ")
		copiar_interno(nombre_archivo, directorio, nombres_archivos, info_sistema)
	elif(opcion ==  4):
		nombre_archivo = input("Ingresa el nombre del archivo (incluyendo extension): ")
		eliminar_archivo(nombre_archivo, directorio, info_sistema)
	elif(opcion ==  5):
		desfragmentar(directorio, bitmap)
	elif(opcion == 6):
		print("\n¡Hasta la próxima!\n")
		break;	
	else:
	    print("\nError: Opción invalida.")
	    print("\n-> Por favor, ingresa una opción valida.")
