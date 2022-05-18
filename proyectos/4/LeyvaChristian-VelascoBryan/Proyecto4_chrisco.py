# Proyecto 4: (Micro) sistema de archivos
# Autores: Bryan Velasco & Christian Leyva 

# Imports: -------------------------------------------------------------------------------

# Bibliotecas incluidas en el core de Python
import os,sys,mmap,time

# Bibliotecas que requieren instalación vía pip
from tabulate import tabulate
from termcolor import cprint

# Notas importantes:  ---------------------------------------------------------------------

# - Archivo de longitud fija de 1440 Kilobytes
# - La superficie del disco se divide en sectores de 256 bytes.
# - Cada cluster mide cuatro sectores. Es decir 1 cluster = 4*256 = 1024 bytes.
# - El primer cluster (#0) del pseudodispositivo es el superbloque. Este contiene información en los siguientes bytes: 
    # 0–8 -> Para identificación, el nombre del sistema de archivos. ¡Debes validar nunca modificar un sistema de archivos que no sea el correcto! Debe ser la cadena FiUnamFS.
    # 10–13 -> Versión de la implementación. Estamos implementando la versión 1.1
    # 20–35 -> Etiqueta del volumen
    # 40–45 -> Tamaño del cluster en bytes
    # 47–49 -> Número de clusters que mide el directorio
    # 52–60 -> Número de clusters que mide la unidad completa 
# - Toda la info se encuentra en el directorio ubicado entre los clusters 1 a 4, donde cada entrada mide 64 bytes y...
    # 0-15: Nombre del archivo
    # 16–24: Tamaño del archivo, en bytes
    # 25–30: Cluster inicial
    # 31–45: Hora y fecha de creación del archivo, especificando AAAAMMDDHHMMSS (p.ej. ‘20220508182600’ para 2022-05-08 18:26:00)
    # 46–60: Hora y fecha de última modificación del archivo, especificando AAAAMMDDHHMMSS (p.ej. ‘20220509182600’)
    # 61–64: Espacio no utilizado (¿reservado para expansión futura?)
# - Las entradas que no se utilizan llevan la cadena '...............'

# Se declaran algunas variables GLOBALES: --------------------------------------------------

entVacia= '...............' # Entrada de directorio no utilizada
nSistemaArch = 'FiUnamFS'
versionSistArch = '1.1'

# Ahora si, comienza la diversion -----------------------------------------------------------

def abrirImagen(filename):
    diskImg = open(filename,'r+b') # Se lee la imagen de disco con r+b -> 
    DIMap = mmap.mmap(diskImg.fileno(),0,access=mmap.ACCESS_READ)
    return DIMap

# Mediante las especificaciones otorgadas por el docente, se obtiene la info del superbloque
def obtenerInfoSuperBloque(DIMap):
    SuperBloque = {}
    SuperBloque['nombre'] = DIMap[0:8].decode('utf-8')
    SuperBloque['version'] = DIMap[10:13].decode('utf-8').strip()
    SuperBloque['volumen'] = DIMap[20:35].decode('utf-8')
    SuperBloque['tamanio'] = DIMap[40:45].decode('utf-8')
    SuperBloque['nClustersDir'] = DIMap[47:49].decode('utf-8')
    SuperBloque['nClustersCom'] = DIMap[52:60].decode('utf-8')

    return SuperBloque

class Archivo:
    def __init__(self,FileMap):
        self.nombre = FileMap[0:15].decode('utf-8').rstrip('\x00')
        self.tamanio = FileMap[16:24].decode('utf-8')
        self.clusterIn = FileMap[25:30].decode('utf-8')
        self.fechaCreacion = FileMap[31:45].decode('utf-8')
        self.fechaModificacion = FileMap[46:60].decode('utf-8')

# Funcion para listar los archivos en la imagen de disco
def ls(DIMap):
    # Recordando que el tamaño de cada cluster es 1024 bytes
    # Y que el directorio se encuentra entre el Cluster 1-4, se debe empezar a buscar desde 1024 hasta 4096 
    #  Por tanto considerando las entradas de 64 bytes...
    archivos =[]
    tablaArchivos = {}
    tablaArchivos['nombre'] = []
    tablaArchivos['tamaño'] = []
    tablaArchivos['clusterInicial'] = []
    tablaArchivos['fechaCreacion'] = []
    tablaArchivos['fechaModificacion'] = []

    for i in range(0,64):
        desde = 1024 + i * 64
        hasta = desde + 64
        
        archivoLeido = Archivo(DIMap[desde:hasta])
        if archivoLeido.nombre != entVacia and archivoLeido.nombre:
            archivos.append(archivoLeido)
            tablaArchivos['nombre'].append(archivoLeido.nombre)
            tablaArchivos['tamaño'].append(archivoLeido.tamanio)
            tablaArchivos['clusterInicial'].append(archivoLeido.clusterIn)
            tablaArchivos['fechaCreacion'].append(archivoLeido.fechaCreacion)
            tablaArchivos['fechaModificacion'].append(archivoLeido.fechaModificacion)
    # print(tablaArchivos)
    print(tabulate(tablaArchivos,headers='keys',tablefmt='github'))


def copyLocal():
    pass
def copyExt():
    pass
def rm():
    pass
def defragmentar():
    pass    

def sistemaArchivos(DIMap):
    helpComandos = {'Comando':['ls','export [nombreArchivo]','import [nombreArchivo]','del [nombreArchivo]','exit'],'Descripción':['Listar contenidos del directorio FiUnamFs','Copia el archivo ([nombreArchivo]) de FiUnamFs a tu sistema','Copia el archivo ([nombreArchivo]) de tu sistema a FiUnamFs','Elimina el archivo ([nombreArchivo]) de FiUnamFs','Salir del programa.']}
    salir = False
    while not salir:
        entry = input(">>>  ")
        param = entry.lower().split()
        # Se verifica el tipo de operacion que se desea hacer:
        
        if len(param) == 0:
            cprint('Por favor, ingresa un comando.\nEscribe \'help\' para mostrar los comandos disponibles','white','on_red')

        # ls -> Listar contenidos del directorio FiUnamFs
        elif param[0] == 'ls':
            ls(DIMap)

        # Copiar archivo de FiUnamFs a tu sistema
        elif param[0] == 'export':
            pass
        
        # Copiar archivo de tu sistema a FiUnamFs
        elif param[0] == 'import':
            pass
        
        # Eliminar archivo de FiUnamFs
        elif param[0] == 'del':
            pass
        
        elif param[0] == 'help':
            print(tabulate(helpComandos,headers='keys'))

        elif param[0] == 'exit':
            salir = True
        else:
            cprint('El comando \'' + param[0] + '\' no existe\nEscribe \'help\' para mostrar los comandos disponibles','white','on_red')

def main():
    # Primero se abre y mapea la imagen de memoria
    filename = 'fiunamfs.img'
    # Se abre el archivo
    try:
        DIMap = abrirImagen(filename)
    except:
        cprint('Error: El archivo no se puede abrir. Verifica que su nombre sea \'fiunamfs.img\' y que se encuentre en el directorio','white','on_red')

    SuperBloque = obtenerInfoSuperBloque(DIMap)
    # Se verifica que el sistema de archivos sea FiUnamFS para proceder.
    if SuperBloque['nombre'] == nSistemaArch:
        if SuperBloque['version'] == versionSistArch:
            sistemaArchivos(DIMap)
        else:
            cprint('Error: La versión del sistema de archivos no es la 1.1','white','on_red')
    else:
        cprint('Error: El sistema de archivos no es: FiUnamFS','white','on_red')
main()