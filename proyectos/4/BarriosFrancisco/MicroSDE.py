import os
import time
class SuperBloque:
	def __init__(self):
		try:
			self.archivo = open('fiunamfs.img','r+b')
			self.archivo.seek(0)
			self.name = self.archivo.read(8).decode('ASCII')
			if self.name != 'FiUnamFS':
				print ('Sistema de archivos no valido')
			else:
				print ('Sistema de archivos montado')
				self.archivo.seek(10)
				self.version = self.archivo.read(3).decode('ASCII')
				self.archivo.seek(20)
				self.label = self.archivo.read(15).decode('ASCII')
				self.archivo.seek(40)
				self.sizeCluster = int(self.archivo.read(5).decode('ASCII'))
				self.archivo.seek(47)
				self.numClustersDir = int(self.archivo.read(2).decode('ASCII'))
				self.archivo.seek(52)
				self.numClustersTotal = int(self.archivo.read(8).decode('ASCII'))
			self.archivo.close()
		except IOError:
			print('Algo anda mal...')
		except FileNotFoundError:
			print('¿Seguro que ya tienes el archivo \"fiunamfs.img\" en la misma carpeta que este código?')
class archivoX:
	def __init__(self):
		self.name = ''
		self.size = 0
		self.firstCluster = 0
		self.fechaCreacion = ''
		self.fechaModificacion = ''
		self.espacioLibre= ''

class FileSystem:
	def __init__(self):
		self.sB = SuperBloque()
		self.archivo = open('fiunamfs.img','r+b')		#El archivo del SIstema de Archivos
		self.directorio = []
		#Primero se lista al directorio para obtener un bitmap correcto
		self.ls()
		#el directorio esta ubicado en los clusters 1 a 4
		self.bitmapLista = 5*[True] + (self.sB.numClustersTotal - 5)*[False]
		self.bitmapLista = createBitmap(self.bitmapLista, self.directorio, self.sB.sizeCluster)
		
	def ls(self):
		self.totalEntradas = int((self.sB.numClustersDir * self.sB.sizeCluster)/64)
		self.archivo.seek(self.sB.sizeCluster)
		self.directorio = []
		for i in range (self.totalEntradas):
			#nombre del archivo 0 - 15
			nameArch = self.archivo.read(15).decode('ASCII')
			if nameArch == '...............':
				self.archivo.read(49)			#para llegar al 64
				continue
			nameArch = deleteWhiteSpaces(nameArch)
			ax = archivoX()
			ax.name = nameArch
			#tamanio del archivo 16 - 24s
			self.archivo.read(1)
			ax.size = int(self.archivo.read(8).decode('ASCII'))
			#cluster inicial 25 - 30
			self.archivo.read(1)
			ax.firstCluster = int(self.archivo.read(5).decode('ASCII'))
			#fecha de creación 31 - 45
			self.archivo.read(1)
			ax.fechaCreacion = self.archivo.read(14).decode('ASCII')
			#fecha de modificacion 46 - 60
			self.archivo.read(1)
			ax.fechaModificacion = self.archivo.read(14).decode('ASCII')
			#espacio no utilizado 61 - 64
			self.archivo.read(1)
			ax.espacioLibre = self.archivo.read(3).decode('ASCII')
			self.directorio.append(ax)
	
	def copyInt(self, rutaArchivo):
		try:
			newArch = open(rutaArchivo, 'rb')
			ax = archivoX()
			ax.name = os.path.basename(rutaArchivo)
			if len(ax.name) > 15:
				print ('El nombre del archivo sobrepasa el maximo permitido (15 caracteres)')
				return -1
			ax.size = os.path.getsize(rutaArchivo)
			ax.fechaCreacion = getFecha(os.path.getctime(rutaArchivo))
			ax.fechaModificacion = getFecha(os.path.getmtime(rutaArchivo))
		except IOError:
			print ('Algo anda mal...')
			return -1
		except FileNotFoundError:
			print ('El archivo ' + rutaArchivo + ' no existe')
			return -1
		if busquedaFiunamfs(ax.name, self.directorio) != -1:
			print ('El archivo ' + ax.name + ' ya existe dentro de FiunamFS')
			return -1
		try:
			ax.name.encode('ASCII')
		except:
			print ('El nombre del archivo consta de caracteres fuera del ASCII tradicional')
			return -1
		indiceEnDir = searchDirLibre(((self.sB.numClustersDir * self.sB.sizeCluster)/64),self.archivo,self.sB.sizeCluster)
		if indiceEnDir == -1:
			print('Ya no hay espacios libres en el directorio :(')
			return -1
		NewFileFirstCluster, self.bitmapLista = searchClustersSeguidos(sizeEnClusters(ax.size, self.sB.sizeCluster), self.bitmapLista)
		if NewFileFirstCluster == -1:
			print('Se acabo el espacio continuo para almacenar al archivo')
			print('Deberías probar desfragmentar la memoria e intentar de nuevo')
			return -1
		ax.firstCluster = NewFileFirstCluster
		#se escriben los metadatos del archivo
		escribirEnDir(self.archivo, ax, indiceEnDir, self.sB.sizeCluster)
		#se escribe el archivo dentro del sistema de archivos
		self.archivo.seek(self.sB.sizeCluster*NewFileFirstCluster)
		self.archivo.write(newArch.read())
		newArch.close()
		print('Se ha importado \"' + rutaArchivo + '\" al sitema FiUnamFS')
		
	def copyOut(self, nameArchivo):
		indice = busquedaFiunamfs(nameArchivo, self.directorio)
		if indice == -1:
			print('El archivo ' + nameArchivo + ' no existe dentro de FiUnamFS')
			return -1
		ArchivoAExportar = self.directorio[indice]
		try:
			FileToExport = open(ArchivoAExportar.name, 'w+b')
			self.archivo.seek(self.sB.sizeCluster*ArchivoAExportar.firstCluster)
			FileToExport.write(self.archivo.read(ArchivoAExportar.size))
			FileToExport.close()
			print('El archivo ' + nameArchivo + ' ha sido exportado a su computadora')
		except IOError:
			print('Ocurrió un error al exportar el archivo')
			return -1
		
	def delete(self, nameArchivo):
		indice = busquedaFiunamfs(nameArchivo, self.directorio)
		if indice == -1:
			print('El archivo ' + nameArchivo + ' no existe dentro de FiUnamFS')
			return -1
		indiceEnImagen = busquedaEnImagen((self.sB.numClustersDir * self.sB.sizeCluster)/64,  nameArchivo, self.archivo, self.sB.sizeCluster)
		archivoEliminar = self.directorio[indice]
		firstCluster = archivoEliminar.firstCluster
		numClusters = sizeEnClusters(archivoEliminar.size, self.sB.sizeCluster)
		#se marcan los clusters como libres
		for i in range(firstCluster, firstCluster + numClusters):
			self.bitmapLista[i] = False
		self.archivo.seek(self.sB.sizeCluster + 64*indiceEnImagen)
		self.archivo.write('...............'.encode('ASCII'))
		self.archivo.seek(self.sB.sizeCluster + 64*indiceEnImagen + 15)
		self.archivo.write(b'\x00' * 49)
		self.directorio.pop(indice)
		#se borra del area de datos
		self.archivo.seek(self.sB.sizeCluster*archivoEliminar.firstCluster)
		self.archivo.write(b'\x00' * archivoEliminar.size)
		print('Se ha eliminado el archivo ' + nameArchivo + ' de FiUnamFS')
		
	def defragment(self):
		numClusters = self.sB.numClustersTotal - 5
		for i in range (5,numClusters):
			for j in range(5,numClusters - i):
				if self.bitmapLista[i] == False:
					if self.bitmapLista[j + 1] == False:
						continue
					self.bitmapLista[j] = True
					self.bitmapLista[j + 1] = False
					#primero, se recorre el cluster de datos un cluster anterior
					self.archivo.seek(self.sB.sizeCluster * j)
					self.archivo.write(self.archivo.read(self.sB.sizeCluster * (j+1)))
					indice = buscarFirstCluster(j + 1, self.directorio)
					if indice == -1:
						continue
					#se actualiza el cluster inicial del archivo en la lista del directorio, si es que este fue el que se recorrio
					self.directorio[indice].firstCluster -= 1
					indiceEnImagen = busquedaEnImagen((self.sB.numClustersDir * self.sB.sizeCluster)/64,self.directorio[indice].name, self.archivo, self.sB.sizeCluster)
					#se actualiza el cluster inicial en el directorio
					self.archivo.seek(self.sB.sizeCluster + 64*indiceEnImagen + 25)
					self.archivo.write(str(self.directorio[indice].firstCluster).encode('ASCII'))
				else:
					continue
		print ('Sistema desfragmentado, revise con \"ls\" los cambios')

#busca si el ciclo for de "defragment" ha llegado a un cluster inicial
def buscarFirstCluster(numCluster, directorio):
	indice = 0
	for i in directorio:
		if i.firstCluster == numCluster:
			return indice
		indice += 1
	return -1
	
#se marcan todos los cluster ocupados por los archivos
#directorio es una lista con los metadatos de los archivos
#lista es la generada indicando los primeros 5 cluster como ocupados
def createBitmap(lista, directorio, sizeCluster):
	for arch in directorio:
		numClusters = sizeEnClusters(arch.size, sizeCluster)
		for i in range(arch.firstCluster, arch.firstCluster + numClusters):
			lista[i] = True
	return lista

def sizeEnClusters(sizeEnBytes, sizeCluster):
	return (sizeEnBytes + (sizeCluster - 1))//sizeCluster
	
#busca un espacio en el directorio para alojar los metadatos del nuevo archivo
def searchDirLibre(numEntradas,archivo,sizeCluster):
	archivo.seek(sizeCluster)
	for i in range(int(numEntradas)):
		name = archivo.read(15).decode('ASCII')
		if name == '...............':
			return i
		archivo.read(49)
	return -1

#sirve para saber si el archivo a importar ya esta dentro de fiunamfs o si hay un archivo con el mismo nombre dentro de la lista que representa al diirectorio
#ademas de buscar si existe un archivo en caso de que se quiera exportar hacia la computadora
def busquedaFiunamfs(nameFile, directorio):
	indice = 0
	for ax in directorio:
		if ax.name == nameFile:
			return indice
		indice = indice + 1
	return -1

#busca el archivo dentro de la imagen del sistemma de archivos
def busquedaEnImagen(numEntradas, nameFile, archivo, sizeCluster):
	archivo.seek(sizeCluster)
	for i in range(int(numEntradas)):
		if nameFile == deleteWhiteSpaces(archivo.read(15).decode('ASCII')):
			return i
		archivo.read(49)
	return -1

#getctime y getmtime dan las fechas de creación y modificación en segundos a partir del momento actual
#por lo que deben ser convertidas
def getFecha(segundos):
	tiempo = time.gmtime(segundos)
	year = str(tiempo.tm_year).rjust(4,'0')
	month = str(tiempo.tm_mon).rjust(2,'0')
	day = str(tiempo.tm_mday).rjust(2,'0')
	hour = str(tiempo.tm_hour).rjust(2,'0')
	minute = str(tiempo.tm_min).rjust(2,'0')
	seconds = str(tiempo.tm_sec).rjust(2,'0')
	return year + month + day + hour + minute + seconds

#se buscan cluster seguidos para alojar al nuevo archivo
def searchClustersSeguidos(totalClusters, bitmap):
	cont = 0
	for i in range(len(bitmap)):
		if bitmap[i] == False:
			cont = cont + 1
			if cont == totalClusters:
				indice = i - totalClusters + 1
				for j in range(indice, indice + totalClusters):
					bitmap[j] = True
				return indice, bitmap
		else:
			cont = 0
	return -1, bitmap

def escribirEnDir(FileSystem, NewFile, indiceDir, sizeCluster):
	FileSystem.seek(sizeCluster + 64*indiceDir)
	FileSystem.write(NewFile.name.rjust(15,' ').encode('ASCII'))
	FileSystem.write(b'\x00')
	FileSystem.write(str(NewFile.size).rjust(8,'0').encode('ASCII'))
	FileSystem.write(b'\x00')
	FileSystem.write(str(NewFile.firstCluster).rjust(5,'0').encode('ASCII'))
	FileSystem.write(b'\x00')
	FileSystem.write(NewFile.fechaCreacion.encode('ASCII'))
	FileSystem.write(b'\x00')
	FileSystem.write(NewFile.fechaModificacion.encode('ASCII'))
	FileSystem.write(b'\x00')

def deleteWhiteSpaces(cadena):
	cadenaNueva = ''
	lista = cadena.split()
	for i in lista:
		cadenaNueva = cadenaNueva + i
	return cadenaNueva
		
def imprimirDir(directorio, sizeCluster):
	print(' | Nombre' + ' '*9 + '| Tamanio   | Cluster Inicial | Cluster Final   | Fecha de Creación   | Fecha de modificación |')
	print('-' * 113)
	for ax in directorio:
		print(' | ' + ax.name.ljust(15) + '| ' + str(ax.size).ljust(10) + '| ' + str(ax.firstCluster).ljust(16) + '| ' + str(ax.firstCluster + sizeEnClusters(ax.size ,sizeCluster)).ljust(16) + '| ' + formatoFecha(ax.fechaCreacion) + ' |  ' + formatoFecha(ax.fechaModificacion) + '  | ')

def formatoFecha(fecha):
	year = fecha[:4]
	month = fecha[4:6]
	day = fecha[6:8]
	hour = fecha[8:10]
	minute = fecha[10:12]
	seconds = fecha[12:14]
	return day + '/' + month + '/' + year + ' ' + hour + ':' + minute + ':' + seconds

def ayuda():
	print('   =========================== AYUDA ===========================')
	print('   ls:                 Listar los contenidos del directorio')
	print('   copyOut <archivo>   Copia un archivo de FiUnamFS hacia el sistema')
	print('                       El archivo se ubicara en la misma carpeta que el archivo \"fiunamfs.unam\"')
	print('   copyInt <archivo>   Copia un archivo de su computadora hacia el sistema FiUnamFS')
	print('   delete  <archivo>   Elimina un archivo de FiUnamFS')
	print('   defragment          Desfragmenta el sistema de archvos. Recomendable usar \"ls\" antes y después de usar este comando para observar los resultados')
	print('   salir               Salir del programa')
	
def select():
	opcion = ['']
	FS = FileSystem()
	while opcion[0] != 'salir':
		entrada = input('\033[92m >> \033[0m')
		opcion = entrada.split()
		if opcion[0] == 'ls':		#listar los contenidos del directorio
			FS.ls()
			imprimirDir(FS.directorio, FS.sB.sizeCluster)
		elif opcion[0] == 'copyInt':		#copiar archivos de FiUnamFS al sistema
			if len(opcion) == 2:
				FS.ls()
				FS.copyInt(opcion[1])
			elif len(opcion) == 1:
				print ('Comando incompleto. Especifica el archivo')
		elif opcion[0] == 'copyOut':
			if len(opcion) == 2:
				FS.ls()
				FS.copyOut(opcion[1])
			elif len(opcion) == 1:
				print ('Comando incompleto. Especifica el archivo')
		elif opcion[0] == 'delete':
			if len(opcion) == 2:
				FS.ls()
				FS.delete(opcion[1])
			elif len(opcion) == 1:
				print ('Comando incompleto. Especifica el archivo')
		elif opcion[0] == 'defragment':
			FS.defragment()
		elif opcion[0] == 'ayuda':
			ayuda()
		elif opcion[0] == 'salir':
			FS.archivo.close()
			break
		else:
			print('\033[31m Comando incorrecto, deberías probar con \"ayuda\"...\033[0m')

select()

