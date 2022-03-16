# -*- coding: utf-8 -*-
"""
Correa González Alfredo
De gatos y ratones

- Tengo k gatos (e I ratones) en casa.
- Les sirvo comida a mis gatos en m platos.
- Gatos y ratones han llegado a un acuerdo para repartirse el
  tiempo y comida pero tienen que convencerme que están haciendo
  su trabajo
- Los gatos pueden comer en sus m platos de comida.
- Los ratones pueden comer en esos platos siempre y cuando
  no sean vistos.
- Si un gato ve a un ratón comiendo, se lo debe comer.
- Los platos están puestos uno junto al otro.
 - Solo un animal puede comer en un plato a la vez.
 - Si un gato está comiendo y ve a un ratón que comienza a comer
  de oitro plato, el gato se lo ve y se lo come.
 - Por acuerdo de caballeros, los gatos no pueden acercarse
  a los platos mientras haya ratones comiendo.
"""

from threading import Semaphore, Thread, Event
import threading
import time
import random

hambreDeGato = 100
hambreDeRaton = 2

numeroDeGatos = 2
numeroDeRatones = 10
platos = []
p = 5

gatosComiendo = 0
ratonesComiendo = 0

mutex_hambreGato = threading.Semaphore(1)
mutex_hambreRaton = threading.Semaphore(1)
entrar_a_comer = Semaphore(1)


def gato(id,m):
    global gatosComiendo, ratonesComiendo, platos, numeroDeRatones 
    while numeroDeRatones != 0:
        time.sleep(random.random() / hambreDeGato)
        entrar_a_comer.acquire()
        entrar_a_comer.release()
        
        mutex_hambreGato.acquire()
        
        if ratonesComiendo > 0:
            print("Gato {} no se acerca a los platos por su orgullo de caballero".format(id))
            mutex_hambreGato.release()
            
        else:
            platos[id%m].acquire()
            print("El gato {} comienza a comer del plato {}".format(id, id%m))
            gatosComiendo = gatosComiendo + 1
            
            print("El gato {} terminó de comer".format(id))
            gatosComiendo = gatosComiendo - 1
            
            platos[id%m].release()
            mutex_hambreGato.release()
            
def raton(id,m):
    global gatosComiendo, ratonesComiendo, platos, numeroDeRatones
    while numeroDeRatones != 0:
        time.sleep(random.random() / hambreDeRaton)
        entrar_a_comer.acquire()
        entrar_a_comer.release()
        mutex_hambreRaton.acquire()
        
        if gatosComiendo > 0:
            print("Se comieron al ratón {}".format(id))
            ratonesComiendo = ratonesComiendo - 1
            numeroDeRatones = numeroDeRatones - 1
            if(numeroDeRatones == 0):
                print("¡¡¡¡¡SE MURIERON TODOS LOS RATONES :(!!!!!")
                time.sleep(10000)
                mutex_hambreRaton.release()
                
        else:
            platos[id%m].acquire()
            print("El ratón {} comienza a comer en el plato {}".format(id, id%m))
            ratonesComiendo = ratonesComiendo + 1
            
            
            print("El ratón {} terminó de comer".format(id))
            ratonesComiendo = ratonesComiendo - 1
            
            platos[id%m].release()
            mutex_hambreRaton.release()
            
            
for i in range(p):
    platos.append(Semaphore(1))

for i in range(numeroDeGatos):
    Thread(target = gato, args = [i,p]).start()
    
for i in range(numeroDeRatones):
    Thread(target = raton, args = [i,p]).start()    

            
                      
            





        
        


