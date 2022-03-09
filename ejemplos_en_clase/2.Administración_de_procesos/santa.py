#!/usr/bin/python3

import threading
import time
import random

tiempo_vacacion=5
num_renos = 9
num_elfos = 10
elfos_para_despertar = 3
p_elfo_torpe = 0.1
barr_elfos = threading.Barrier(elfos_para_despertar)
llegan_renos = threading.Barrier(num_renos)
despierta_a_santa = threading.Semaphore(0)
viaje_terminado=threading.Semaphore(0)
elfo_contrariado = threading.Semaphore(0)
elfos_con_bronca = []
mutex_bronca = threading.Semaphore(1)

def elfo(id:int):
    global elfos_con_bronca
    while True:
        time.sleep(5 * random.random())
        if random.random() < p_elfo_torpe:
            print('EEEE%d: AYYYYYYYY!' % id)
            with mutex_bronca:
                elfos_con_bronca.append(id)
            barr_elfos.wait()
            with mutex_bronca:
                if id == elfos_con_bronca[0]:
                    despierta_a_santa.release()
            elfo_contrariado.acquire()

def santa():
    global elfos_con_bronca
    while True:
        print('*** S: Por fin a dormir')
        despierta_a_santa.acquire()
        print('*** S: ¿Y ora qué?')
        mutex_bronca.acquire()
        if len(elfos_con_bronca) >= 3:
            while len(elfos_con_bronca) > 0:
                elfo = elfos_con_bronca.pop(0)
                print('*** S: Resolviendo la molesta bronca de E%d...' % elfo)
                elfo_contrariado.release()
            mutex_bronca.release()
        else:
            mutex_bronca.release()
            print('*** S: A dar el rol por el mundo')
            time.sleep(2)
            for r in range(num_renos):
                print('*** S: Disfruta tus vacaciones, reno %d!' % r)
                viaje_terminado.release()

def reno(id:int):
    while True:
        vacacion(id)
        llegan_renos.wait()
        if id == 1:
            print('R1: Despertando a Santa')
            despierta_a_santa.release()
        print('R%d: Comencemos el viaje de trabajo' % id)
        viaje_terminado.acquire()

def vacacion(id:int):
    print('El reno %d inicia su vacación anual' % id)
    time.sleep(random.random() * tiempo_vacacion)
    print('El reno %d vuelve de vacaciones' % id)

threading.Thread(target=santa).start()
for i in range(num_renos):
    threading.Thread(target=reno, args=[i]).start()
for i in range(num_elfos):
    threading.Thread(target=elfo,args=[i]).start()
