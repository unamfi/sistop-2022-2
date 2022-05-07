# Proyecto 3 Christian Leyva
# Para instalar las bibliotecas necesarias utilizar los siguientes comandos:
# pip install tabulate
# pip install w3lib

import sys
import re
from tabulate import tabulate # ⚠️ Intalacion necesaria - Biblioteca para imprimir en consola de forma tabular.
from PmapToHTML_chrisco import *
import webbrowser

# Obtiene el PID el cual se pasa como argumento
def getArgs():
    return sys.argv[1]

def leerMAP(PID):
    ruta = "/proc/"+PID + "/smaps"
    with open(ruta, 'r') as archivoMap:
        textoMap = archivoMap.read()
    return textoMap

# Se obtiene y arregla dentro de una lista la informacion proporcionada por el 
# log
def ObtenerPmap(textoLargo:str):
    lineasPMAP = textoLargo.splitlines()
    salida = []
    i = 0
    # print("|  Uso      |De pág.|A pág. | Tamaño |Núm. páginas|Perm| Uso o mapeo ")

    # Se inicializa el diccionario con los titulos de las columnas para ser mostradas mas adelante en consola
    out ={}
    out['uso'] = 'Uso'
    out['desde'] = 'De pág.'
    out['hasta'] = 'A pág.'
    out['size'] = 'Tamaño'
    out['sizeUnit'] = ''
    out['paginas'] = 'Paginas'
    out['permisos'] ='Permisos'
    out['mapeo'] = 'Uso o mapeo'
    salida.append(out)
    
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
        return str(int(valor/4))
    
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
        # Se salta la primera iteracion con los titulos de las columnas
        if 'uso' in line:
            continue
        line['paginas'] = getnPaginas(int(line['size']),line['sizeUnit'])
        line['uso'] = getUso(line['mapeo'], line['permisos'])
    
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
    # Para mostrar de manera 'bonita' el Pmap, se utiliza la biblioteca tabulate
    print(tabulate(Pmap,headers="firstrow",tablefmt='fancy_grid'))

    # A partir de aqui se comienza la realizacion de la tabla en html con formato chido
    filename = "Pmap_PID_" + PID + ".html"
    crearHTML(PID,createPmapHTML(Pmap),filename)
    
    # Se abre automáticamente el archivo generado:
    # Si no se desea que se abra automáticamente puede comentar la siguiente linea:
    webbrowser.open_new_tab(filename)

main()