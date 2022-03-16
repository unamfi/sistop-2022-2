import threading
import time
import random
palillos = [threading.Semaphore(1),
            threading.Semaphore(1),
            threading.Semaphore(1),
            threading.Semaphore(1),
            threading.Semaphore(1)]
vueltas = 0
mut = threading.Semaphore(1)

def filosofo(num):
    global vueltas
    while True:
        mut.acquire()
        vueltas += 1
        mut.release()
        piensa(num)
        print('%d -- %d tiene hambre' % (vueltas, num))
        palillos[num].acquire()
        palillos[(num+1) % len(palillos)].acquire()
        come(num)
        palillos[num].release()
        palillos[(num+1) % len(palillos)].release()

def come(num):
    print('%d comiendo' % num)
    time.sleep(random.random() / 100)

def piensa(num):
    print('%d pensando' % num)
    time.sleep(random.random() / 100)

for i in range(5):
    threading.Thread(target=filosofo,args=[i]).start()
