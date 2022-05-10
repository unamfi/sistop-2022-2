#Proyecto 3 Memoria
#Autores:
#Davila Ortega Jesus Eduardo
#Espinosa Cortez Giselle

from tkinter import *

bloques = []
mapaMemoria = []

"""
Empieza la programacion de la interfaz grafica
"""
#Creacion de la ventana
ventana = Tk()
PID = StringVar()
num_PID = 0

#Caracteristicas de la ventana
ventana.title("Proyecto 3: Asignacion de memoria en un sistema real")
ventana.resizable(False,False)
ventana.geometry("1100x620")
ventana.config(bg="#000000")

#Cuadro de texto donde se insertara el PID
PID2 = Frame()
PID2.config(bg="#C6AE00", bd=10,relief="groove",width="700", height="100")
PID2.pack(side="top")
Label(PID2,text="Ingrese el PID que se utilizara:", font=("Times New Roman",12)).grid(row=0,column=0)
Entry(PID2,textvariable=PID).grid(row=0,column=1)
Button(PID2,text="Envio",width=7,command=lambda:obtenerPartesMemoria(bloques)).grid(row=0,column=2)

#Ventana que contiene los datos obtenidos.
Informacion = Frame()
Informacion.config(bg="#C6AE00",bd=10,relief="groove",width="700",height="450")
Informacion.pack(side="bottom")

#Cuadro de texto del frame 1, el cual contiene la informacion del mapa
Label(Informacion,text="NEW MAP",font=("Times New Roman",12)).grid(row=0,column=0)
action=Text(Informacion,wrap=NONE,width=100,height=30)
action.grid(row=0,column=0,padx=10,pady=10)

#Barra de desplazamiento para el cuatro de texto con la informacion
#Mejor presentacion de los datos
scrollBarVert = Scrollbar(Informacion,command=action.yview)
scrollBarVert.grid(row=0,column=1,sticky="nsew")
action.config(yscrollcommand=scrollBarVert.set)
scrollBarHor = Scrollbar(Informacion,command=action.xview,orient='horizontal')
scrollBarHor.grid(row=1,column=0,sticky="nsew")
action.config(xscrollcommand=scrollBarHor.set)

#Configurando las etiquetas para el color de los distintos tipos de datos que se mostraran en nuestra interfaz
action.tag_configure('color_direcInicio',foreground='#14BFE2')
action.tag_configure('color_direcFinal',foreground='#E21458')
action.tag_configure('color_tamano',foreground='red')
action.tag_configure('color_pagNumber',foreground='#5400D5')
action.tag_configure('color_permisos',foreground='blue')
action.tag_configure('color_heap',foreground='#3AC056')
action.tag_configure('color_stack',foreground='#900C3F')
action.tag_configure('color_Datos',foreground='#0046F5')
action.tag_configure('color_anonandSyscalls',foreground='#5D0808')
action.tag_configure('color_threedot',foreground='white')
action.tag_configure('color_texto',foreground='#360077')
action.tag_configure('color_pathname',foreground='#EF5A00')
action.tag_configure('color_uso',foreground='#ED12AF')
action.tag_configure('color_kernel',foreground='#07EB90')
action.tag_configure('color_vacio',foreground='#7B8AFF')
action.tag_configure('color_reserva',foreground='#A72050')

"""
Diseño de la clase que albergara la entrada de /proc/<PID>/maps
"""
class ParteMemoria:

	def __init__(self):

		#Informacion obtenida del archivo
		self.direcInicio = ''
		self.direcFinal = ''
		self.privilegios = ''
		self.offset = ''
		self.device = ''
		self.inode = ''
		self.pathname = ''

		#Atributos a imprimir
		self.uso = ''
		self.paginaIni = ''
		self.paginaFin = ''
		self.cantidadPag = 0
		self.tamanoText = ''

	"""
	Método que obtiene los datos a imprimir de cada linea
	"""
	def manejoDatos(self):

		#Quitando el dezplazamiento de las direcciones para obtener la pagina inicial y la pagina final
		self.paginaIni = self.direcInicio[0:len(self.direcInicio)-3]
		self.paginaFin = self.direcFinal[0:len(self.direcFinal)-3]

		#Obteniendo el total de paginas.
		self.cantidadPag = int(self.paginaFin,16) - int(self.paginaIni,16)

		self.tamanoText = ParteMemoria.getTamano(self.cantidadPag)

		#Identificando el uso del bloque
		if('/' in self.pathname):
			if('x' in self.privilegios):
				self.uso = 'Texto'
			elif(not('r' in self.privilegios) and not('w' in self.privilegios)):
				self.uso = 'Reserva'
			else:
				self.uso = 'Datos'
		elif(self.pathname == '[stack]'):
			self.uso = 'Stack'
		elif(self.pathname == '[heap]'):
			self.uso = 'Heap'
		elif(self.pathname == '[anon]'):
			self.uso = 'Mapeo Anon'
		elif(self.pathname == '[vsyscall]'):
			self.uso = 'Sys. Calls'
		elif(self.pathname == '[vdso]'):
			self.uso = 'Sys. Calls'
		elif(self.pathname == '[vvar]'):
			self.uso = 'Kernel Vars.'
		elif(self.pathname == 'Vacio'):
			self.uso = '...'
		else:
			self.uso = self.pathname
			
	
	#Metodo encargado de obtener el tamaño total de una de las partes de nuestra memoria
	def getTamano(cantidadPag):
		tamano = cantidadPag * 4
		unidades = ["KB","MB","GB","TB","PB","EB","ZB","YB","BB"]
		contadorUnidad = 0

		while((tamano/1024) >= 1):
			contadorUnidad += 1
			tamano = tamano/1024

		tamanoText = str(round(tamano,1)) + unidades[contadorUnidad]

		return tamanoText
	#metodo auxiliar utilizado durante el desarrollo del programa para comprobar nuestros resultados.
	def imprimirInfo(self):
		return("|| {:12} || {:16} - {:16} || {:12} || {:12} || {:4} || {}\n".format(self.uso,self.paginaIni,self.paginaFin,self.tamanoText,self.cantidadPag,self.privilegios,self.pathname))

"""
Metodo utilizado para obtener nuestro mapa a partir del comando /proc/[PID]/maps.
"""
def obtenerPartesMemoria(bloques):

	action.delete('1.0',END)
	try:
		pid = PID.get()
	except ValueError:
		action.insert(INSERT,"Valores Incorrectos\n")
	if(int(pid) > 0):
		action.insert(INSERT,"PID: {}\n".format(str(pid)))

		try:
			RutaMapa = '/proc/'+pid+'/maps'
			ArchivoMapa = open(RutaMapa,'r')

			RenglonMapa = ArchivoMapa.readlines()

			#Se procede a leer todas las entradas del archivo
			for line in RenglonMapa:
				parte = ParteMemoria()

				datosPagina = line.split()
				direcIniFin = datosPagina[0].split('-')

				parte.direcInicio = direcIniFin[0]
				parte.direcFinal = direcIniFin[1]
				parte.privilegios = datosPagina[1][0:3]
				parte.offset = datosPagina[2]
				parte.device = datosPagina[3]
				parte.inode = datosPagina[4]

				if(len(datosPagina) > 5):
					parte.pathname = datosPagina[5]
				#Manejo de aquellos partes sin nombre
				else:
					parte.pathname = '[anon]'

				parte.manejoDatos()
				bloques.append(parte)

			if(len(bloques) == 0):
				exit()

		finally:
			ArchivoMapa.close()
			generarMapaMemoria(bloques,mapaMemoria)

"""
Metodo para generar el mapa de memoria desde la lista generada con obtenerPartesMemoria.
Dentro de este metodo se encuentra el codigo que imprime en nuestra interfaz gráfica
"""

def generarMapaMemoria(bloques,mapaMemoria):
	pagLongitud = len(bloques[0].direcInicio)
	#Poniendo la direccion de memoria base
	contadorMemoria = '0'*pagLongitud
	HeapEncontrado = False
	origen = None

	for bloque in bloques:
		if(int(bloque.direcInicio,16)>int(contadorMemoria,16)):

			bloqueAuxiliar = ParteMemoria()
			bloqueAuxiliar.direcInicio = contadorMemoria
			bloqueAuxiliar.direcFinal = bloque.direcInicio
			bloqueAuxiliar.pathname = 'Vacio'
			bloqueAuxiliar.manejoDatos()
			mapaMemoria.append(bloqueAuxiliar)

		if(bloque.uso == 'Heap'):
			HeapEncontrado=True
		if (not HeapEncontrado and '/' in bloque.pathname and origen == None):
			origen = bloque.pathname
		if('/' in bloque.pathname and bloque.pathname != origen):
			HeapEncontrado = True

		if(HeapEncontrado):
			if(bloque.uso == 'Texto'):
				bloque.uso = 'Bib Texto'
			if(bloque.uso == 'Datos'):
				bloque.uso = 'Bib Datos'
		mapaMemoria.append(bloque)
		contadorMemoria = bloque.direcFinal

	#Empezando a imprimir el mapa de memoria en nuestra interfaz
	#Las lineas comentadas de código comentadas fueron usadas durante el desarrollo para comprobar la salida
	#print("|| {:12} || {:16} - {:16} || {:12} || {:12} || {:4} || {}\n".format("Uso","PaginaInicio","PaginaFinal","Tamaño","NumPaginas","Perm","Uso o mapeo"))
	
	#Se imprimen los nombres de cada columna, para saber el significado de las mismas
	action.insert(INSERT,"||")
	action.insert(INSERT," {:12} ".format("Uso"),'color_uso')
	action.insert(INSERT,"||")
	action.insert(INSERT," {:16} ".format("Inicio Pagina"),'color_direcInicio')
	action.insert(INSERT,"-")
	action.insert(INSERT," {:16} ".format("Fin Pagina"),'color_direcFinal')
	action.insert(INSERT,"||")
	action.insert(INSERT," {:15} ".format("Tamaño"),'color_tamano')
	action.insert(INSERT,"||")
	action.insert(INSERT," {:12} ".format("Num Paginas",'color_pagNumber'))
	action.insert(INSERT,"||")
	action.insert(INSERT," {:4} ".format("Perm"),'color_permisos')
	action.insert(INSERT,"||")
	action.insert(INSERT," {} \n".format("Uso o Mapeo", 'color_pathname'))
	
	#Ciclo que pasa por todo nuestro mapa de memoria generado previamente e imprime los valores que se desean obtener.
	for i in reversed(mapaMemoria):
		#print(i.imprimirInfo())
		action.insert(INSERT,"||")
		#Estructura if-elif-else utilizada para dar color a los usos dependiendo de que se trate cada uno
		if(i.uso == 'Heap'):
			action.insert(INSERT," {:12} ".format(i.uso),'color_heap')
		elif(i.uso == 'Bib Texto'):
			action.insert(INSERT," {:12} ".format(i.uso),'color_texto')
		elif(i.uso == 'Bib Datos'):
			action.insert(INSERT," {:12} ".format(i.uso),'color_Datos')
		elif(i.uso == 'Stack'):
			action.insert(INSERT," {:12} ".format(i.uso),'color_stack')
		elif(i.uso == 'Mapeo Anon' or i.uso == 'Sys. Calls'):
			action.insert(INSERT," {:12} ".format(i.uso),'color_anonandSyscalls')
		elif(i.uso == 'Reserva'):
			action.insert(INSERT," {:12} ".format(i.uso),'color_reserva')
		elif(i.uso == 'Kernel Vars'):
			action.insert(INSERT," {:12} ".format(i.uso),'color_kernel')
		else:
			action.insert(INSERT," {:12} ".format(i.uso),'color_vacio')
		action.insert(INSERT,"||")
		action.insert(INSERT," {:16} ".format(i.paginaIni),'color_direcInicio')
		action.insert(INSERT,"-")
		action.insert(INSERT," {:16} ".format(i.paginaFin),'color_direcFinal')
		action.insert(INSERT,"||")
		action.insert(INSERT," {:15} ".format(i.tamanoText),'color_tamano')
		action.insert(INSERT,"||")
		action.insert(INSERT," {:12} ".format(i.cantidadPag),'color_pagNumber')
		action.insert(INSERT,"||")
		action.insert(INSERT," {:4} ".format(i.privilegios),'color_permisos')
		action.insert(INSERT,"||")
		action.insert(INSERT," {} \n".format(i.pathname),'color_pathname')

ventana.mainloop()
