#! /usr/bin/python3

import threading
import time 
import random 

# Variables
hackersEsperando = 0
serfsEsperando = 0
boletosHackers = 0
boletosSerfs = 0
asientosLlenosBote = 0
num_hackers = 5
num_serfs = 5

## Mutex para hackers y serfs
llega_hacker = threading.Semaphore(1)
llega_serf = threading.Semaphore(1)

## Barreras
barreraHackers = threading.Barrier(2)
barreraSerfs = threading.Barrier(2)

## Variables de condición
listosParaPartir = threading.Condition()

def sarpar():
	print("Barco sarpando!")

def abordar(id, tipo):
	print(tipo, " número ", id, "abordando")

def hacker(id):
	global hackersEsperando, boletosHackers, asientosLlenosBote

	llega_hacker.acquire()
	hackersEsperando += 1

	print("hacker %d arribando" %id)
	# Espera para abordar
	while boletosHackers == 0:
		if (asientosLlenosBote+boletosHackers+boletosSerfs < 4) and (hackersEsperando >= 2):
			hackersEsperando -= 2
			boletosHackers += 2
			barreraHackers.reset()
		else:
			barreraHackers.wait()

	# abordando
	boletosHackers -= 1
	abordar(id, tipo)
	asientosLlenosBote += 1

	# sarpando
	if asientosLlenosBote == 4:
		listosParaPartir.notifyAll()
		sarpar()
		asientosLlenosBote = 0
		barreraHackers.reset()
		barreraSerfs.reset()
	else:
		listosParaPartir.wait()

	llega_hacker.release()

def serfs(id):
	global serfsEsperando, boletosSerfs, asientosLlenosBote
	with llega_serf:
		serfsEsperando += 1

		print("serf %d arribando" %id)
		# Espera para abordar
		while boletosSerfs == 0:
			if (asientosLlenosBote+boletosHackers+boletosSerfs < 4) and (serfsEsperando >= 2):
				serfsEsperando -= 2
				boletosSerfs += 2
				barreraSerfs.reset()
			else:
				barreraSerfs.wait()

		# abordando
		boletosSerfs -= 1
		abordar(id, tipo)
		asientosLlenosBote += 1

		# sarpando
		if asientosLlenosBote == 4:
			listosParaPartir.notifyAll()
			sarpar()
			asientosLlenosBote = 0
			barreraHackers.reset()
			barreraSerfs.reset()
		else:
			listosParaPartir.wait()


for i in range(num_hackers):
	threading.Thread(target=hacker, args=[i]).start()

for i in range(num_serfs):
	threading.Thread(target=serfs, args=[i]).start()




