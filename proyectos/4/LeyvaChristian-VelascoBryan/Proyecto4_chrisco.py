# Proyecto 4: (Micro) sistema de archivos
# Autores: Bryan Velasco & Christian Leyva 

# Imports: -------------------------------------------------------------------------------

# Bibliotecas incluidas en el core de Python
import os,sys,mmap,time

# Bibliotecas que requieren instalación vía pip
from tabulate import tabulate
from termcolor import colored, cprint

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
    SuperBloque['version'] = DIMap[10:13].decode('utf-8')
    SuperBloque['volumen'] = DIMap[20:35].decode('utf-8')
    SuperBloque['tamanio'] = DIMap[40:45].decode('utf-8')
    SuperBloque['nClustersDir'] = DIMap[47:49].decode('utf-8')
    SuperBloque['nClustersCom'] = DIMap[52:60].decode('utf-8')

    return SuperBloque

class ChriscoExplorer:
    def ls():
        pass
    def copyLocal():
        pass
    def copyExt():
        pass
    def rm():
        pass
    def defragmentar():
        pass    

def sistemaArchivos(DIMap):
    pass

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