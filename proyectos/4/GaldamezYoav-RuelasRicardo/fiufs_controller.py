#Se inicia la conexión (lectura de la imagen) con el sistema de archivos
try:
	sistema = open('fiunamfs.img', encoding='ASCII') #Importante especificar y trabajar con codififación ASCII
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


#Método que permite leer los datos del superbloque y asignarlos a un objeto de este tipo
def crear_super_bloque():
	#En este método ocuparemos las funciones seek y read para archivos
	#Seek se encarga de establecer un cursor en la posición dada por parametro
	#Read se encarga de leer la cantidad de datos especificados como parametro

	#Leemos el nombre del sistema de archivos en las posiciones 0-8 de la imagen
	sistema.seek(0)
	nombre = sistema.read(8)

	if (nombre != "FiUnamFS"):
		raise Exception(
				"\n¡Algo salio mal!\n" +
				"Error: El sistema de archivos no es de tipo FiUnamFS."
			)
		exit()

	#Leemos la versión de implementación en las posiciones 10-13
	sistema.seek(10)
	version = sistema.read(4)

	#Leemos la etiqueta del volumen en las posiciones 20-35
	sistema.seek(20)
	et_volumen = sistema.read(16)

	#Leemos el tamaño del cluster (en bytes) en las posiciones 40-45
	sistema.seek(40)
	tam_cluster = sistema.read(6)

	#Leemos el número de clusters que mide el directorio en las posiciones 47-49
	sistema.seek(47)
	num_clusters_dir = sistema.read(3)

	#Leemos el número de clusters que mide la unidad completa en las posiciones 52-60
	sistema.seek(52)
	num_clusters_uni = sistema.read(9)

	

	return SuperBloque(nombre,
					version,
					et_volumen,
					tam_cluster,
					num_clusters_dir,
					num_clusters_uni)


#Método que permite mostrar el contenido del directorio
def mostrar_directorio(info_sistema):
	direccion_cluster_1 = info_sistema.tam_cluster;
	direccion_cluster_2 = info_sistema.tam_cluster*2;
	direccion_cluster_3 = info_sistema.tam_cluster*3;
	direccion_cluster_4 = info_sistema.tam_cluster*4;



info_sistema = crear_super_bloque()



print(info_sistema.tam_cluster)

