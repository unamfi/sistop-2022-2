import os
from datetime import datetime
import math

microsistema = open('fiunamfs.img', 'r+b')

lectura = microsistema.read(60).decode('utf-8')

tamanio = int(lectura[40:46].rstrip('\x00'))
clus_directorio = int(lectura[47:50].rstrip('\x00'))
clus_unidad = int(lectura[52:].rstrip('\x00'))

print('Identificación:', lectura[0:8])
print('Versión:', lectura[10:14])
print('Etiqueta:', lectura[20:36])
print('Tamaño cluster:', tamanio)
print('Núm. de clusters directorio:', clus_directorio)
print('Núm. de clusters unidad:', clus_unidad)

num_archivos = int(clus_directorio * 8 * 256 / 64)

def info_archivos(): 
	"""
	0: nombre
	1: tamaño en bytes
	2: cluster inicial
	3: año de creación
	4: mes de creación
	5: día de creación
	6: hora de creación
	7: minuto de creación
	8: último ocupado 
	9: segundos de creación
	"""
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

	#lista = sorted(lista, key=lambda x:x[2])
	
	return lista

def enlistar_archivos():
	lista = info_archivos()

	for elemento in lista:
		print('{}		{}	B		{}-{}		{}-{}-{}		{}:{}'.format(
			elemento[0], elemento[1], elemento[2], elemento[8], elemento[3], elemento[4], elemento[5], elemento[6], elemento[7]))
			

def copiar_archivo_sistema():
	nombre_copia = input('Ingrese el nombre del archivo nuevo: ')
	nombre_original = input('Ingrese el nombre del archivo a copiar: ')

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
		print('Archivo copiado.')
	else:
		print('El archivo no existe.')

def copiar_sistema_archivo():
	nombre_original = input('Ingrese el nombre del archivo a copiar: ')
	try: 
		archivo_original = open(nombre_original, 'rb')
		nuevo_tamanio = os.stat(nombre_original).st_size
		lectura_original = archivo_original.read()

		nombre_copia = input('Ingrese el nombre del archivo nuevo: ')

		lista = info_archivos()
		lista = sorted(lista, key=lambda x:x[2])

		espacio = []
		for i in range(len(lista)-1):
			espacio.append((lista[i+1][2] - lista[i][8]) * tamanio)

		for i in range(len(espacio)):
			if nuevo_tamanio < espacio[i] :
				sig_cluster = lista[i][8] + 1
				break
			sig_cluster = lista[-1][8] + 1

		microsistema.seek(sig_cluster * tamanio)
		microsistema.write(lectura_original)

		archivo_original.close()

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
		print('Archivo copiado.')
	except FileNotFoundError:
		print('El archivo indicado no existe.')

def eliminar_archivo():
	nombre_eliminar = input('Ingrese el nombre del archivo a eliminar: ')

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
		print('Archivo eliminado.')
	else: 
		print('El archivo indicado no existe.')

def desfragmentar():
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

opcion = 9808790848908094832908490230

while opcion != 6:

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
		print('Listando los contenidos del directorio.')
		enlistar_archivos()
	elif opcion == 2:
		copiar_archivo_sistema()
	elif opcion == 3:
		copiar_sistema_archivo()
	elif opcion == 4:
		eliminar_archivo()
	elif opcion == 5:
		desfragmentar()
		print('Desfragmentado.')
	elif opcion == 6:
		print('Ejecución terminada.')
	else:
		#microsistema.seek(2048 + 19)
		#microsistema.write('24576'.encode('utf-8'))
		print('Opción no válida')

microsistema.close()