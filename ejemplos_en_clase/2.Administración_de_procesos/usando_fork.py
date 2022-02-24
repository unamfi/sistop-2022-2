#!/usr/bin/python
import os
import time
import signal

def espera_hijos(sig, frame):
    print('Un hijo terminó. Lo limpiamos.')
    print(os.wait())

def no_me_muero(sig, frame):
    print('No, no me voy a morir :-Þ')

def cambio_de_tamaño(sig,frame):
    print('La ventana cambió de tamaño...')

signal.signal(signal.SIGCLD, espera_hijos)
signal.signal(signal.SIGTERM, no_me_muero)
signal.signal(signal.SIGINT, no_me_muero)
signal.signal(signal.SIGWINCH, cambio_de_tamaño)

print('Mi identificador de proceso (PID) es: %d' % os.getpid())

pid = os.fork()

if pid == 0:
    print('Soy el proceso hijo. Mi PID es %d' % os.getpid())
    time.sleep(2)
    exit(0)

elif pid > 0:
    print('Soy el proceso padre. Mi PID es %d, y el del hijo %d' %
          (os.getpid(), pid))

else:
    print('¡Ocurrió un error! PID=%d' % pid)

time.sleep(10)
