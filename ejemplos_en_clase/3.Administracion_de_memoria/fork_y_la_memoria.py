from os import fork, getpid
from time import sleep

pid = fork()
x = 0

if pid == 0:
    print('Proceso hijo. PID=%d' % getpid())
    x = 4
elif pid > 0:
    print('Proceso padre. PID=%d' % getpid())
    x = 8

sleep(3)
print('Y al final, para %d x vale %d' % (getpid(), x))


