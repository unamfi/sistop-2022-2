# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 22:24:10 2022

@author: axel_
"""
from threading import Semaphore, Thread
from time import sleep


 
#globales
#contadores
Hackers= 0
Serfs = 0
passengers = 0

#mutexes
mutex = Semaphore(1)
balsa_mutex = Semaphore(1)

#semáforos
serfs_cola = Semaphore(0)
hackers_cola = Semaphore(0)



    
    
def aborda(tipo):
    
    
    global passengers
    balsa_mutex.acquire()
    passengers+=1
    print("Soy "+tipo+" y subo a la balsa\n")
    if passengers == 4:
        zarpar()
        passengers=0

    balsa_mutex.release()

def Serf():
    
    global Serfs
    
    global Hackers
    
    mutex.acquire()
    
    Serfs+=1
    
    if Serfs == 4:
        
        
        serfs_cola.release()
        serfs_cola.release()
        serfs_cola.release()
        serfs_cola.release()

        Serfs-=4
        mutex.release()
        aborda("serf")
        
    elif (Hackers == 2 and Serfs == 2):
        
        
        hackers_cola.release()
        hackers_cola.release()
        serfs_cola.release()
        Hackers-=2
        Serfs-=2
        mutex.release()
        aborda("serf")
        
    else:
        
        
        mutex.release()
        serfs_cola.acquire()
        aborda("Serf")
    
def Hacker():  
           
    global Hackers
    
    global Serfs
    
    mutex.acquire()
    
    Hackers+=1
    
    if Hackers==4:        
        
        hackers_cola.release() 
        hackers_cola.release()
        hackers_cola.release()
        hackers_cola.release()
        Hackers-=4         
        mutex.release()       
        aborda("Hacker")      
        
    if (Hackers==2 and Serfs==2): 
        
        
        hackers_cola.release()             
        serfs_cola.release()
        serfs_cola.release()
        Hackers-=2                      
        Serfs-=2
        mutex.release()                        
        aborda("Hacker")    
             
    else:
        
        
        mutex.release()                  
        hackers_cola.acquire()             
        aborda("Hacker")  


def zarpar():
    print("Let´s go\n")
    sleep(1)

for i in range(10):

    Thread(target = Hacker, args = []).start()
    Thread(target = Serf, args = []).start()
