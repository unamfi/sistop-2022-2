import threading
import time
import random

#variables globales
numMercancia = 4
productos = [[numMercancia, 'leche'], [numMercancia, 'queso'], [numMercancia, 'papel'], [numMercancia, 'agua'], [numMercancia, 'jugo'], [numMercancia, 'coca cola'], [numMercancia, 'pan'], [numMercancia, 'galletas'], [numMercancia, 'sopa'], [numMercancia, 'aceite'], [numMercancia, 'cafe']]
grupos = []
per_max_en_grupo = 5
max_grupos = 0
max_productos = 6
lista_compras = []

#Administracion de procesos
mutex = threading.Semaphore(1)
torniquete = threading.Semaphore(1)
estante = threading.Semaphore(1)
barr_grupos = []
rellenar = threading.Event()

def cliente(id):
	global mutex, per_max_en_grupo, grupos, barr_grupos, max_grupos
	while True:
#cuando aun no hay grupos en la tienda, el primer cliente puede entrar solo o esperar para entrar en grupo
		mutex.acquire()
		num_int_grupo = random.randint(1,per_max_en_grupo)
		num_grupo = random.randint(0, max_grupos)
		if num_grupo == 0 or num_int_grupo == 1:
		# Si num_grupo es 0, o los integrantes es de una persona, entonces se entra solo
			mutex.release()
			time.sleep(0.3)
			print ('╠',id, ': Entrare solo a la tienda')
			going_inside_alone(id)
		else:
			grupo_existente = 0
			# Primero se busca que ya haya alguien del grupo con el que viene el cliente
			for grupo in grupos:
				if grupo[1] == num_grupo:
					# Si para un grupo ya llegaron todos, los extras entran solos
					if grupo[3] + 1 >= grupo[2]:
						grupo_existente = -1
						mutex.release()
						time.sleep(0.3)
						print ('╠',id, ': Entrare solo a la tienda')
						going_inside_alone(id)
					else:
						grupo_existente = grupo[1]
						print ('╠',id, ': Vengo con el grupo ',grupo[1])
						grupos.remove(grupo)
						grupos.append([grupo[0], grupo[1], grupo[2], grupo[3] + 1])
						time.sleep(0.3)
						esperar(grupo[1])
						group_going_inside(grupo, id)
					break
			# Si aun no llega nadie de su grupo, entonces este cliente lo inicia
			if grupo_existente == 0:
				print ('╠',id, ': Entrare en grupo de ', num_int_grupo, 'mi grupo es ', num_grupo)
				time.sleep(0.3)
				print ('╠',id, ': A esperar a que lleguen')
				time.sleep(0.3)
				#grupo [primer cliente, numero de grupo, total integrantes, integrantes que han llegado]
				grupo = [id, num_grupo, num_int_grupo, 1, 1]
				grupos.append(grupo)
				barr_grupos.append([threading.Barrier(num_int_grupo), num_grupo]) 
				#por cada grupo, se crea una barrera
				esperar(num_grupo)
				group_going_inside(grupo, id)
		# El mutex no se libera en cliente (a menos que venga solo) porque se libera cuando se llama a esperar()
				
# Se busca la barrera (el grupo) al que pertenece
def esperar(num_grupo):
	global barr_grupo
	for barrera in barr_grupos:
		if barrera[1] == num_grupo:
			mutex.release()
			barrera[0].wait()
			break
	
def going_inside_alone(id):
	print (' ╬',id, ': Escaneando el codigo QR')
	time.sleep(1.5)
	print (' ╬',id, ': Entre a la tienda')
	time.sleep(0.4)
	buying_alone(id)

def group_going_inside(grupoinfo, id):
	global torniquete
	torniquete.acquire()
	torniquete.release()
	print (' ╬ Grupo' ,grupoinfo[1],': ', grupoinfo[0], 'está escaneando el codigo QR para entrar')
	time.sleep(1)
	print (' ╬',id, ': entre a la tienda con el grupo: ', grupoinfo[1])
	time.sleep(0.4)
	group_buying(grupoinfo, id)

def buying_alone(id):
	global max_productos, mutex, productos, rellenar, estante
	for i in range (max_productos):
		mutex.acquire()
		estante.acquire()
		producto = productos[random.randint(0, len(productos) - 1)]
		if producto[0] <= int(numMercancia/4):
			print ('   ╚ Se esta acabando el producto ', producto[1])
			estante.release()
			# Cuando un producto esta agotandose, se le indica al proveedor para que lo rellene
			# Se libera el estante para que el proveedor pueda usarlo
			rellenar.set()
			time.sleep(0.5)
		else:
			#Se libera el estante para que otro cliente pueda usarlo
			estante.release()
		estante.acquire()
		productos.remove(producto)
		producto[0] = producto[0] - 1
		productos.append(producto)
		estante.release()
		print ('  ╬',id, ' ha comprado ', producto[1])
		time.sleep(0.5)
		mutex.release()
	get_out(id)

def group_buying(grupoinfo, id):
	global mutex, max_productos, productos, lista_compras, rellenar, estante
	for i in range (max_productos):
		mutex.acquire()
		estante.acquire()
		producto = productos[random.randint(0, len(productos) - 1)]
		if producto[0] <= int(numMercancia/4):
			print ('   ╚ Se esta acabando el producto ', producto[1])
			estante.release()
			rellenar.set()
			time.sleep(0.5)
		else:
			estante.release()
		#lista[numero de grupo,total productos] se guarda para evitar que un grupo lleve mas de n productos
		lista_existe = False
		lista_llena = False
		# Se verifica si la lista de compras del grupo ya fue creada
		for lista in lista_compras:
			if lista[0] == grupoinfo[1]:
				lista_existe = True
				if lista[1] < max_productos:
					lista_compras.remove(lista)
					lista_compras.append([lista[0], lista[1] + 1])
				else:
					print ('    ═ El grupo ', grupoinfo[1], ' ya acabo de agarrar')
					time.sleep(0.3)
					lista_llena = True
				break
		if lista_existe == False:
			lista_compras.append([grupoinfo[1], 1])
		if lista_llena == False:
			estante.acquire()
			productos.remove(producto)
			producto[0] = producto[0] - 1
			productos.append(producto)
			estante.release()
			print ('  ╬',id, ' ha agregado ', producto[1], 'a la lista de compras del grupo', grupoinfo[1])
			time.sleep(0.5)
		else:
			mutex.release()
			break
		mutex.release()
	group_going_outside(grupoinfo, id)

def proveedor():
	global rellenar, productos, numMercancia, estante
	rellenar.wait(timeout=None)
	while True:
		if rellenar.wait(timeout=None):
			estante.acquire()
			print ('Provedor: Voy a rellenar lo que esta vacío')
			for producto in productos:
				if producto[0] <= int(numMercancia/4):
					print ('Provedor: Traje mas ', producto[1])
					time.sleep(0.2)
					productos.remove(producto)
					producto[0] = numMercancia
					productos.append(producto)
			rellenar.clear()
			estante.release()

def get_out(id):
	print ('     ╣',id,': Me voy de la tienda...')
	time.sleep(0.5)

def group_going_outside(grupoinfo, id):
	global lista_compras, mutex, grupos
	mutex.acquire()
	esperar(grupoinfo[1])
	mutex.acquire()
	delete_group(grupoinfo, id)
	print ('     ╣',id, ': Me voy de la tienda... Soy del grupo ', grupoinfo[1])
	mutex.release()
	time.sleep(0.4)
	
# Se elimina todo lo relacionado al grupo, para que se puedan ingresar futuros grupos de clientes
def delete_group(grupoinfo, id):
	global grupos
	if grupoinfo[0] == id:
		for lista in lista_compras:
			if lista[0] == grupoinfo[1]:
				lista_compras.remove(lista)
				break
		for barrera in barr_grupos:
			if barrera[1] == grupoinfo[1]:
				barr_grupos.remove(barrera)
				break
		grupos.remove(grupoinfo)

def main():
	global max_grupos
	print("     ╔"+"═"*13+"╗")
	print('     ║  '+'*'*9+'  ║')
	print("     ║  Amazon Go  ║")
	print('     ║  '+'*'*9+'  ║')
	print("     ╚"+"═"*13+"╝")
	numClientes = int(input("¿Cuantos clientes llegaran a la tienda?: "))
	max_grupos = int(input('¿Cuantos grupos como maximo permitira en la tienda? (Se sugiere ingresar total Clientes / 5): '))
	print('Usted ha elegido ',numClientes, 'clientes y ',max_grupos, 'grupos')
	print('Para este caso, solo existira un proveedor (es que lo explotan)')
	time.sleep(1)
	clientes = [threading.Thread(target = cliente, args=[i]).start() for i in range (numClientes)]
	empleado = threading.Thread(target = proveedor, args=[]).start()

main()
