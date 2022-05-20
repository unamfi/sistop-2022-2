# -*- coding: utf-8 -*-
"""
Created on Thu May 16 11:03:46 2022

@author: axel_
"""

import time
import os

	

def enlistarContenido(SistemadeArchivos, ClusterSize):
	print("\nLISTA DE CONTENIDO\n")
	SistemadeArchivos.seek(ClusterSize)

	for i in range(0, ClusterSize * 4, 64):
		SistemadeArchivos.seek(ClusterSize+i)
		archivo = SistemadeArchivos.read(16).decode("utf-8")
		if archivo[:15] != "...............":
			print("\nArchivo:", archivo.strip()[:-1])
			print("Tamanio:",SistemadeArchivos.read(9).decode("utf-8")[:-1]," Cluster inicial:",SistemadeArchivos.read(6).decode("utf-8")[:-1])

def encontrarArchivo(archivoaEncontrar, SistemadeArchivos, ClusterSize):

	#se posisciona en el cluster del directorio
	SistemadeArchivos.seek(ClusterSize)

	#recorre las entradas del directorio
	for i in range(0, ClusterSize * 4, 64):
		SistemadeArchivos.seek(ClusterSize+i)
		#se le asigna los datos leidos correspondiente al nombre quitando un caracter nulo al final
		archivo = SistemadeArchivos.read(16).decode("utf-8").strip()[:-1]
		if archivo == archivoaEncontrar:

			tamanioArchivo = int(SistemadeArchivos.read(9).decode("utf-8")[:-1])
			clusterInicial = int(SistemadeArchivos.read(6).decode("utf-8")[:-1])

			return (tamanioArchivo, clusterInicial)
		
	return (0,0)


def copiaraSistema(SistemadeArchivos, ClusterSize):
	print("\nCOPIAR HACIA SISTEMA\n")

	archivoaCopiar = input("\nIngrese nombre del archivo a copiar al sistema:")

	datos_archivo = encontrarArchivo(archivoaCopiar, SistemadeArchivos, ClusterSize)

	#se asignan los datos correspondientes de la tupla
	tamanioArchivo = datos_archivo[0]
	clusterInicial = datos_archivo[1]

	#si no tiene tamano ni cluster inicial no existe
	if tamanioArchivo == 0 and clusterInicial == 0:
		print("\nEl archivo no se encontro en FiUnamFs")

	else:

		print("\nse encontró el Archivo:", archivoaCopiar)
		print("Tamaño:", tamanioArchivo," Cluster inicial:", clusterInicial)

		nuevo_archivo = open("(del SSAA)"+archivoaCopiar,"wb")

		SistemadeArchivos.seek(ClusterSize * clusterInicial)
		nuevo_archivo.write(SistemadeArchivos.read(tamanioArchivo))

		nuevo_archivo.close()

		print("\n¡Archivo copiado a sistema con exito!")

def dirClusterSig(clusterInicial, tamanioArchivo, ClusterSize):
	sobrante = tamanioArchivo%ClusterSize
	valorAaumentar = 2048 - sobrante

	return (clusterInicial) * 2048 + tamanioArchivo + valorAaumentar


def obtenerEspacioDirectorio(SistemadeArchivos, ClusterSize):
	SistemadeArchivos.seek(ClusterSize)

	for i in range(0, ClusterSize * 4, 64):
		SistemadeArchivos.seek(ClusterSize+i)
		archivo = SistemadeArchivos.read(16).decode("utf-8")
		if archivo[:15] == "...............":
			return ClusterSize + i

	return -1


def obtenerClusterDisp(tamano_de_archivoaCopiar, SistemadeArchivos, ClusterSize, SistemadeArchivosSize):
	SistemadeArchivos.seek(ClusterSize)
	datosArchivos = []
	for i in range(0, ClusterSize * 4, 64):
		SistemadeArchivos.seek(ClusterSize+i)

		archivo = SistemadeArchivos.read(16).decode("utf-8").strip()[:-1]

		if archivo[:15] != "...............":
			tamanioArchivo = int(SistemadeArchivos.read(9).decode("utf-8")[:-1])
			clusterInicial = int(SistemadeArchivos.read(6).decode("utf-8")[:-1])

			#se agrega a una lista donde se contienen los datos de los archivos
			datosArchivos.append((clusterInicial,tamanioArchivo))

	
	#se ordenan los datos esenciales de los archivos con respecto a su cluster inicial
	datosArchivos = sorted(datosArchivos, key=lambda x: x[0])

	for i in range(0,len(datosArchivos)):

		dirClusterSiguiente = dirClusterSig(datosArchivos[i][0], datosArchivos[i][1], ClusterSize)

		#si son los ultimos datos de los archivos la comparacion es con el tamaño del archivo 
		if i == len(datosArchivos)-1:
			espacio_libre = SistemadeArchivosSize - dirClusterSiguiente
		#si no entonces la comparacion es con el archivo siguiente
		else:
			dir_cluster_archivo_siguiente = datosArchivos[i+1][0] * 2048
			espacio_libre = dir_cluster_archivo_siguiente - dirClusterSiguiente

		if espacio_libre >= tamano_de_archivoaCopiar:
			return dirClusterSiguiente
	return -1
			

def elimDeFIunamFS(SistemadeArchivos, ClusterSize):
	print("\nELIMINAR DE FIUNAMFS\n")

	archivoAeliminar = input("Ingrese nombre del archivo a eliminar: ")

	SistemadeArchivos.seek(ClusterSize)

	#recorre las entradas del directorio
	for i in range(0, ClusterSize * 4, 64):
		SistemadeArchivos.seek(ClusterSize+i)
        
		#quitando un caracter nulo al final
        
		archivo = SistemadeArchivos.read(16).decode("utf-8").strip()[:-1]
		if archivo == archivoAeliminar:
			SistemadeArchivos.seek(ClusterSize+i)
			SistemadeArchivos.write("...............".encode("utf-8"))

			print("\n¡Archivo eliminado de FiUnamFs con exito!")
			return

	print("\nEl archivo no se encontro en FiUnamFs")

def copiarAFiunamfs(SistemadeArchivos, SistemadeArchivosSize, ClusterSize):
	print("\ncopiar hacia FiUnamFS\n")
	archivoaCopiar = input("\nIngrese nombre de archivo a copiar: ")

	if len(archivoaCopiar) > 15:
		print("\nel nombre sobrepasa los 15 caracteres, intenta de nuevo" )
		return

	if os.path.isfile(archivoaCopiar) == False:
		print("\nEl archivo no existe, intenta de nuevo.")
		return
	#se obtienen los datos esenciales del archivo y se ponen en una tupla
	datos_archivo = encontrarArchivo(archivoaCopiar, SistemadeArchivos, ClusterSize)

	#se obtienen los datos de la tupla
	tamanioArchivo = datos_archivo[0]
	clusterInicial = datos_archivo[1]

	if tamanioArchivo == 0 and clusterInicial == 0:
		
		tamanioArchivoaCopiar = os.stat(archivoaCopiar).st_size

		print("\nTamaño de archivo:", tamanioArchivoaCopiar)

		direccion = obtenerEspacioDirectorio(SistemadeArchivos, ClusterSize)

		if direccion == -1:
			print("\nEl directorio no tiene suficiente espacio para almacenar tu archivo")
			return

		dirClusterDisponible = obtenerClusterDisp(tamanioArchivoaCopiar, SistemadeArchivos, ClusterSize, SistemadeArchivosSize)

		if dirClusterDisponible == -1:
			print("\nEl archivo no cabe en FiUnamFS")
			return

		SistemadeArchivos.seek(direccion)
		SistemadeArchivos.write("                ".encode("utf-8"))
		SistemadeArchivos.seek(direccion)
		archivoaCopiar = archivoaCopiar + "."
		SistemadeArchivos.write(archivoaCopiar.encode("utf-8"))


		SistemadeArchivos.seek(direccion+16)
		SistemadeArchivos.write("000000000".encode("utf-8"))
		str_tamanioArchivoaCopiar = str(tamanioArchivoaCopiar)
		str_tamanioArchivoaCopiar = str_tamanioArchivoaCopiar + "."
		numeroCeros = 9 - len(str_tamanioArchivoaCopiar)
		SistemadeArchivos.seek(direccion + 16 + numeroCeros)
		SistemadeArchivos.write(str_tamanioArchivoaCopiar.encode("utf-8"))


		SistemadeArchivos.seek(direccion+25)
		SistemadeArchivos.write("000000".encode("utf-8"))
		cluster_disponible = int(dirClusterDisponible / 2048)
		str_cluster_disponible= str(cluster_disponible)
		str_cluster_disponible = str_cluster_disponible + "."
		numeroCeros = 6 - len(str_cluster_disponible)
		SistemadeArchivos.seek(direccion + 25 + numeroCeros)
		SistemadeArchivos.write(str_cluster_disponible.encode("utf-8"))

		
		SistemadeArchivos.seek(direccion+31)
		str_fecha = str(time.localtime().tm_year) + str(time.localtime().tm_mon).zfill(2) + str(time.localtime().tm_mday).zfill(2) + str(time.localtime().tm_hour).zfill(2) + str(time.localtime().tm_min).zfill(2) + str(time.localtime().tm_sec).zfill(2)
		str_fecha = str_fecha + "."
		SistemadeArchivos.write(str_fecha.encode("utf-8"))


		SistemadeArchivos.seek(direccion+46)
		SistemadeArchivos.write(str_fecha.encode("utf-8"))


		contenidoArchivo = open(archivoaCopiar[:-1], "r+b")
		SistemadeArchivos.seek(dirClusterDisponible)
		for elemento in contenidoArchivo:
			SistemadeArchivos.write(elemento)

		print("\nArchivo copiado a FiUnamFs\n")

		


	else:

		print("\nEl archivo ya existe, intenta de nuevo")
			
def main():

	tamanioSector = 512
	ClusterSize = tamanioSector * 4

	SistemadeArchivos = open("fiunamfs.img", "r+b")

	print("\nFiUnamFs.img\n")

	SistemadeArchivos.seek(0)
	print("Nombre de sistema de archivos:", SistemadeArchivos.read(9).decode("utf-8"))
	print("Versión de la implementación:", SistemadeArchivos.read(4).decode("utf-8"))
	SistemadeArchivos.seek(20)
	print("Etiqueta del volumen:", SistemadeArchivos.read(16).decode("utf-8"))
	SistemadeArchivos.seek(40)
	print("Tamaño del cluster en bytes:", SistemadeArchivos.read(6).decode("utf-8"))
	SistemadeArchivos.seek(47)
	print("Número de clusters del directorio:", SistemadeArchivos.read(3).decode("utf-8"))
	SistemadeArchivos.seek(52)
	print("Número de clusters de la unidad completa:", SistemadeArchivos.read(9).decode("utf-8"))

	opcion = ""

	#while para hacer dinamico el programa 
	while(opcion != "5"):

		#reiniciar para mostrar cambios
		SistemadeArchivos = open("fiunamfs.img", "r+b")

		SistemadeArchivosSize = os.stat("fiunamfs.img").st_size

		print("\nMENU\n")
		print("1. lista del contenido en el sistema de archivos")
		print("2. Copiar archivo de FiUnamFS hacia sistema")
		print("3. Copiar archivo dl sistema hacia FiUnamFS")
		print("4. Eliminar archivo de FiUnamFS")
		print("5. Cerrar")
        
		opcion = input("\n\ningresa lo que quieras que haga el programa: ")

		if opcion == "1":
            #llama a la funcion para listar el contenido del sistema de archivos
			enlistarContenido(SistemadeArchivos, ClusterSize)

		elif opcion == "2":
            #llama a la funcion para copiar hacia nuestro sistema
			copiaraSistema(SistemadeArchivos, ClusterSize)

		elif opcion == "3":
            
			copiarAFiunamfs(SistemadeArchivos, SistemadeArchivosSize, ClusterSize)

		elif opcion == "4":
            
			elimDeFIunamFS(SistemadeArchivos, ClusterSize)

		#se cierra el ssaa 
		SistemadeArchivos.close()

main()
