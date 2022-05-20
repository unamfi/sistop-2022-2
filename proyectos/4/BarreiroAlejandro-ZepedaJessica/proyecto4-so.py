'''Proyecto 4: (Micro) Sistema de Archivos
Realizado por Alejandro Barreiro y Jessica Zepeda
Sistemas Operativos 2022-2'''

import os
from datetime import datetime
import math

microsistema = open('fiunamfs.img', 'r+b')

#Se obtiene la información del superbloque y se muestra.
lectura = microsistema.read(60).decode('utf-8')

tamanio = int(lectura[40:46].rstrip('\x00'))
clus_directorio = int(lectura[47:50].rstrip('\x00'))
clus_unidad = int(lectura[52:].rstrip('\x00'))

print('\n\033[1m----------Microsistema de archivos----------\033[0m\n')
print('\033[1m{:<28}	{:15}'.format('Identificación:\033[0m', lectura[0:8]))
print('\033[1m{:<28}	{:15}'.format('Versión:\033[0m', lectura[10:14]))
print('\033[1m{:<28}	{:15}'.format('Etiqueta:\033[0m', lectura[20:36]))
print('\033[1m{:<28}	{:5}'.format('Tamaño cluster:\033[0m', tamanio))
print('\033[1m{:<28}	{:5}'.format('Núm. de clusters directorio:\033[0m', clus_directorio))
print('\033[1m{:<28}	{:5}'.format('Núm. de clusters unidad:\033[0m', clus_unidad))

num_archivos = int(clus_directorio * 8 * 256 / 64)

'''Función que lee todos los archivos o líneas en el directorio y almacena en una lista los archivos existentes.
   Regresa una lista donde cada elemento es una lista de la información de un archivo.
   La información que almacena cada índice es: 
		0: nombre
		1: tamaño en bytes
		2: cluster inicial
		3: año de creación
		4: mes de creación
		5: día de creación
		6: hora de creación
		7: minuto de creación
		8: clúster final 
		9: segundos de creación
	'''
def info_archivos(): 
	lista = []
	direccion = tamanio

	for i in range(num_archivos):
		microsistema.seek(direccion)
		lectura_enlistar = microsistema.read(64).decode('utf-8')
		if lectura_enlistar[0:16] != '...............\x00':
			lista_anidada = []
			lista_anidada.append(lectura_enlistar[0:16].rstrip('\x00').lstrip(' '))
			lista_anidada.append(int(lectura_enlistar[16:25].rstrip('\x00')))
			lista_anidada.append(int(lectura_enlistar[25:31].rstrip('\x00')))
			lista_anidada.append(lectura_enlistar[31:35])
			lista_anidada.append(lectura_enlistar[35:37])
			lista_anidada.append(lectura_enlistar[37:39])
			lista_anidada.append(lectura_enlistar[39:41])
			lista_anidada.append(lectura_enlistar[41:43])
			lista_anidada.append(math.ceil(lista_anidada[1] / 2048 + lista_anidada[2]))
			lista_anidada.append(lectura_enlistar[43:45])
			lista.append(lista_anidada)
		direccion += 64
	
	return lista

'''Función que muestra la información de los archivos existentes utiliando la lista regresada por la función info_archivos'''
def enlistar_archivos():
	lista = info_archivos()

	for elemento in lista:
		print('{:<20}	{:<8}B	{:4} -{:4}	{:4}-{:2}-{:2}	{:2}:{:2}'.format(
			elemento[0], elemento[1], elemento[2], elemento[8], elemento[3], elemento[4], elemento[5], elemento[6], elemento[7]))
			

'''Función que copia un archivo de FiUnamFS al sistema'''
def copiar_archivo_sistema():
	nombre_copia = input('\nIngrese el nombre del archivo nuevo:    ')
	nombre_original = input('Ingrese el nombre del archivo a copiar:    ')

	'''Se obtienen los archivos existentes y se busca el nombre ingresado por el usuario. 
	   En caso de no encontrarse el valor de cluster_inicial será -1 y se indicará que el archivo no existe.
	   En caso de encontrarse se lee todo el contenido del archivo y se escribe en uno nuevo con el nombre ingresado.'''
	lista = info_archivos()

	cluster_inicial = -1
	for elemento in lista:
		if elemento[0] == nombre_original:
			tamanio_archivo = elemento[1]
			cluster_inicial = elemento[2]
			break

	if cluster_inicial != -1:
		microsistema.seek(cluster_inicial * tamanio)
		lectura = microsistema.read(tamanio_archivo)

		archivo_copia = open(nombre_copia, 'wb')
		archivo_copia.write(lectura)
		archivo_copia.close()
		print('\nArchivo copiado.')
	else:
		print('\nEl archivo no existe.')

'''Función que copia un archivo del sistema hacia FiUnamFS además de agregar la información del archivo en el directorio'''
def copiar_sistema_archivo():
	nombre_original = input('\nIngrese el nombre del archivo a copiar:    ')

	'''Se intenta leer el archivo indicado, en caso de no existir se lanza una excepción y se indica que no existe.'''
	try: 
		archivo_original = open(nombre_original, 'rb')
		nuevo_tamanio = os.stat(nombre_original).st_size
		lectura_original = archivo_original.read()

		nombre_copia = input('Ingrese el nombre del archivo nuevo:    ')

		'''Se obtienen los archivos ya existentes y se ordenan ascendentemente de acuerdo al cluster inicial 
		   para calcular el espacio entre archivos contiguos.'''
		lista = info_archivos()
		lista = sorted(lista, key=lambda x:x[2])

		espacio = []
		for i in range(len(lista)-1):
			#Se resta uno ya que en caso de que sean clusteres contiguos no se tiene espacio pero la resta daría 1
			espacio.append((lista[i+1][2] - lista[i][8] - 1) * tamanio)

		'''Si se encuentra un espacio suficientemente grande para colocar el nuevo archivo se guarda el valor del 
		   siguiente cluster disponible. Si no se encuentra el espacio, se guarda el cluster siguiente al último 
		   ocupado por el último archivo.'''
		for i in range(len(espacio)):
			if nuevo_tamanio < espacio[i] :
				sig_cluster = lista[i][8] + 1
				break
			sig_cluster = lista[-1][8] + 1

		microsistema.seek(sig_cluster * tamanio)
		microsistema.write(lectura_original)

		archivo_original.close()

		'''Se crea la cadena de información que va en el directorio con el nombre indicado y la fecha actual.
		   La cadena se guarda en el primer espacio sin información en el directorio'''
		nuevo_directorio = (nombre_copia.rjust(15,' ') + '\x00' + str(nuevo_tamanio).rjust(8,'0') 
			+ '\x00' + str(sig_cluster).rjust(5,'0') + '\x00' + datetime.now().strftime('%Y%m%d%H%M%S')
			+ '\x00' + datetime.now().strftime('%Y%m%d%H%M%S') + '\x00' + '\x00' + '\x00' + '\x00').encode('utf-8')
		
		direccion = tamanio
		for i in range(num_archivos):
			microsistema.seek(direccion)
			lectura_enlistar = microsistema.read(64).decode('utf-8')
			if lectura_enlistar[0:16] == '...............\x00':
				microsistema.seek(direccion)
				microsistema.write(nuevo_directorio)
				break
			direccion += 64
		print('\nArchivo copiado.')
	
	except FileNotFoundError:
		print('\nEl archivo indicado no existe.')

'''Función que elimina un archivo de FiUnamFS'''
def eliminar_archivo():
	nombre_eliminar = input('\nIngrese el nombre del archivo a eliminar:    ')

	'''Se obtienen los archivos existentes y se busca el nombre ingresado por el usuario. 
	   En caso de no encontrarse el valor de cluster_inicial será -1 y se indicará que el archivo no existe.
	   En caso de encontrarse se escribe el caracter \00x en cada byte ocupado por el archivo, se recorre el directorio
	   hasta encontrar el nombre y se sustituyen los 64 bytes por la cadena "vacía"'''
	lista = info_archivos()

	cluster_inicial = -1
	for elemento in lista:
		if elemento[0] == nombre_eliminar:
			tamanio_archivo = elemento[1]
			cluster_inicial = elemento[2]
			break

	if cluster_inicial != -1:
		microsistema.seek(cluster_inicial * tamanio)
		for i in range(tamanio_archivo):
			microsistema.write(('\x00').encode('utf-8'))

		directorio_vacio = ('...............\x0000000000\x0000000\x0000000000000000\x0000000000000000\x00\x00\x00\x00').encode('utf-8')

		direccion = tamanio
		for i in range(num_archivos):
			microsistema.seek(direccion)
			lectura_enlistar = microsistema.read(64).decode('utf-8')
			if lectura_enlistar[0:16].lstrip(' ').rstrip('\x00') == nombre_eliminar:
				microsistema.seek(direccion)
				microsistema.write(directorio_vacio)
				break
			direccion += 64
		print('\nArchivo eliminado.')
	
	else: 
		print('\nEl archivo indicado no existe.')

'''Función que desfragmenta FiUnamFS.'''
def desfragmentar():
	'''Se obtienen los archivos ya existentes y se ordenan ascendentemente de acuerdo al cluster inicial. Se verifica si el 
	   cluster incial y final de cada dos archivos no son contiguos. Si es así, se lee todo el archivo "posterior", se borra 
	   su contenido y se escribe en el siguiente cluster del final del archivo anterior.'''
	lista = info_archivos()
	lista = sorted(lista, key=lambda x:x[2])

	for i in range(len(lista)-1):
		if lista[i+1][2] - lista[i][8] > 1:
			microsistema.seek(lista[i+1][2] * tamanio)
			lectura_defrag = microsistema.read(lista[i+1][1])

			microsistema.seek(lista[i+1][2] * tamanio)
			for j in range(lista[i+1][1]):
				microsistema.write(('\x00').encode('utf-8'))

			microsistema.seek((lista[i][8] + 1) * tamanio)
			microsistema.write(lectura_defrag)

			'''Se hace una cadena con la actualización de cluster final y fecha de modificación del archivo recorrido.
			   Se busca el archivo en el directorio y se actualiza la información.'''
			modificaciones = (str(lista[i][8] + 1).rjust(5,'0') + '\x00' + lista[i+1][3] + lista[i+1][4] + lista[i+1][5]
				+ lista[i+1][6] + lista[i+1][7] + lista[i+1][9] + '\x00' + datetime.now().strftime('%Y%m%d%H%M%S')).encode('utf-8')

			direccion = tamanio
			for j in range(num_archivos):
				microsistema.seek(direccion)
				lectura_enlistar = microsistema.read(64).decode('utf-8')
				if lectura_enlistar[0:16].lstrip(' ').rstrip('\x00') == lista[i+1][0]:
					microsistema.seek(direccion + 25)
					microsistema.write(modificaciones)
					break
				direccion += 64

'''Menú principal
   La opción 7 está escondida y corrige la imagen del sistema inicial ya que hay un traslape entre logo.png y README.org'''
opcion = 9808790848908094832908490230

while opcion != 6:

	print('\n\033[1m--------------Menú de opciones--------------\033[0m')
	print('''\nSelecciona una opción:
1. Listar los contenidos del directorio
2. Copiar uno de los archivos de dentro del FiUnamFS hacia tu sistema
3. Copiar un archivo de tu computadora hacia tu FiUnamFS
4. Eliminar un archivo del FiUnamFS
5. Desfragmentar
6. Salir
	''')

	opcion = int(input('Ingrese la opción: '))

	if opcion == 1:
		print('\nListando los contenidos del directorio...\n')
		enlistar_archivos()
	elif opcion == 2:
		copiar_archivo_sistema()
	elif opcion == 3:
		copiar_sistema_archivo()
	elif opcion == 4:
		eliminar_archivo()
	elif opcion == 5:
		desfragmentar()
		print('\nDesfragmentado.')
	elif opcion == 6:
		print('\nEjecución terminada.')
	elif opcion == 7:
		microsistema.seek(2048 + 19)
		microsistema.write('24576'.encode('utf-8'))
		print('\nOpción no válida')
	else:
		print('\nOpción no válida')

microsistema.close()