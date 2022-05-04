# Proyecto 3 Christian Leyva

import sys
import re

# Obtiene el PID el cual se pasa como argumento
def getArgs():
    return sys.argv[1]

def leerMAP(PID):
    ruta = "/proc/"+PID + "/smaps"
    archivoMap = open(ruta, 'r')
    textoMap = archivoMap.read()
    archivoMap.close()
    return textoMap

# Se obtiene y arregla dentro de una lista la informacion proporcionada por el 
# log
def ObtenerPmap(textoLargo:str):
    lineasPMAP = textoLargo.splitlines()
    salida = []
    i = 0
    while i < len(lineasPMAP):
        out = {}
        primera = lineasPMAP[i].split(' ')
        out['desde'] = primera[0].split('-')[0]
        out['hasta'] = primera[0].split('-')[1]
        out['permisos'] = primera[1]
        out['mapeo'] = primera[-1]
        segunda = lineasPMAP[i+1].split(' ')
        out['size'] = segunda[-2]
        out['sizeUnit'] = segunda[-1].lower()
        
        salida.append(out)
        # Se aumenta 23 debido a que cada 23 lineas es sobre un mapeo distinto
        i += 23

    return salida

def getnPaginas(valor,unidad):
    if unidad == 'kb':
        return str(valor/4)
    
    if unidad == 'mb':
        return str((valor*1000)/4)
    
    if unidad == 'gb':
        return str((valor*1000000)/4)
    
    if unidad == 'tb':
        return str((valor*1000000000)/4)

def getUso(mapeo,permisos):
    if mapeo == '[stack]':
        return "Stack"
    elif mapeo == '[heap]':
        return "Heap"
    elif mapeo == '[anon]':
        return 'Mapeo Anonimo'
    elif mapeo in ('[vdso]', '[vsyscall]', '[vectors]'):
        return "Llamada al Sistema"
    elif mapeo == '[vvar]':
        return 'Var Kernel'
    elif mapeo == "":
        return "vacio"
    elif permisos[0].lower() == 'r' and permisos[2].lower() == "x" and "lib" in mapeo:
        return "Bib→Texto"
    elif permisos[0].lower() == 'r' and "lib" in mapeo:
        return "Bib→Datos"
    elif permisos[0].lower() == 'r' and permisos[2].lower() == "x" and "/usr/bin" in mapeo:
        return "Texto"
    elif permisos[0].lower() == 'r' and "/usr/bin" in mapeo:
        return "Datos"
    else:
        return '???'

# Se obtiene el Uso y el num de paginas
def PulirPMap(Pmap:list):
    for line in Pmap:
        line['paginas'] = getnPaginas(int(line['size']),line['sizeUnit'])
        line['uso'] = getUso(line['mapeo'], line['permisos'])

def MostrarPMap(Pmap:list):
    print("|  Uso      |De pág.|A pág. | Tamaño |Núm. páginas|Perm| Uso o mapeo ")
    for line in Pmap:
        print(line['uso'] + '\t' + line['desde'] + '\t' + line['hasta'] + '\t' + line['paginas'] + '\t' + line['permisos']+ '\t'  + line['mapeo'])

def main():
    
    try:
        PID = getArgs()
    except:
        print("\nERROR:\n\tPor favor ingresa el PID del proceso a leer. \nEjemplo de ejecución:\n\n\tpython3 proyecto3_chrisley.py {PID}\n")
        return
    
    try:
        textoMap = leerMAP(PID)
    except:
        print("\nERROR:\n\tNo se pudo acceder al map, verifica que el PID ingresado sea correcto y que el proceso este corriendo.\n")
        return
    Pmap = ObtenerPmap(textoMap)
    PulirPMap(Pmap)
    MostrarPMap(Pmap)

main()