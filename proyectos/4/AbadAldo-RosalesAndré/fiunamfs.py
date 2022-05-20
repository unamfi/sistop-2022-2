#!/usr/bin/python3

import os, sys, struct
from getpass import getuser

class FiUnamFS:
	def __init__(self): 
		self.sector_size = 512	# La superficie del disco se divide en sectores de 256 bytes
		self.cluster = self.sector_size * 4	# Cada cluster mide cuatro sectores
		self.file_system = open('fiunamfs.img','r+b')	# Archivo abierto para su lectura en modo binario; error si el archivo no existe
		self.name_length = 16

	''' Listar los contenidos del directorio '''
	def ls(self):
		self.file_system.seek(0)
		files = []
		for i in range(0, self.cluster * 4, 64):
			self.file_system.seek(self.cluster + i)
			file_name = self.file_system.read(self.name_length - 1)
			if file_name != b'Xx.xXx.xXx.xXx.':
				files.append(file_name)

		for fil in files:
			print(fil.decode())
		self.file_system.seek(0)

	''' Copiar de FiUnamFS al sistema '''
	def cp_fi(self, name, path):
		for i in range(0, self.cluster * 4, 64):
			self.file_system.seek(self.cluster + i)
			file_name = self.file_system.read(self.name_length - 1)
			self.file_system.read(1)
			if file_name.decode().strip() == name:
				length = struct.unpack('<L', self.file_system.read(4))[0]
				start = struct.unpack('<L', self.file_system.read(4))[0]
				self.file_system.seek(self.cluster * start)
				data = self.file_system.read(length)

				written_file = open(path+"/"+file_name.decode().strip(),"wb")
				written_file.write(data)
				written_file.close()
				break
		if i == (63 * 64):
			print("'" + archivo + " no se encontró en FiUnamFS.\n")

	''' Copiar del sistema a FiUnamFS '''
	#def cp_sys()


	''' Eliminar archivo de FiUnamFS '''
	def rm(self, archivo):
		for i in range(0, self.cluster * 4, 64):
			self.file_system.seek(self.cluster + i)
			file_name = self.file_system.read(self.name_length - 1)
			if file_name.decode().strip() == archivo:
				self.file_system.seek(self.cluster + i)
				self.file_system.write(('Xx.xXx.xXx.xXx.').encode())
				print("Archivo eliminado de FiUnamFS exitosamente.\n")
				break
		if i == (63 * 64):
			print("'" + archivo + " no se encontró en FiUnamFS.\n")

	''' Desfragmentación '''
	def defrag(self):
		initial_clusters = []
		file_lengths = []
		file_names = []
		for i in range(0, self.cluster * 4, 64):
			self.file_system.seek(self.cluster + i)
			file_name = self.file_system.read(self.name_length - 1)
			self.file_system.read(1)
			length = self.file_system.read(4)
			start = self.file_system.read(4)
			if file_name != b'Xx.xXx.xXx.xXx.':
				file_names.append(file_name)
				initial_clusters.append(struct.unpack('<l', start)[0])
				file_lengths.append(struct.unpack('<l', length)[0])
		sorted_file_names = [x for y, x in sorted(zip(initial_clusters, file_names))]
		sorted_file_lengths = [x for y, x in sorted(zip(initial_clusters, file_lengths))]
		sorted_initial_clusters = sorted(initial_clusters)

		new_initial_clusters = []
		new_initial_clusters.append(5)
		for i in range(1, len(sorted_initial_clusters)):
			if sorted_file_lengths[i - 1] <= 1024:
				size = 2
			else:
				size = (sorted_file_lengths[i - 1] // 1024) + 2
				if sorted_file_lengths[i - 1] % 1024 == 0:
					size -=1
				new_initial_clusters.append(new_initial_clusters[i - 1] + size)

		for i in range(0, len(new_initial_clusters)):
			self.file_system.seek(sorted_initial_clusters[i] * self.cluster)
			data = self.file_system.read(sorted_file_lengths[i])
			self.file_system.seek(new_initial_clusters[i] * self.cluster)
			self.file_system.write(data)
		for i in range(0, len(sorted_file_names)):
			for j in range(0, self.cluster * 4, 64):
				self.file_system.seek(self.cluster + j)
				file_name = self.file_system.read(self.name_length - 1)
				self.file_system.read(5)
				if file_name == sorted_file_names[i]:
					self.file_system.write(struct.pack('<L', new_initial_clusters[i]))				

	''' Menú '''
	def help(self):
		print("\n _ _ _ _ _ _ _ _ _ Comandos del Sistema _ _ _ _ _ _ _ _ _\n")
		print("| help                -> Desplegar menú de ayuda         |\n");
		print("| ls                  -> Listar contenido del directorio |\n");
		print("| cp «archivo» «ruta» -> Copiar archivo                  |\n");
		print("| rm «nombre_archivo» -> Eliminar archivo de FiUnamFS    |\n");
		print("| defrag              -> Desfragmentar FiUnamFS          |\n");
		print("| exit                -> Salir de FiUnamFS               |\n");
		print("|________________________________________________________|\n");

	def action(self, command):
		command = command.split()
		if command[0] == "help":
			if len(command) == 1:
				self.help()
			else:
				print("Este comando no requiere argumentos.\n")

		elif command[0] == "ls":
			if len(command) == 1:
				self.ls()
			else:
				print("Este comando no requiere argumentos.\n")

		elif command[0] == "cp":
			if len(command) == 3:
				self.cp_fi(command[1], command[2])
			elif len(command) < 3:
				print("Este comando requiere de los siguientes argumentos: «archivo» «ruta».\n")
			else:
				print("Este comando sólo requiere los argumentos: «archivo» «ruta».\n")

		elif command[0] == "rm":
			if len(command) == 2:
				self.rm(command[1])
			elif len(command) < 2:
				print("Este comando requiere del siguiente argumento: «nombre_archivo».\n")
			else:
				print("Este comando sólo requiere el argumento: «nombre_archivo».\n")

		elif command[0] == "defrag":
			if len(command) == 1:
				self.defrag()
			else:
				print("Este comando no requiere argumentos.\n")

		elif command[0] == "exit":
			if len(command) == 1:
				self.file_system.close()
 	   			#break	# Creo que esto no jala xD
			else:
				print("Este comando no requiere argumentos.\n")

		else:
			print("'" + command + "' no se reconoce como un comando interno o externo, programa o archivo por lotes ejecutable.\n")

	def execution(self):
		print("Use el comando 'help' para conocer el menú de comandos.\n")
		user = getuser()
		while True:
			entrada = input("[" + user + "@FiUnamFS]:~$ ")
			self.action(entrada)
			if entrada == "exit":
				break

if __name__ == '__main__':
	FileSystem = FiUnamFS()
	FileSystem.execution()