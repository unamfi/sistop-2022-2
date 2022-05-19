

from columnar import columnar

#para las columnas, los encabezados
headers = [' uso ', ' pagina inicial ', ' página final ', ' bytes ', ' páginas ', ' permiso ', ' mapeo ']

print("\nMEMORIA DE PROCESOS\n # PID para analizar: ", end = "")

proceso = input()

#archivos es la primera lista generada
archivos = []

direccion = "/proc/"+proceso+"/maps"

maps = open(direccion, "r")

for linea in maps:
	linea_separada = linea.split()
	
	#se obtienen las paginas separando por el guion
	paginas = linea_separada[0].split("-") 

	permisos = linea_separada[1]

	if(len(linea_separada) == 6):
		ubicacion = linea_separada[5]  
		
		#si no hay mapeo,es vacio
	else:
		ubicacion = "---- Vacio ----"

	#se quitan los ultimos 3 caracteres que corresponden a los 4096 bytes de cada pagina
	archivos.append([paginas[0][:-3], paginas[1][:-3], permisos, ubicacion]) 

#segunda lista generada a partir de la informacion y donde se identifican las secciones de memoria
lista = []

print("\nLISTA:\n")


for elemento in archivos:

	uso = ""

	if(elemento[3][0] == "/"):

		#para identificar si es libreria
		if(elemento[3][0:4] == "/lib" or elemento[3][0:8] == "/usr/lib"):
			uso = "Lib -> "

		#si es ejecutable
		if(elemento[2][2] == "x"):
			uso = uso + "Texto"
		else:
		# si es texto
			uso = uso + "Datos"

	else:
		#si no es texto ni datos
		uso = elemento[3]

	#se calcula el numero de paginas haciendo una resta
	paginas = int(elemento[1], 16) - int(elemento[0],16)

	lista.append([uso, elemento[0], elemento[1], paginas * 4000, paginas, elemento[2], elemento[3]])



tabla= columnar(lista, headers, no_borders=False)

#se imprime la tabla con ayuda de la libreria columnar

print(tabla)
