#!/usr/bin/python3
from time import sleep
from os import unlink, getpid

fh = open('/tmp/datos_temporales', 'w+')
fh.write('Bienvenido a mi archivo temporal desde el proceso:')
fh.write('%s' % getpid())
fh.flush()

sleep(10)
unlink('/tmp/datos_temporales')
fh.write('Sigo vivo!')
fh.flush()

sleep(60)
fh.close()
