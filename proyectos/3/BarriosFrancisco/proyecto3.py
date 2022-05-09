from sys import argv
import time
def openFile (num_PID):
#Se trata de abrir el archivo maps, si existe, o si se tiene el permiso de lectura
	try:
		f = open("/proc/" + str(num_PID) + "/maps")
		lineas = f.readlines()
		listaMemoria = []
		for linea in lineas:
			arreglo = linea.split(' ')
			arreglo = deleteWhiteSpaces(arreglo)	#se eliminan elementos del arreglo vacios
			direcciones = arreglo[0].split('-')
			downAddress = direcciones[0]
			upAddress = direcciones[1]
			permisos = arreglo[1]
			size, numPages = calcularSize(downAddress, upAddress)
			color, uso, mapeo = getMapeo(arreglo)
			renglon = [mapeo,downAddress,upAddress,size,numPages,permisos,uso,color]
			listaMemoria.append(renglon)		#Se ingresan los datos obtenidos de un renglon a una lista
			#linea = f.readline()
		getMemory(listaMemoria)			#acabando todas las lineas, se procede a buscar
		f.close()
		main()
	except FileNotFoundError:
		print('El número PID del proceso no existe o hay un problema para abrir el archivo')
		main()
	
def calcularSize (baja, alta):
	resta = (int(alta,16) - int(baja,16))/1024
	numPages = str(resta/4) + ' pags'			#la resta devuelve KB, y con paginas de 4KB
	unidades = ['KB','MB','GB','TB','PB','EB','ZB','YB','BB']
	unidad = 0
	while (resta/1024) >= 1:
		unidad += 1
		resta = resta/1024
	size = str(resta) +  ' ' + unidades[unidad]
	return size, numPages
	
def getMapeo(arreglo):
	mapeo = 'Anonymus'			#por default, si es que no se encuentra la ruta del archivo (arreglo[5] no existe)
	uso = '-[Anon]-\n'
	color = '0m'				#color de RESET, con caracteres de escape ANSI
	if len(arreglo) == 6:
		if '/' in arreglo[5]:
			if 'deleted' in arreglo[5]:	#caso deleted
				mapeo = '...'
				color = '31m'
			elif 'x' in arreglo[1]:
				mapeo = 'Texto'
				color = '92m'
			elif (not 'r' in arreglo[1]) and (not 'w' in arreglo[1]):
				mapeo = 'Reserva'
			else:
				mapeo = 'Datos'
				color = '93m'
			uso = arreglo[5]
		elif '[stack]' in arreglo[5]:
			mapeo = 'Stack'
			uso = '[Stack]\n'
			color = '94m'
		elif '[heap]' in arreglo[5]:
			mapeo = 'Heap'
			uso = '[Heap]\n'
			color = '91m'
		elif '[vvar]' in arreglo[5]:
			mapeo = 'Kernel Vars'
			uso = '[Kernel Vars]\n'
			color = '95m'
		elif ('[vsyscall]' in arreglo[5]) or ('[vectors]' in arreglo[5]) or ('[vdso]' in arreglo[5]):
			mapeo = 'Sys calls'
			uso = arreglo[5]
			color = '96m'
	return color, uso, mapeo	#color: dependiendo el uso, sera el color
					#uso: directorio, si existe, o uso explicito
					#mapeo: en que se usa esa region de memoria
	
#En mi caso, a veces el arreglo lanzaba elementos que contenian '', por lo que estos se eliminan
def deleteWhiteSpaces(arreglo):
	listaSinEspacios = []
	for i in arreglo:
		if i != '':
			listaSinEspacios.append(i)
	#para el caso especial / (deleted), estos se almacenan en lista[5] y lista[6], por lo que se unen en un solo elemento, y se elimina el ultimo
	if len(listaSinEspacios) == 7:
		listaSinEspacios[5] = listaSinEspacios[5] + listaSinEspacios[6]
		listaSinEspacios.pop()
	return listaSinEspacios
	
def getMemory(listaMemoria):
	hayHeap = False
	posicion = 0
	direcActual = ''
	direcPasada = '0'
	for renglon in listaMemoria:
		#buscando espacios vacios
		direcActual = renglon[1]
		if (int(direcActual,16)-int(direcPasada,16) == 0) or direcPasada == '0':
			direcPasada = renglon[2]
			if renglon[0] == 'Heap':
				hayHeap = True
			if hayHeap:
				if renglon[0] == 'Texto':
					listaMemoria[posicion][0] = 'Bib -> Texto'
				if renglon[0] == 'Datos':
					listaMemoria[posicion][0] = 'Bib -> Datos'
			#si el archivo no especifico un heap explicitamente
			else:
				if (renglon[0] == 'Texto') and ('/lib/' in renglon[6]):
					listaMemoria[posicion][0] = 'Bib -> Texto'
				if (renglon[0] == 'Datos') and ('/lib/' in renglon[6]):
					listaMemoria[posicion][0] = 'Bib -> Datos'
		else:
			size, numPages = calcularSize(direcPasada,direcActual)
			renglonNuevo = ['...',direcPasada,direcActual,size,numPages,'----','---Vacio---\n','0m']
			listaMemoria.insert(posicion, renglonNuevo)
			direcPasada = direcActual
		#buscando Heap
		posicion = posicion + 1
	printMemory(listaMemoria)
	
def printMemory(lista):
	print(' Uso            | Dir Inicio    | Dir Fin       | Tamaño   | Num paginas  | Permisos | Uso o mapeo')
	print('/---------------|---------------|---------------|----------|--------------|----------|-----------------------------------')
	for linea in reversed(lista):
		linea = ajustarCadena(linea)
		resul = linea[0] + linea[1] + linea[2] + linea[3] + linea[4] + linea[5] + linea[6]
		print('\033[' + linea[7] + resul + '\033[0m',end='')
	print('---------------/|---------------|---------------|----------|--------------|----------|-----------------------------------')
		
#dependiendo el tamaño del campo, se agregan espacios en blanco
def ajustarCadena(linea):
	linea[0] = ' ' + linea[0] + (15 - len(linea[0]))*' ' + '|'	#mapeo
	linea[1] = ' ' + linea[1][:-3] + (17 - len(linea[1]))*' ' + '|'	#direccion baja
	linea[2] = ' ' + linea[2][:-3] + (17 - len(linea[2]))*' ' + '|'	#direccion alta
	if len(linea[3]) > 7:						#tamaño
		linea[3] = roundSize(linea[3])
	linea[3] = ' ' + linea[3] + (9 - len(linea[3]))*' ' + '|'
	if len(linea[4]) > 13:						#numPaginas
		linea[4] = redondearNumP(linea[4])
	linea[4] = ' ' + linea[4] + (13 - len(linea[4]))*' ' + '|'
	linea[5] = ' ' + linea[5] + ' '*5 + '|'			#permisos
	linea[6] = ' ' + linea[6]
	return linea

#en caso de que el tamaño sobrepase el numero de digitos maximos (10 digitos)
def roundSize(size):
	sizeReducido = size[:-3]
	numSize = float(sizeReducido)
	numSize = round(numSize,2)
	return str(numSize) + size[-3:]

#Si el numero de paginas es inmenso, o sus digitos sobrepasan el maximo (14 digitos)
def redondearNumP(textoNumP):
	numPaginas = float(textoNumP[:-5])
	numReducido = ''
	if numPaginas>9999999:
		exponente = 0
		while (numPaginas)/1000 > 1:
			exponente = exponente + 1
			numPaginas = numPaginas/1000
		numReducido = str(round(numPaginas,2)) + 'E' + str(exponente*3)
	else:
		numReducido = str(round(numPaginas,2))
	return numReducido + ' pags'

#funcion main, en donde se ingresa el PID
def main():
	num_PID = input('Ingrese el numero PID del proceso deseado: ')
	openFile(num_PID)
	
main()

