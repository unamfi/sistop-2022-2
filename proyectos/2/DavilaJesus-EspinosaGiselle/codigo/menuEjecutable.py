import curses
import time
import codigoFuncionamiento as pro2
import interfaz as inte
import threading

def menu():
	#Inicializacion de la pantalla
	#Obtencion de medidas de la consola
	scr = curses.initscr()
	curses.noecho()
	dims = scr.getmaxyx()

	hilosEjecucion = False

	q = -1
	while q != 113 and q != 81:

		scr.nodelay(1)
		q = scr.getch()

		scr.clear()
		# Formacion de la pantalla de titulo
		scr.addstr(1,dims[1]-24, 'Presione \'q\' para salir')
		scr.addstr(2,(dims[1]-50)//2, ' ______    __           ______   _______      ______     ______   _______      _______    __         __   _______    _____      ______    _______    ')
		scr.addstr(3,(dims[1]-50)//2, '|  ____|  |  |         |   _  \\ |   _  \\     /      \\   /  ____| |   _  \\     /   _   \\  |  \\       /  | /   _   \\  |    \\     /      \\  |   _  \\    ')
		scr.addstr(4,(dims[1]-50)//2, '| |____   |  |         |  |_| | |  |_|  /   |    _   | |  /  ___ |  |_|  /    |  |_|   | |   \\     /   | |  |_|   | |  _  \\  |    _   | |  |_|  /   ')
		scr.addstr(5,(dims[1]-50)//2, '|  ____|  |  |         |  ___/  |  |\\   \\   |   |_|  | |  | |__ ||  |\\   \\    |   __   | |    \\ __/    | |   __   | | |_|   | |   |_|  | |  |\\   \\   ')
		scr.addstr(6,(dims[1]-50)//2, '| |____   |  |____     |  |     |  | \\   \\  \\        / \\ \\ ___/ /|  | \\   \\   |  |  |  | |  |\\ ____/|  | |  |  |  | |      /  \\        / |  | \\   \\  ')
		scr.addstr(7,(dims[1]-50)//2, '|______|  |_______|    |__|     |__|  \\ __\\  \\ _____/   \\ _____/ |__|  \\ __\\  |__|  |__| |__|       |__| |__|  |__| |_____/    \\ _____/  |__|  \\ __\\ ')

		scr.addstr(8,(dims[1]-60)//2, ' __        __   _______    __       ______   ______   ______    ______    _____    ______  ')
		scr.addstr(9,(dims[1]-60)//2, '|  \\      /  | /   _    \\ |  |     |_    _| /   ___| |_    _|  /      \\  |  ___|  /       \\')
		scr.addstr(10,(dims[1]-60)//2,'|   \\    /   | |  |_|   | |  |       |  |   |  /       |  |   |    _   | | |___  |    _    |')
		scr.addstr(11,(dims[1]-60)//2,'|    \\__/    | |   __   | |  |       |  |   |  |       |  |   |   |_|  | |___  | |   |_|   |')
		scr.addstr(12,(dims[1]-60)//2,'|  |\\____/|  | |  |  |  | |  |____  _|  |_  |  \\___   _|  |_  \\        /  ___| | \\        /')
		scr.addstr(13,(dims[1]-60)//2,'|__|      |__| |__|  |__| |_______||______| \\ _____| |______|  \\ _____/  |_____|  \\ _____/')

		scr.addstr(16,(dims[1]-15)//2,'1. El problema')
		scr.addstr(18,(dims[1]-15)//2,'2. Ejecucion visual')
		scr.refresh()

		s = -1

		# 1. El problema
		if q == 49:
			scr.clear()
			scr.nodelay(1)

			# Mostramos la descripcion del problema
			while s != 115 and s != 83:

				scr.addstr(1,(dims[1]-33)//2,'Presiona \'s\' para salir al menu')
				scr.addstr(2,(dims[1]-20)//2,'El programador malicioso')
				scr.addstr(3, 2,'Debido a la pronta finalización de un proyecto se planea despedir a aquellos programadores solo contratados para este proyecto, nuestro programador es uno de esos ante el inminente despido nuestro programador decide programar errores para evitar ser despedido, para esto el jefe de el no debe darse cuenta por lo que ambos no deben de estar en la misma sala al mismo tiempo, asi mismo nuestro programador se pone nervioso si el número de errores desciendo de 5, esto ocasionara que nuestro programador active una alarma la cual alretara a sus colegas para salir a arreglarla, como sus colegas son muy buenos amigos aprovechan la alarma para juntarse e ir a solucionar el problema, el jefe solo ve la alarma desde su oficina, al momsnto de que todos salgan de la sala nuestro programador cerrara la puerta magnetica para evitar el ingreso de sus colegas y este programara errores más rapido para poder reponer aquellos errores que sus colegas rerparon. Cuando el jefe esta en la sala nuestro programador malicioso no puede activar la alarma.')

				scr.nodelay(0)
				s = scr.getch()
				scr.clear()

		# Ejecucion Visual del programa
		elif q == 50:

			scr.clear()
			scr.nodelay(1)

			#Lista de los ultimos 10 eventos
			textoEntrante = [""]*10

			# Se crean y se inician los hilos la primera vez que se entra en la seccion
			if not hilosEjecucion:
				hiloProg = threading.Thread(target = pro2.progMalicioso, args = [])
				hiloProg.start()

				hiloColega1 = threading.Thread(target = pro2.colega, args = [1])
				hiloColega2 = threading.Thread(target = pro2.colega, args = [2])
				hiloColega3 = threading.Thread(target = pro2.colega, args = [3])
				hiloColega4 = threading.Thread(target = pro2.colega, args = [4])
				hiloColega5 = threading.Thread(target = pro2.colega, args = [5])
				hiloColega6 = threading.Thread(target = pro2.colega, args = [6])
				hiloColega7 = threading.Thread(target = pro2.colega, args = [7])
				hiloColega1.start()
				hiloColega2.start()
				hiloColega3.start()
				hiloColega4.start()
				hiloColega5.start()
				hiloColega6.start()
				hiloColega7.start()

				hiloJefe = threading.Thread(target = pro2.jefe, args = [])
				hiloJefe.start()

				hilosEjecucion = True


			while s != 115 and s != 83:
				s = scr.getch()

				#Esperando la señalizacion de un hilo para actualizar
				inte.senalHilos.acquire()
				scr.clear()

				# Se visualiza el estado actual del escenario
				scr.addstr(1,dims[1]-33,'Presiona \'s\' para salir al menú')
				scr.addstr(2,dims[1]-20,"El programador malicioso")
				scr.addstr(4,(dims[1]-23)//2, inte.escena[0])
				scr.addstr(5,(dims[1]-23)//2, inte.escena[1])
				scr.addstr(6,(dims[1]-23)//2, inte.escena[2])
				scr.addstr(7,(dims[1]-23)//2, inte.escena[3])
				scr.addstr(8,(dims[1]-23)//2, inte.escena[4])
				scr.addstr(9,(dims[1]-23)//2, inte.escena[5])
				scr.addstr(10,(dims[1]-23)//2, inte.escena[6])
				scr.addstr(11,(dims[1]-23)//2, inte.escena[7])
				scr.addstr(12,(dims[1]-23)//2, inte.escena[8])
				scr.addstr(15,(dims[1]-31)//2,"P-Programador Malicioso   C-Colega  J-Jefe")

				#Se actualiza la lista de eventos recientes, y se muestra
				for i in reversed(range(9)):
					textoEntrante[i+1] = textoEntrante[i]
				textoEntrante[0] = inte.escena[9]

				scr.addstr(17,(dims[1]-66)//2,textoEntrante[9])
				scr.addstr(18,(dims[1]-66)//2,textoEntrante[8])
				scr.addstr(19,(dims[1]-66)//2,textoEntrante[7])
				scr.addstr(20,(dims[1]-66)//2,textoEntrante[6])
				scr.addstr(21,(dims[1]-66)//2,textoEntrante[5])
				scr.addstr(22,(dims[1]-66)//2,textoEntrante[4])
				scr.addstr(23,(dims[1]-66)//2,textoEntrante[3])
				scr.addstr(24,(dims[1]-66)//2,textoEntrante[2])
				scr.addstr(25,(dims[1]-66)//2,textoEntrante[1])
				scr.addstr(26,(dims[1]-66)//2,textoEntrante[0]) 
				scr.refresh()
				time.sleep(0.25)

				# Se señaliza que ya se termino de actualizar la pantalla.
				inte.senalActu.release()

		time.sleep(0.05)
	curses.endwin()



menu()
