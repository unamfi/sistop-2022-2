#!/usr/bin/python
from mmap import mmap
from time import sleep

mem = open('mem_compartida', 'r+')
memoria = mmap(mem.fileno(), 8192)
memoria[10:15] = b"Mundo"
memoria[5:9] = b"Hola"

while True:
    print(memoria[5:15])
    sleep(2)
