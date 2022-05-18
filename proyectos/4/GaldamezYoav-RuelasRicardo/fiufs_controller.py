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
    unidades = ['KB','MB','GB','TB','PB','EB','ZB','YB','BB']

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
	print(f_nombre.format("Nombre"),end='')
	print(f_tamanio.format("Tamaño"),end='')
	print(f_cluster.format("Cluster"),end='')
	print(f_creacion.format("Creación:"),end='')
	print(f_modificacion.format("Última modificación:"))

	for entrada in directorio:
		print(f_nombre.format(entrada.nombre),end='')
		print(f_tamanio.format(entrada.tamanio),end='')
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


codif = 'ASCII'
directorio = [] #Lista de entradas que conforman el directorio de nuestro sistema de archivos
nombres_archivos = {None} #Conjunto de nombres de archivos que permite verificar su unicidad
info_sistema = generar_super_bloque() #Asignación de la información del sistema de archivos a partir del superbloque
generar_directorio(info_sistema, directorio, nombres_archivos) #Generación inicial del directorio
mostrar_directorio(directorio)
copiar_externo(directorio,"README.org",nombres_archivos,info_sistema)