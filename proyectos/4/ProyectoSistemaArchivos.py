"""
Autores
Davila Ortega Jesus Eduardo
Espinosa Cortez Gisselle
"""
"""
Bibliotecas utilizadas para el desarrollo del programa
"""
import os
import math
import time
from tkinter import *

#Clase sistema de archivos creada especificamente para obtener los datos del sistema de archivos
#Los métodos de la clase son aquellos relacionados con algun dato que tenga la clase
class sistema:

	#Atributos de nuestra clase sistema por defecto
	file = open('fiunamfs.img',"br+")
	nombre = ''
	version = ''
	etiquetaVol = ''
	LongitudCluster = 0
	cantidadClusterD = 0
	cantidadClusterU = 0
	lonitudEntradaDir = 64
	
	"""
	Métodos de la clase sistema para su correcto funcionamiento
	"""
	
	#Obteniendo los datos apartir del archivo que se requiera
	def __init__(self,ruta):
			salida.delete('1.0',END)
			self.file = open(ruta,"br+")
			self.nombre = self.file.read(8)
			if ConvertirAString(self.nombre) == "FiUnamFS":
				self.version = self.leer(10,13)
				self.etiquetaVol = self.leer(20,35)
				self.LongitudCluster = int(self.leer(40,45))
				self.cantidadClusterD = int(self.leer(47,49))
				self.cantidadClusterU = int(self.leer(52,60))
			else:
				salida.insert(INSERT,"El sistema de archivos no esta diseñado ")
				salida.insert(INSERT,"para trabajar con ese micro sistema de archivos")

	def imprimirCaracteristicas(self):
		salida.delete('1.0',END)
		sistemaNombre = ConvertirAString(self.nombre)
		sistemaVersion = ConvertirAString(self.version)
		sistemaEtiqueta = ConvertirAString(self.etiquetaVol)
		longitudCluster = str(self.LongitudCluster)
		cantidadClusterDir= str(self.cantidadClusterD)
		cantidadClusterUnidad = str(self.cantidadClusterU)
		
		salida.insert(INSERT,"Nombre del sistema de archivos: "+sistemaNombre+"\n")
		salida.insert(INSERT,"Version de implementacion: "+sistemaVersion+"\n")
		salida.insert(INSERT,"Etiqueta del volumen: "+sistemaEtiqueta+"\n")
		salida.insert(INSERT,"Longitud del cluster en bytes:"+longitudCluster+"\n")
		salida.insert(INSERT,"Numero de clusters que mide el directorio:"+cantidadClusterDir+"\n")
		salida.insert(INSERT,"Numero de clusters que mide la unidad completa:"+cantidadClusterUnidad+"\n")
		
		
	#Método para obtener todos los datos del directorio, incluyendo los espacios vacios
	def getDirectorio(self):
		archivos = []
		for i in range(int(self.LongitudCluster),int(self.LongitudCluster)*(int(self.cantidadClusterD)+1),int(self.lonitudEntradaDir)):
			archivos.append(self.leer(i,i+self.lonitudEntradaDir))
		return archivos

	#Método encargado de imprimir el contenido del directorio, ignorando las entradas no utilizadas del directorio.
	def imprimirDirectorio(self):
		salida.delete('1.0',END)
		directorio = self.getDirectorio()
		auxiliar = ""
		directorioFinal = []
		for i in range(0,directorio.__len__()):
			auxiliar2 = ConvertirAString(directorio[i][:15])
			if "..............." != auxiliar2:
				directorioFinal.append(auxiliar2)
		salida.insert(INSERT,"Los archivos dentro son: \n")
		for i in directorioFinal:
			salida.insert(INSERT,i+"\n")
	
	#Método encargado de imprimir el estado de las entradas del directorio ya sea vacio u ocupado
	def impresionVacios(self):
		salida.delete('1.0',END)
		auxiliar = self.clusterVacio()
		salida.insert(INSERT,"Cluster \t----------\tEstado\n")
		for i in range(auxiliar.__len__()):
			if auxiliar[i]==True:
				salida.insert(INSERT,str(i)+"\t----------\tVacio\n")
			else:
				salida.insert(INSERT,str(i)+"\t----------\tOcupado\n")

	#Método encargado de leer nuestro archivo.
	def leer(self,inicio,final):
		checkpoint = self.file.tell()
		self.file.seek(inicio,0)
		final = final - inicio
		resultado = self.file.read(final)
		self.file.seek(checkpoint,0)
		return resultado

	#Método encargado de obtener la cantidad de clusters necesarios para una insercion
	def calculoClusters(self,tamanio):
		clustersSuficientes = tamanio/self.LongitudCluster
		if tamanio%self.LongitudCluster != 0:
			clustersSuficientes = clustersSuficientes + 1
		return int(math.trunc(clustersSuficientes))

	#Metodo encargado de buscar si un archivo ya se encuentra dentro de FiUnamFs
	def repetido(self,nombre):
		auxiliar = agregarEspacios(nombre)
		for i in range(self.LongitudCluster,(int(self.cantidadClusterD)+1)*self.LongitudCluster,self.lonitudEntradaDir):
			presente = self.leer(i , i+15)
			if presente == auxiliar:
				return True
		return False
	
	#Método encargado de identificar si el cluster esta vacio u ocupado
	def clusterVacio(self):
		mapa = []
		for i in range(0,self.cantidadClusterU):
			mapa.append(True)
		for i in range(0,self.cantidadClusterD+1):
			mapa[i] = False
		for i in range(self.LongitudCluster,(int(self.cantidadClusterD)+1)*self.LongitudCluster,self.lonitudEntradaDir):
			if b'...............' == self.leer(i, i + 15):
				continue
			c1Inicial = int(self.leer(i+25,i+30))
			c1Necesario = self.calculoClusters(int(self.leer(i + 16, i + 24)))
			for j in range(c1Inicial,c1Necesario + c1Inicial):
				mapa[j] = False
		return mapa

	#Método encargado de actualizar el clusterInicial de un registro
	def refrescarRegistro(self,fila,clusterInicial):
		clusterIni = ConversionBytes(clusterInicial)

		while clusterIni.__len__() < 5:
			clusterIni = b'0'+clusterIni
		for i in range(self.LongitudCluster,(int(self.cantidadClusterD)+1)*self.LongitudCluster,self.lonitudEntradaDir):
			auxiliar = self.leer(i, i + 15)
			if fila[:15] == auxiliar:
				self.file.seek(i + 25)
				self.file.write(clusterIni)
				return
		salida.insert(INSERT,"No se puede refrescar el directorio")
		return

	#Método encargado de escribir un registro en una de las entradas no utilizadas del directorio
	def archivoNuevo(self,fila):
		for i in range(self.LongitudCluster,(int(self.cantidadClusterD)+1)*self.LongitudCluster,self.lonitudEntradaDir):
			auxiliar = self.leer(i,i+15)
			if b'...............' == auxiliar:
				self.file.seek(i)
				self.file.write(fila)
				return
		salida.insert(INSERT,"Error no hay espacio suficiente")
		return

	#Método encargado de añadir un archivo a FiUnamFs
	def addArchivo(self):
		salida.delete('1.0',END)
		try:
			ruta = Ruta2.get()
		except ValueError:
			salida.insert(INSERT,'Valores Incorrectos')
		
		#Se busca que el archivo exista
		if os.path.isfile(ruta) == False:
			salida.insert(INSERT,"Error no existe el archivo origen: "+path)
			return
		#Obteniendo los datos del archivo y adecuandolos a nuestro formato
		tamanio = os.stat(ruta).st_size
		nombre = agregarEspacios(os.path.split(ruta)[-1])
		nombre = bytes(nombre,"utf-8")

		#Se busca observar si el nombre no excede nuestra especificación
		if nombre.__len__() > 15:
			salida.insert(INSERT,"Error nombre demasiado grande, solo se permiten 15 caracteres")
			return

		#Se procede a observar si no hay un archivo con el mismo nombre dentro de FiUnamFs
		if self.repetido(nombre) == True:
			salida.insert(INSERT,"Error ya existe un archivo con el mismo nombre")
			return

		#Obteniendo el tamaño del archivo y comprobando si cumple con nuestras reglas.
		size = ConversionBytes(tamanio)
		if size.__len__() > 8:
			salida.insert(INSERT,"Error el tamanio del archivo es demasiado grande")
			return
		while size.__len__() < 8:
			size = b'0' + size
		
		#Obteniendo la fechas de creacion y modificacion del archivo
		fechaCreacionArch = convertirFecha(os.path.getctime(ruta))
		fechaModificacionArch = convertirFecha(os.path.getmtime(ruta))
		
		#Obtenemos la lista con los clusters vacios asi como la cantidad necesaria de ellos
		cantidadClusters = self.calculoClusters(tamanio)
		clustersVacios = self.clusterVacio()
		tamanioNecesario = cantidadClusters

		#Se empieza a recorrer la lista de los clusters para ver en donde encaja nuestro archivo de manera contigua
		for i in range(0,clustersVacios.__len__()):
			if clustersVacios[i] == True:
				tamanioNecesario = tamanioNecesario - 1
			else:
				tamanioNecesario = cantidadClusters
			if tamanioNecesario == 0:
				InicioCluster = ConversionBytes(i-(cantidadClusters-1))

				while InicioCluster.__len__() < 5:
					InicioCluster = b'0' + InicioCluster
				#Se abre el archivo y se lee su contenido
				archivoAux = open(ruta,"br")
				contenido = archivoAux.read()
				archivoAux.close()
				
				#Se busca en donde se va a insertar y se procede a escribir el contenido
				self.file.seek((i-(cantidadClusters-1))*self.LongitudCluster)
				self.file.write(contenido)

				#Se procede a escribir las caracteristicas del archivo
				alarmaError = self.archivoNuevo(b''+nombre+b'\x00'+size+b'\x00'+InicioCluster+
					b'\x00'+fechaCreacionArch+b'\x00'+fechaModificacionArch+b'\x00'+b'\x00'+b'\x00'+b'\x00')
				if alarmaError == False:
					salida.insert(INSERT,"No se pudo insertar el archivo")
					return
				else:
					salida.insert(INSERT,'Archivo copiado satisfactoriamente a fiunamfs')
					return
		salida.insert(INSERT,"No se pudo insertar, no hay suficiente espacio para que quepa")

	#Método que se encarga de copiar un archivo de FiUnamFs a nuestro equipo
	def obtenerArchivo(self):
		salida.delete('1.0',END)
		try:
			nombre = Archivo1.get()
			ruta = Ruta1.get()
		except ValueError:
			salida.insert(INSERT,'Valores Incorrectos')
		try:
			ruta = Ruta1.get()
		except ValueError:
			salida.insert(INSERT,'Valores Incorrectos')
		#Se obtiene el nombre en un formato para facilitar la busqueda
		AuxNombre = bytes(agregarEspacios(nombre),"utf-8")
		tamanio = 0
		AlertaEncontrado = False
		
		#Se procede a buscar el archivo en caso de no encontrarlo se lanza el mensaje
		for i in range(self.LongitudCluster,(int(self.cantidadClusterD)+1)*self.LongitudCluster,self.lonitudEntradaDir):
			fila = self.leer(i, i + 15)
			if AuxNombre == fila:
				cluster = int(self.leer(i + 25,i + 30))
				tamanio = int(self.leer(i+16,i+24))
				AlertaEncontrado = True
				break

		if AlertaEncontrado == False:
			salida.insert(INSERT,"Error el archivo "+nombre+" no se encontro o no existe")
			return

		#Leyendo el contenido del archivo a modificar y guardandolo
		contenido = self.leer(cluster*self.LongitudCluster,cluster*self.LongitudCluster+tamanio)

		#EScribiendo en el archivo de destino su contenido.
		if ruta.__len__() == 0:
			archivo = open(nombre,"wb")
		else:
			archivo = open(ruta+"/"+nombre,"bw")

		archivo.write(contenido)
		archivo.close()
		salida.insert(INSERT,"El archivo "+nombre+" fue copiado exitosamente\n en "+ruta)
		return

	#Método encargado de eliminar un archivo de FiUnamFs
	def borrarArchivo(self):
		salida.delete('1.0',END)
		try:
			archivo = Archivo2.get()
		except ValueError:
			salida.insert(INSERT,'Valores Incorrectos')
		#Se empieza a buscar el archivo para poder eliminarlo
		nombre = agregarEspacios(archivo)
		for i in range(self.LongitudCluster,(int(self.cantidadClusterD)+1)*self.LongitudCluster,self.lonitudEntradaDir):
			auxiliar = self.leer(i, i + 15)
			if nombre == ConvertirAString(auxiliar):
				self.file.seek(i)
				self.file.write(voidRegister())
				salida.insert(INSERT,"El archivo "+archivo+" fue eliminado satisfactoriamente")
				return
		salida.insert(INSERT,"No se pudo eliminar el archivo "+archivo)
		return

	#Método encargado de desfragmentar FiUnamFs
	def desfragmentacion(self):
		salida.delete('1.0',END)
		directorio = self.getDirectorio()

		#Obtenemos el directorio y ordenamos en base a su primer cluster
		for i in range(0,directorio.__len__()):
			for j in range(0,directorio.__len__()-i-1):
				auxiliar = directorio[j]
				directorio[j] = directorio[j + 1]
				directorio[j + 1] = auxiliar

		#Observamos si hay clusters vacios antes que ellos
		for i in range(0,directorio.__len__()):
			#Se ignoran los vacios
			if directorio[i][:15] == b'...............':
				continue
				
			#Obtenemos el estado de cada entrada del directorio
			vacios = self.clusterVacio()

			#Se empieza a buscar la entrada mas proxima para poder mover nuestros datos
			for j in range(int(directorio[i][25:30])-1,4,-1):
				if vacios[j] == False:
					ClusterInicial = j + 1
					tamanio = int(directorio[i][16:24])
					informacion = self.leer(int(directorio[i][25:30])*self.LongitudCluster,(int(directorio[i][25:30])*self.LongitudCluster)+tamanio)
					#Se busca y se escribe en donde se encontro un lugar disponible
					self.file.seek(ClusterInicial * self.LongitudCluster)
					self.file.write(informacion)

					AlarmaError = self.refrescarRegistro(directorio[i],ClusterInicial)

					if AlarmaError == False:
						salida.insert(INSERT,"Error no se pudo desfragmentar")
						return
					else:
						break
		salida.insert(INSERT,"Desfragmentacion llevada acabo exitosamente")
		return

"""
Métodos auxiliares para la ejecucion de nuestro programa
"""

#Método encargado de dar formato a los nombres que obtengamos
def agregarEspacios(cadena):
	while cadena.__len__() < 15:
		cadena = ' ' + cadena
	return cadena

#Método encargado de convertir a Bytes lo que le enviemos
def ConversionBytes(convertir):
	aux = bytes(str(convertir),"utf-8")
	return aux

#Método encargado de dar el formato necesitado a las fechas que obtengamos
def convertirFecha(fecha):
	datos = time.gmtime(fecha)
	fechaAcomodada = time.strftime("%Y%m%d%H%M%S",datos)
	fechaBytes = bytes(fechaAcomodada,"utf-8")
	return fechaBytes

#Método encargado de decodificar nuestros datos que enviemos
def ConvertirAString(dato):
	auxiliar = dato.decode("utf-8")
	return auxiliar

#Método encargado de generar un registro en blanco
def voidRegister():
	registro = b'...............'+b'\x00'+b'00000000'+b'\x00'
	registro = registro + b'00000'+b'\x00'+b'000000000000000'+b'\x00'
	regsitro = registro + b'000000000000000'+b'\x00'+b'\x00'+b'\x00'+b'\x00'
	return registro

#Método encargado de obtener la cadena para inicializar nuestra clase sistema
def obtenerSistema():
	salida.delete('1.0',END)
	try:
		nombre = Sistema.get()
	except ValueError:
		salida.insert(INSERT,"Valores Incorrectos")
	ArchivoPadre = sistema(nombre)
	salida.insert(INSERT,"Archivo encontrado y listo para usarse")
	
"""
Empieza la implementacion de la interfaz gráfica
"""
#Se inicializa nuestra ventana principal
ventana = Tk()
#Declaracion de nuestro objeto de clase sistema
global ArchivoPadre
#Variables utilizadas por la interfaz gráfica
Sistema = StringVar()
Ruta1 = StringVar()
Ruta2 = StringVar()
Archivo1 = StringVar()
Archivo2 = StringVar()
#Caracteristicas de nuestra ventana
ventana.title('Proyecto 4 Sistema de Archivos')
ventana.geometry('1100x620+50+50')
ventana.resizable(False,False)
ventana.config(bg="#000000")

#Definimos nuestro frame que contiene nuestro metodo de entrada para definir nuestro archivo
frame = Frame()
frame.config(bg="#3D0000", bd=10,relief="groove",width="700", height="100")
frame.pack(side="top")
Label(frame,bg="#3D0000",text="Inserte el dato necesario: ",font=("Times New Roman",14),fg="#C6BB6A").grid(row=0,column=0)
Entry(frame,textvariable=Sistema,bg="#C6BB6A").grid(row=0,column=1)
Button(frame,text="Seleccionar el sistema de archivos",width=30,bg="#950101",font=("Times New Roman",12),command=obtenerSistema).grid(row=0,column=2)


#Configuración del frame encargado de contener la salida
frameSalida = Frame()
frameSalida.config(bg="#3D0000", bd=10,relief="groove",width="700", height="100")
frameSalida.pack(side="left")

#Configuración de la caja de texto que se utilizara de salida para nuestro programa
Label(frameSalida,text="Informacion",font=("Times New Roman",14),bg="#C6AE00").grid(row=0,column=0)
salida=Text(frameSalida,wrap=NONE,width=60,height=30,bg="#C6BB6A")
salida.grid(row=0,column=0,padx=10,pady=10)

#Inicializando nuestra variable de clase sistema !!Se necesita el microsistema de archivos en el directorio de ejecución
ArchivoPadre = sistema('fiunamfs.img')

#Definimos el frame que contendra nuestros botones para la ejecucion
frameOpciones = Frame()
frameOpciones.config(bg="#3D0000", bd=10,relief="groove",width="700", height="100")
frameOpciones.pack(side="right")

#Configuración del boton encargado de imprimir el contenido
Button(frameOpciones,text="Listar Archivos",width=30,bg="#950101",font=("Times New Roman",12),command=(ArchivoPadre.imprimirDirectorio)).grid(row=0,column=0)

#Configuración del boton y las entradas necesarias para obtener un archivo de FIUnamFs
Button(frameOpciones,text="Copiar un archivo a tu sistema",width=30,bg="#950101",font=("Times New Roman",12),command=(ArchivoPadre.obtenerArchivo)).grid(row=1,column=0)
Label(frameOpciones,bg="#3D0000",text="Inserte el nombre del archivo: ",font=("Times New Roman",14),fg="#C6BB6A").grid(row=2,column=0)
Entry(frameOpciones,textvariable=Archivo1,bg="#C6BB6A").grid(row=2,column=1)
Label(frameOpciones,bg="#3D0000",text="Inserte la ruta donde se guardara el archivo: ",font=("Times New Roman",14),fg="#C6BB6A").grid(row=3,column=0)
Entry(frameOpciones,textvariable=Ruta1,bg="#C6BB6A").grid(row=3,column=1)

#Configuración del boton y las entradas necesarias para copiar un archivo a FiUnamFs
Button(frameOpciones,text="Copiar un archivo a FiUnamFs",width=30,bg="#950101",font=("Times New Roman",12),command=(ArchivoPadre.addArchivo)).grid(row=4,column=0)
Label(frameOpciones,bg="#3D0000",text="Inserte la ruta o el nombre del archivo: ",font=("Times New Roman",14),fg="#C6BB6A").grid(row=5,column=0)
Entry(frameOpciones,textvariable=Ruta2,bg="#C6BB6A").grid(row=5,column=1)

#Configuración del boton para desfragmentar
Button(frameOpciones,text="Desfragmentar",width=30,bg="#950101",font=("Times New Roman",12),command=(ArchivoPadre.desfragmentacion)).grid(row=6,column=0)

#Configuración del boton para obtener la disponibilidad de entradas en el directorio
Button(frameOpciones,text="Mapa de memoria disponible",width=30,bg="#950101",font=("Times New Roman",12),command=(ArchivoPadre.impresionVacios)).grid(row=7,column=0)

#Configuración del boton y la entrada necesaria para eliminar un archivo de FiUnamFs
Button(frameOpciones,text="Borrar un archivo de FiUnamFs",width=30,bg="#950101",font=("Times New Roman",12),command=(ArchivoPadre.borrarArchivo)).grid(row=8,column=0)
Label(frameOpciones,bg="#3D0000",text="Inserte el nombre del archivo: ",font=("Times New Roman",14),fg="#C6BB6A").grid(row=9,column=0)
Entry(frameOpciones,textvariable=Archivo2,bg="#C6BB6A").grid(row=9,column=1)

#Configuración del boton para poder ver las caracteristicas del sistema
Button(frameOpciones,text="Informacion de FiUnamFs",width=30,bg="#950101",font=("Times New Roman",12),command=(ArchivoPadre.imprimirCaracteristicas)).grid(row=10,column=0)

#Configuracion de nuestra scrollbar para poder movernos en caso de tener demasiada información
scrollBarVert = Scrollbar(frameSalida,command=salida.yview,bg="#000000")
scrollBarVert.grid(row=0,column=1,sticky="nsew")
salida.config(yscrollcommand=scrollBarVert.set)

ventana.mainloop()
