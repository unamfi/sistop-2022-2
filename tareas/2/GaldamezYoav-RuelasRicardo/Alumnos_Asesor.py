import threading
import random
import time

#Semaforo que funge como multiplex y simula el cubiculo
cubiculoProfesor = threading.Semaphore(6)

#Semaforo que funge como mutex y simula al alumno que esta preguntando
mutex_alumnos = threading.Semaphore(1)

#Semaforo que funge como apagador para despertar al asesor cuando haya un alumno
despertar_asesor = threading.Semaphore(0)

#Semaforo que funge como apagador para avisar que se ha respondido una duda
responder = threading.Semaphore(0)

#Semaforo que representa a los alumnos
alumnos = threading.Semaphore(0)

#Número máximo de alumnos
num_alumnos = 12

def alumno(id):
	while True:
		#Permitimos solamente el acceso a 6 alumnos máximo
		cubiculoProfesor.acquire()

		#Generamos aleatoriamente el número de dudas, de 1 a 3
		dudas = random.randint(1,4)

		#Tenemos un alumno con dudas y protegemos esta sección
		mutex_alumnos.acquire()

		#Se agrega el alumno al arreglo de alumnos con dudas
		alumnos.acquire()
		print("Entrando -> Alumno: %d \t Dudas: %d dudas \t Alumnos en Cubiculo: %d" %(id,dudas,len(alumnos)))
		
		print("Despertando profesor")
		#Señal para despertar al asesor
		despertar_asesor.release()
		mutex_alumnos.release()

		while dudas != 0:
			#Se espera la señal de que el asesor pueda responder mi duda
			responder.acquire()
			#Una vez contestada se resta el número de dudas
			dudas = dudas - 1
			print("Alumno: %d \t Dudas restantes: %d " %(id,dudas))
			if dudas==0:
				#Si el alumno ya no tiene dudas, se elimina del arreglo y avisa que está saliendo del cúbiculo
				alumnos.release()
				print("Saliendo: %d \t Alumnos en Cubiculo: %d" %(id,len(alumnos)))
				break;

			#Esperamos a que se haya respondido a los demás alumnos
			time.sleep(len(alumnos))
		#El alumno ha salido del cubiculo y deja libre un lugar
		cubiculoProfesor.release()
		break;

def asesor():
	while True:
		#Esperamos la señal de que hay un alumno con dudas esperando 
		despertar_asesor.acquire()
		print("*Se estan respondiendo dudas*")
		#Enviamos la señal de que puede responder una duda 
		responder.release()
		responder.acquire()
		#Tiempo que se tarda en responder una duda
		time.sleep(1)
		print("*Se ha respondido una duda*")
		#Enviamos la señal de que puede responder otra duda
		responder.release()
		print("*Se echa un sueñito*")

threading.Thread(target=asesor).start()
for alumno_id in range(num_alumnos):
    threading.Thread(target=alumno, args=[alumno_id]).start()